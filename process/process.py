# Processes and assigns files

import os, subprocess, re, shutil, glob
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from farproof.client_list.models import Page, Revision, PDFFile
from farproof.settings import CONTENTS_PATH, PROFILES_DIR

#####################################################################
# 	Processing options :											#
#####################################################################
# See: http://ghostscript.com/doc/current/Use.htm					#
# and: http://ghostscript.com/doc/current/Devices.htm#TIFF			#
# and: http://ghostscript.com/doc/current/GS9_Color_Management.pdf	#
# CAUTION: is very important that variables are written like this:	#
#          ' -var1 -var2' (note space at beginning of quotes)		#
# CAUTION: order of passed arguments DOES matter!!					#
#####################################################################
# Common options:
gs = r'D:\tmp\gs\bin\gswin64c.exe'
COMMON = ' -dNOPAUSE -dBATCH -dQUIET'

# Render options:
DEVICE = ' -sDEVICE=tiffsep' #Output devices: tiff24nc, tiff32nc, tiffsep
GRAPHICS = ' -dGraphicsAlphaBits=2'
JPEGQ = '100'
TEXT = ' -dTextAlphaBits=4 -dAlignToPixels=0'
COLOR = ' -dUseCIEColor -dDOINTERPOLATE' #-dCOLORSCREEN'

# Color management: 
ICC_FOLDER = ' -sICCProfilesDir=' + PROFILES_DIR
RGB_PROFILE = ' -sOutputICCProfile=sRGB.icm'
CMYK_PROFILE = ' -sOutputICCProfile=CoatedFOGRA27.icc' #-sProofProfile
RENDER_INTENT = ' -dRenderIntent=1' #0:Perceptual, 1:Colorimetric, 2:Saturation, 3:Absolute Colorimetric
OVERPRINT = ' -dSimulateOverprint=true' #Only for CMYK outputs
BPC = ' -dBlackPtComp=1' #0:Don't, #1:Do
PRESERVE_K = ' -dKPreserve=0' #0:No preservation, 1:PRESERVE K ONLY (littleCMS), 2:PRESERVE K PLANE (littleCMS)
#####################################################################
# 	End of processing options.										#
#####################################################################


# RGB devices don't support overprint, conversion from CMYK tiff is neccesary
# TODO: make CMYK_PROFILE and OVERPRINT work together
# TODO: explore -sSourceObjectICC to set the rendering of RGB to CMYK (and maybe CMYK to CMYK)
def process(dpi, pdf, client, job, item, SEPS): 
	tiff_file = NamedTemporaryFile(suffix='-%d.tiff')
	pdf_file = pdf.f
	command = gs + DEVICE + ' -r' + str(dpi) + COMMON + COLOR + GRAPHICS + TEXT + RENDER_INTENT + OVERPRINT + ' -sOUTPUTFILE=' + tiff_file.name +' '+ pdf_file.path
	print('PDF to TIFF... ' + pdf_file.path + ' ->> ' + tiff_file.name)
	print(command)
	tiff_render_proc = subprocess.Popen(command, stdin=subprocess.PIPE)
	tiff_render_proc.communicate()
	
	# Spawn the assign process:
	print("Done rendering TIFF files, converting to JPEG...")
	assign(tiff_file, pdf_file, client, job, item, SEPS)
	
	
