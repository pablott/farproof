# Required by celery:
from __future__ import absolute_import
import os
import sys
import subprocess
import re
import glob

from django.core.files.temp import NamedTemporaryFile

from celery import task, current_task
from farproof.core.models import Client, Job, Item
from farproof.settings import CONTENTS_PATH, TEMP_PATH, PROFILES_PATH



#####################################################################
# Saving PDF, render and assignment to pages.						#
#####################################################################
# Renders PDF to a temporary file and sends it to a celery queue.	#
# TODO: Use 3 queues instead of one:								#
# nr.		name		task					priority			#
#	-------------------------------------------------------------	#
# 	1		render		PDF render to TIFF		top					#
# 	2		compose		TIFF to RGB JPG			medium/top			#
# 	3		seps		TIFF to grayscale PNG	low					#
# 																	#
# Page numbering is taken from PDF filename and used 				#
# as page's absolute position.										#
# Folder structure:													#
# C: Client PK														#
# J: Job PK															#
# I: Item PK														#
# P: Page absolute number 		                                	#
# R: Revision number												#
# /TEMP_PATH/render/						Temporary render files	#
# /CONTENTS_PATH/							User files				#
# /CONTENTS_PATH/profiles/					ICC color profiles		#
# /CONTENTS_PATH/uploads/				 	Uploaded PDF files		#
# /CONTENTS_PATH/C/J/I/pages/ 				Page previews			#
# 		/.../P/R/render/{page_number}.jpg	Previews in RGB JPG		#
# 		/.../P/R/render/{page_number}-c|m|y|k|SPOT.png				#
#											Seps in grayscale PNG	#
#####################################################################

#####################################################################
# 	Processing options.												#
#####################################################################
# See: http://ghostscript.com/doc/current/Use.htm					#
# and: http://ghostscript.com/doc/current/Devices.htm#TIFF			#
# and: http://ghostscript.com/doc/current/GS9_Color_Management.pdf	#
# CAUTION: order of passed arguments DOES matter!!					#
#																	#
# RGB devices don't support overprint, 								#
# conversion from CMYK tiff is neccesary.							#
#																	#
# TODO: make CMYK_PROFILE and OVERPRINT work together.				#
# TODO: explore -sSourceObjectICC to set the rendering of 			#
# 		RGB to CMYK (and maybe CMYK to CMYK).						#
#####################################################################
# Common options:
gs = os.path.normpath('gs')
convert = os.path.normpath('convert')

# Render options:
DEVICE = '-sDEVICE=tiffsep'  # Output devices: tiff24nc, tiff32nc, tiffsep
GRAPHICS = '-dGraphicsAlphaBits=2'
TEXT_ALPHA_BITS = '-dTextAlphaBits=4'
TEXT_ALIGN_TO_PIXELS = '-dAlignToPixels=0'
JPEGQ = '80'

# Color management: 
ICC_FOLDER = '-sICCProfilesDir=' + PROFILES_PATH
RGB_PROFILE = 'sRGB.icm'
CMYK_PROFILE = 'CoatedFOGRA39.icc' # -sProofProfile, -sOutputICCProfile
RENDER_INTENT = '-dRenderIntent=1' # 0:Perceptual, 1:Colorimetric, 2:Saturation, 3:Absolute Colorimetric
OVERPRINT = '-dSimulateOverprint=true' # Only for CMYK outputs
BPC = '-dBlackPtComp=1' # 0:Don't, 1:Do
PRESERVE_K = '-dKPreserve=0' # 0:No preservation, 1:PRESERVE K ONLY (littleCMS), 2:PRESERVE K PLANE (littleCMS)
#####################################################################
# 	End of processing options.										#
#####################################################################

from time import sleep


