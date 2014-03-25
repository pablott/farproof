# Processes and assigns files
from __future__ import absolute_import # Required by celery

import os, subprocess, re, shutil, glob
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from farproof.client_list.models import Page, Revision, PDFFile
from farproof.settings import CONTENTS_PATH, PROFILES_PATH, TEMP_PATH
from farproof.celery import app

#####################################################################
# 	Processing options :											#
#####################################################################
# See: http://ghostscript.com/doc/current/Use.htm					#
# and: http://ghostscript.com/doc/current/Devices.htm#TIFF			#
# and: http://ghostscript.com/doc/current/GS9_Color_Management.pdf	#
# CAUTION: is very important that variables are written like this:	#
#          ' -var1 -var2' (note space at beginning of quotes)		#
# CAUTION: order of passed arguments DOES matter!!					#
#																	#
# RGB devices don't support overprint, 								#
# conversion from CMYK tiff is neccesary.							#
# TODO: make CMYK_PROFILE and OVERPRINT work together.				#
# TODO: explore -sSourceObjectICC to set the rendering of 			#
# RGB to CMYK (and maybe CMYK to CMYK).								#
#####################################################################

# Common options:
gs = os.path.normpath('D:/tmp/gs/bin/gswin64c.exe')
convert = os.path.normpath('C:/imagemagick-6.8.8-Q16/convert.exe')

# Render options:
DEVICE = '-sDEVICE=tiffsep' #Output devices: tiff24nc, tiff32nc, tiffsep
GRAPHICS = '-dGraphicsAlphaBits=2'
JPEGQ = '80'
TEXT_ALPHA_BITS = '-dTextAlphaBits=4'
TEXT_ALIGN_TO_PIXELS = '-dAlignToPixels=0'

# Color management: 
ICC_FOLDER = '-sICCProfilesDir=' + PROFILES_PATH
RGB_PROFILE = '-sOutputICCProfile=sRGB.icm'
CMYK_PROFILE = '-sOutputICCProfile=CoatedFOGRA27.icc' #-sProofProfile
RENDER_INTENT = '-dRenderIntent=1' #0:Perceptual, 1:Colorimetric, 2:Saturation, 3:Absolute Colorimetric
OVERPRINT = '-dSimulateOverprint=true' #Only for CMYK outputs
BPC = '-dBlackPtComp=1' #0:Don't, #1:Do
PRESERVE_K = '-dKPreserve=0' #0:No preservation, 1:PRESERVE K ONLY (littleCMS), 2:PRESERVE K PLANE (littleCMS)
#####################################################################
# 	End of processing options.										#
#####################################################################


@app.task
def process(dpi, pdf, client, job, item, SEPS): 
	# Check for page range in filename:
	filename = os.path.basename(os.path.normpath(pdf.f.path))
	seq = re.findall('(\d+)', filename)
	start_pos = int(seq[0])
	end_pos = int(seq[1])
	span = (end_pos-start_pos)+1 # sum +1 because the range includes both extremes.

	# Render page by page and send them to their proper folder:
	for i in range(0,span):
		page_current_pos = i+start_pos 	# Item's page position 
		pdf_current_pos = i+1 			# PDF page position
		
		# Extract prefix from NamedTemporaryFile:
		tiff_file = NamedTemporaryFile(suffix='-'+str(pdf_current_pos)+'.tiff', dir=TEMP_PATH)
		prefix = os.path.basename(os.path.normpath(tiff_file.name)).split('-')[0]
		print('Prefix: ' + str(prefix))
		
		cmd1 = [gs, DEVICE, '-r'+str(dpi), '-dFirstPage='+str(pdf_current_pos), '-dLastPage='+str(pdf_current_pos), '-dNOPAUSE', '-dBATCH', '-q', '-dUseCIEColor', '-dDOINTERPOLATE', GRAPHICS, TEXT_ALPHA_BITS, TEXT_ALIGN_TO_PIXELS, RENDER_INTENT, OVERPRINT, '-sOUTPUTFILE='+tiff_file.name, pdf.f.path]
		print(cmd1)
		tiff_render_proc = subprocess.Popen(cmd1)
		tiff_render_proc.communicate()
		print("Done rendering TIFF files, converting to JPEG...")	
	
		# Check if current_page really has a Revision 
		# (because if not, last_rev will return '0' and not a Revision object).
		current_page = Page.objects.get(number=page_current_pos, item=item)
		current_rev = current_page.last_rev()
		if current_rev:
			next_rev = current_rev.rev_number+1
		else:
			next_rev = 0
		
		# Create recquired dirs recursively only if they don't exist:
		page_dir = os.path.join(CONTENTS_PATH, str(client.pk), str(job.pk), str(item.pk), 'pages', str(page_current_pos), str(next_rev))
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
			
		cmd2 = [convert, '-quality', JPEGQ, tiff_file.name, '+profile', 'icm', '-black-point-compensation', '-profile', os.path.join(PROFILES_PATH, 'CoatedFOGRA27.icc'), '-intent', 'relative', '-profile', os.path.join(PROFILES_PATH, 'sRGB.icm'), os.path.join(page_dir, jpeg_filename)]

		print('TIFF to JPEG... \n\t' + tiff_file.name + ' ->> ' + os.path.join(page_dir, jpeg_filename))
		print(cmd2)
		jpeg_render_proc = subprocess.Popen(cmd2)
		jpeg_render_proc.communicate()
		print("Removing TIFF file...\n\t " +  tiff_file.name)
		# Closing is necessary or else the temporary file doesn't get deleted:
		tiff_file.close()
		
		# Rendering of individual separation files:
		sep_list = glob.glob(os.path.join(TEMP_PATH, (prefix + '-' + str(pdf_current_pos) + '.tiff*.tif')))
		if SEPS:
			print('Processing separations into PNGs...')
			for tif_sep_file in sep_list:
				suffix = re.search('\((.*?)\)', tif_sep_file).group(1).lower()
				png_sep_filename = str(page_current_pos) +'-'+ suffix +'.png'
				
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
				cmd3 = [convert, str(os.path.join(TEMP_PATH, tif_sep_file)), str(os.path.join(page_dir, png_sep_filename))]
				print(cmd3)
				sep_render_proc = subprocess.Popen(cmd3)
				sep_render_proc.communicate()
				
				# Finally, move rendered separations to the proper item's subfolder:
				print("Removing separation file... \n\t" + os.path.join(TEMP_PATH, tif_sep_file))
				os.remove(os.path.join(TEMP_PATH, tif_sep_file))
		else:
			for sep_file in sep_list:
				print("Removing unused separation file... \n\t" + os.path.join(TEMP_PATH, sep_file))
				os.remove(os.path.join(TEMP_PATH, sep_file))
			
	print('Render of ' + pdf.f.path + ' done!')