def assign(tiff_file, pdf_file, client, job, item, SEPS=False):
	# Extract prefix formfrom NamedTemporaryFile
	prefix = os.path.basename(os.path.normpath(tiff_file.name)).split('-')[0]
	tmpdir = os.path.dirname(tiff_file.name)
	print('Prefix: ' + str(prefix))

	# Check for page range in filename:
	filename = os.path.basename(os.path.normpath(pdf_file.path))
	seq = re.findall('(\d+)', filename)
	start_pos = int(seq[0])
	end_pos = int(seq[1])
	span = (end_pos-start_pos)+1 # sum +1 because the range includes both extremes
	
	# Use initial number to rename JPEGs and send them to their proper page folder:
	for i in range(0,span):
		current_pos = i+start_pos
		# Check if current_page really has a Revision 
		# (because if not, last_rev will return '0' and not a Revision object)
		current_page = Page.objects.get(number=current_pos, item=item)
		current_rev = current_page.last_rev()
		if current_rev:
			next_rev = current_rev.rev_number+1 
		else:
			next_rev = 0
		
		# Create recquired dirs recursively only if they don't exist
		page_dir = os.path.join(CONTENTS_PATH, str(client.pk), str(job.pk), str(item.pk), 'pages', str(current_pos), str(next_rev))
		if os.path.isdir(page_dir):
			print("page_dir already exists: \n\t" + page_dir)
			pass
		else:
			print("Creating page_dir... \n\t" + page_dir)
			os.makedirs(page_dir)
		
		# Construct jpeg_filename and tiff_file:
		tiff_file = os.path.join(tmpdir, (prefix + '-' + str(i+1) + '.tiff'))
		jpeg_filename = str(current_pos) + '.jpg'
		
		# Remove page_dir files if they exists
		if os.path.isfile(page_dir + jpeg_filename):
			os.remove(page_dir + jpeg_filename)
			
		print('TIFF to JPEG... \n\t' + tiff_file + ' ->> ' + os.path.join(page_dir, jpeg_filename))
		
		# IMPORTANT: shell=True is required!! turning path into str also is.
		jpg_render_proc = subprocess.Popen([
			'convert', 
			'-quality', JPEGQ,
			tiff_file,
			'+profile', 'icm',
			'-black-point-compensation',
			'-profile', str(os.path.join(PROFILES_DIR, 'CoatedFOGRA27.icc')),
			'-intent', 'relative',
			'-profile', str(os.path.join(PROFILES_DIR, 'sRGB.icm')),
			str(os.path.join(page_dir, jpeg_filename)),
		], shell=True) 
		
		# Finally, remove intermediate TIFF files:
		jpg_render_proc.wait()
		print("Removing intermediate TIFF files...\n\t " +  tiff_file)
		os.remove(tiff_file)
		
		# Rendering of individual separation files:
		sep_list = glob.glob(os.path.join(tmpdir, (prefix + '-' + str(i+1) + '.tiff*.tif')))
		
		if SEPS:
			print('Processing separations into PNG...')
			for tif_sep_file in sep_list:
				suffix = re.search('\((.*?)\)', tif_sep_file).group(1)
				png_sep_filename = str(current_pos) +'-'+ suffix +'.png'
				sep_render_proc = subprocess.Popen([
					'convert', 
					str(os.path.join(tmpdir, tif_sep_file)),
					# http://www.imagemagick.org/Usage/color_mods/#linear
					# TODO: tint seps before saving.
					# The following fx tints each ink (although it takes a LOOOONG time)
					# imagemagick is not fast, a canvas solution might be more efficient
					# http://stackoverflow.com/questions/11973086/duplicate-photoshops-color-blend-mode-in-imagemagick
					# 'convert image.jpg color_layer.png -compose blend -composite result.jpg'
					# FOGRA27	->	sRGB
					# cyan		->	0,158,224
					# '-size', '100x100',
					# 'canvas:rgb(0,158,224)',
					# '-fx', '1-(1-v.p{0,0})*(1-u)',
					str(os.path.join(page_dir, png_sep_filename)),
				], shell=True)
				
				# Finally, move rendered separations to the proper item's subfolder:
				sep_render_proc.wait()
				print("Removing intermediate separation files... \n\t" + os.path.join(tmpdir, tif_sep_file))
				os.remove(os.path.join(tmpdir, tif_sep_file))
		else:
			for sep_file in sep_list:
				print("Removing unused intermediate separation files... \n\t" + os.path.join(tmpdir, sep_file))
				os.remove(os.path.join(tmpdir, sep_file))
			
	print('Render of ' + pdf_file.path + ' done!')