@task
def process (pdf, client_pk, job_pk, item_pk, DPI=32, SEPS=False):
    n = 1

    def percent ():
        # TODO: This functions doesn't know the number of separations.
        if SEPS:
            # print int(float(i+((1-n)/4))) / float(span)) * 100
            # return int(float(i+(n/4)) / float(span*4)) * 100
            return int(100 * float(i) / float(span))
        else:
            return int(100 * float(i) / float(span))

    client = Client.objects.get(pk=client_pk)
    job = Job.objects.get(pk=job_pk, client=client)
    item = Item.objects.get(pk=item_pk, job=job)

    # Check for page range in filename:
    filename = pdf.title
    seq = re.findall('(\d+)', filename)
    print filename
    start_pos = int(seq[0])
    print len(seq)
    if len(seq) > 1:
        end_pos = int(seq[1])
    else:
        end_pos = start_pos
    span = (end_pos - start_pos) + 1  # sum +1 because the range includes both extremes.

    # Render page by page and send them to their proper folder:
    for i in range(0, span):
        page_current_pos = i + start_pos  # Item's page position
        pdf_current_pos = i + 1  # PDF page position

        current_task.update_state(state='IN PROGRESS',
                                  meta={'percent': percent(), u'filename': filename, 'pdf_current_pos': pdf_current_pos,
                                        'span': span, 'seps': SEPS})

        # Extract prefix from NamedTemporaryFile:
        tiff_file = NamedTemporaryFile(suffix='-' + str(pdf_current_pos) + '.tiff', dir=TEMP_PATH)
        prefix = os.path.basename(os.path.normpath(tiff_file.name)).split('-')[0]
        print('Prefix: ' + str(prefix))

        cmd1 = [gs, DEVICE, '-r' + str(DPI), '-dFirstPage=' + str(pdf_current_pos),
                '-dLastPage=' + str(pdf_current_pos), '-dNOPAUSE', '-dBATCH', '-q', '-dUseCIEColor', '-dDOINTERPOLATE',
                GRAPHICS, TEXT_ALPHA_BITS, TEXT_ALIGN_TO_PIXELS, RENDER_INTENT, OVERPRINT,
                '-sOUTPUTFILE=' + tiff_file.name, pdf.f.path.encode(sys.getfilesystemencoding())]
        print(cmd1)
        tiff_render_proc = subprocess.Popen(cmd1)
        tiff_render_proc.communicate()
        print("Done rendering TIFF files, converting to JPEG...")

        # Check if current_page really has a Revision
        # (because if not, last_rev will return '0' and not a Revision object).
        # current_version = version.objects.filter(abs_num=page_current_pos, name='base').page()
        # current_page = Page.objects.filter(item=item, version=current_version)
        current_version = version.objects.filter(abs_num=page_current_pos, name='base').page()

        current_rev = current_page.last_rev()
        if current_rev:
            next_rev = current_rev.rev_number + 1
        else:
            next_rev = 0

        # Create recquired dirs recursively only if they don't exist:
        page_dir = os.path.join(CONTENTS_PATH, str(client.pk), str(job.pk), str(item.pk), 'pages',
                                str(page_current_pos), str(next_rev))
        if os.path.isdir(page_dir):
            print("Directory already exists, skipping: \n\t" + page_dir)
            pass
        else:
            print("Creating directory... \n\t" + page_dir)
            os.makedirs(page_dir)

        # Construct jpeg_filename:
        jpeg_filename = str(page_current_pos) + '.jpg'

        # Remove page_dir files if they exist:
        if os.path.isfile(page_dir + jpeg_filename):
            os.remove(page_dir + jpeg_filename)

        cmd2 = [convert, '-quality', JPEGQ, tiff_file.name, '+profile', 'icm', '-black-point-compensation', '-profile',
                os.path.join(PROFILES_PATH, CMYK_PROFILE), '-intent', 'relative', '-profile',
                os.path.join(PROFILES_PATH, RGB_PROFILE), os.path.join(page_dir, jpeg_filename)]

        print('TIFF to JPEG... \n\t' + tiff_file.name + ' ->> ' + os.path.join(page_dir, jpeg_filename))
        print(cmd2)
        jpeg_render_proc = subprocess.Popen(cmd2)
        jpeg_render_proc.communicate()
        print("Removing TIFF file...\n\t " + tiff_file.name)
        # Closing is necessary or else the temporary file doesn't get deleted:
        tiff_file.close()

        # Rendering of individual separation files:
        sep_list = glob.glob(os.path.join(TEMP_PATH, (prefix + '-' + str(pdf_current_pos) + '.tiff*.tif')))
        if SEPS:
            print('Processing separations into PNGs...')
            for n, tif_sep_file in enumerate(sep_list):
                # Get sep_name form filename and transcode it into unicode,
                # it has to find out the FS encoding to get right chars.
                sep_name = re.search('\((.*?)\)', tif_sep_file.decode(sys.getfilesystemencoding())).group(1).lower()
                print 'tif_sep_file: ' + tif_sep_file + '\t' + str(type(tif_sep_file))
                print 'sep_name: ' + sep_name + '\t' + str(type(sep_name))

                # Construct png_sep_filename:
                png_sep_filename = str(page_current_pos) + '-' + sep_name + '.png'

                current_task.update_state(state='IN PROGRESS',
                                          meta={'percent': percent(), u'filename': filename,
                                                'pdf_current_pos': pdf_current_pos, 'span': span, u'sep_name': sep_name,
                                                'seps': SEPS})
                sleep(.5)

                # # http://www.imagemagick.org/Usage/color_mods/#linear
                # # TODO: Tint seps before saving. Suggestions: -map palette or -fx as follows:
                # # fx tints each ink (although it takes a LOOOONG time)
                # # imagemagick is not fast, a canvas solution might be more efficient
                # # http://stackoverflow.com/questions/11973086/duplicate-photoshops-color-blend-mode-in-imagemagick
                # # 'convert image.jpg color_layer.png -compose blend -composite result.jpg'
                # # FOGRA27		->	sRGB
                # # cyan		->	0,158,224
                # '-size', '100x100',
                # 'canvas:rgb(0,158,224)',
                # '-fx', '1-(1-v.p{0,0})*(1-u)',

                # The png_sep_filename needs to be saved.
                cmd3 = [convert, tif_sep_file,
                        os.path.join(page_dir, png_sep_filename.encode(sys.getfilesystemencoding()))]
                print(cmd3)
                sep_render_proc = subprocess.Popen(cmd3)
                sep_render_proc.communicate()

                # Finally, move rendered separations to the proper item's subfolder:
                print "Removing separation file... \n\t" + tif_sep_file
                os.remove(tif_sep_file)
        else:
            for sep_file in sep_list:
                print("Removing unused separation file... \n\t" + os.path.join(TEMP_PATH, sep_file))
                os.remove(os.path.join(TEMP_PATH, sep_file))

    current_task.update_state(state='IN PROGRESS',
                              meta={'percent': 100, u'filename': filename, 'pdf_current_pos': pdf_current_pos,
                                    'span': span, 'seps': SEPS})
    print('Render of ' + pdf.f.path + ' done!')
    sleep(10)
