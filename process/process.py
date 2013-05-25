# Processes and assigns files

import os, subprocess, re, shutil, glob
from farproof.client_list.models import Page, Revision
from farproof.settings import CONTENTS_PATH

# See: http://ghostscript.com/doc/current/Use.htm
# and: http://ghostscript.com/doc/current/Devices.htm#TIFF
# and: http://ghostscript.com/doc/current/GS9_Color_Management.pdf

# CAUTION: is very important that variables are written like this:
#'-var1 -var2', (with the '' included)
gs = r'D:\tmp\gs\bin\gswin64c.exe',
COMMON = '-dNOPAUSE -dBATCH -dQUIET', # REQUIRES the trailing comma for some odd reason


# Render Options:
GRAPHICS = '-dGraphicsAlphaBits=2'
JPEGQ = '100'
TEXT = '-dTextAlphaBits=4 -dAlignToPixels=0'
COLOR = '-dUseCIEColor -dDOINTERPOLATE' #-dCOLORSCREEN'

# Color Management: 
ICC_FOLDER = '-sICCProfilesDir=' "D:/tmp/profiles/"
RGB_PROFILE = '-sOutputICCProfile=sRGB.icm'
CMYK_PROFILE = '-sOutputICCProfile=CoatedFOGRA27.icc' #-sProofProfile
RENDER_INTENT = '-dRenderIntent=1' #0:Perceptual, 1:Colorimetric, 2:Saturation, 3:Absolute Colorimetric
OVERPRINT = '-dSimulateOverprint=true' #Only for CMYK outputs
BPC = '-dBlackPtComp=1' #0:Don't, #1:Do
PRESERVE_K = '-dKPreserve=0' #0:No preservation, 1:PRESERVE K ONLY (littleCMS), 2:PRESERVE K PLANE (littleCMS)
	


def process(dpi, upload_dir, filename, client, job, item, SEPS=False): 
	render_dir = os.path.join(CONTENTS_PATH, str(client.pk), str(job.pk), str(item.pk), 'render')
	if os.path.isdir(render_dir):
		print("render_dir already exists: " + render_dir)
		pass
	else:
		print("creating render_dir... " + render_dir)
		os.makedirs(render_dir) # TODO: don't stop on OSError and jump to writing chunks

	# RGB devices don't support overprint, conversion from CMYK tiff is neccesary
	# TODO: make CMYK_PROFILE and OVERPRINT work together
	# TODO: explore -sSourceObjectICC to set the rendering of RGB to CMYK (and maybe CMYK to CMYK)
	print('PDF to TIFF... ' + os.path.join(upload_dir, filename) +' ->> '+ render_dir)
	tiff_render_proc = subprocess.Popen([
		gs,
		'-sDEVICE=tiffsep', '-r' + str(dpi), #tiff24nc, tiff32nc, tiffsep
		COMMON,
		COLOR, 
		GRAPHICS,
		TEXT,
		RENDER_INTENT,
		OVERPRINT,
		'-sOUTPUTFILE=' + os.path.join(render_dir, "%d.tiff"), os.path.join(upload_dir, filename), #'-sstdout=' "D:/tmp/file.txt",
	]) 
	
	# Wait for render to finish and spawn the assign process
	tiff_render_proc.wait()
	print("finished rendering TIFF, converting to JPEG...")
	assign(render_dir, filename, client, job, item, SEPS)
	
	
def assign(render_dir, filename, client, job, item, SEPS):
	# Check for page range in filename
	seq = re.findall('(\d+)', filename)
	start_pos = int(seq[0])
	end_pos = int(seq[-1])
	span = (end_pos-start_pos)+1 # sum +1 because the range is including both extremes
	
	# Use initial number to rename jpgs and send them to their proper page folder
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
		
		# Construct page_dir, new_filename and original_filename
		page_dir = os.path.join(CONTENTS_PATH, str(client.pk), str(job.pk), str(item.pk), 'pages', str(current_pos), str(next_rev))
		origin_filename = str(i+1) +".tiff"
		new_filename = str(current_pos) +"-render.jpg"
		
		# Create required dirs recursively only if they don't exist
		if os.path.isdir(page_dir):
			print("page_dir already exists: " + page_dir)
			pass
		else:
			print("creating page_dir... " + page_dir)
			os.makedirs(page_dir)
		
		# Remove target dir files if they exists
		if os.path.isfile(page_dir + new_filename):
			os.remove(page_dir + new_filename)
			
		print('TIFF to JPG... ' + os.path.join(render_dir, origin_filename) +' ->> '+ os.path.join(page_dir, new_filename))
		
		# IMPORTANT: shell=True is required!! turning path into str also is.
		# Order of passed arguments DOES matter.
		jpg_render_proc = subprocess.Popen([
			'convert', 
			'-quality', JPEGQ,
			str(os.path.join(render_dir, origin_filename)),
			'+profile', 'icm',
			'-black-point-compensation',
			'-profile', r'D:\tmp\profiles\CoatedFOGRA27.icc',
			'-intent', 'relative',
			'-profile', r'D:\tmp\profiles\sRGB.icm',
			str(os.path.join(page_dir, new_filename)),
		], shell=True) 
		
		# Finally, move rendered files to the proper item's subfolder.
		jpg_render_proc.wait()
		print("removing intermediate files... " + os.path.join(render_dir, origin_filename))
		os.remove(os.path.join(render_dir, origin_filename))

		
		# Render individual separation files:
		# TODO: It should process all separations (CMYK+spots) and import them with a name 
		#		(maybe adding UI for this?).
		print('processing separations into png...')
		# TODO, CAUTION: chdir() changes the dir for any actions that happens afterwards
		#os.chdir(render_dir)
		# http://stackoverflow.com/questions/431684/how-do-i-cd-in-python
		sep_list = glob.glob(str(i+1)+'.tiff*.tif')
		if SEPS:
			for org_sep_filename in sep_list:
				print org_sep_filename
				suffix = re.search('\((.*?)\)', org_sep_filename).group(1)
				dst_sep_filename = str(current_pos) +'-'+ suffix +'.png'
				
				sep_render_proc = subprocess.Popen([
					'convert', 
					str(os.path.join(render_dir, org_sep_filename)),
					# http://www.imagemagick.org/Usage/color_mods/#linear
					# TODO: tint seps before saving.
					# The following fx tints each ink (although it takes a LOOOONG time)
					# imagemagick is not fast, a canvas solution might be more efficient
					# http://stackoverflow.com/questions/11973086/duplicate-photoshops-color-blend-mode-in-imagemagick
					# 'convert image.jpg color_layer.png -compose blend -composite result.jpg'
					# FOGRA27	->	sRGB
					# cyan		->	0,158,224
					# This works: C:\Users\Pablo>convert D:\tmp\pdf\1\10\26\render\9.tiff(Black).tif xc:rgb(0,158,224) -fx 1-(1-v.p{0,0})*(1-u) 000.png
					#'-size', '100x100',
					#'canvas:rgb(0,158,224)',
					#'-fx', '1-(1-v.p{0,0})*(1-u)',
					str(os.path.join(page_dir, dst_sep_filename)),
				], shell=True)
				
				# Finally, move rendered separations to the proper item's subfolder.
				sep_render_proc.wait()
				print("removing intermediate sep files... " + os.path.join(render_dir, org_sep_filename))
				os.remove(os.path.join(render_dir, org_sep_filename))
		else:
			for org_sep_filename in sep_list:
				print("removing intermediate sep files... " + os.path.join(render_dir, org_sep_filename))
				os.remove(os.path.join(render_dir, org_sep_filename))
			
	print('Render of '+filename+' done!')