# Processes and assigns files


from farproof.client_list.models import Page, Revision
import os, subprocess, re, shutil


# See: http://ghostscript.com/doc/current/Use.htm
# and: http://ghostscript.com/doc/current/Devices.htm#TIFF
# and: http://ghostscript.com/doc/current/GS9_Color_Management.pdf

# CAUTION: is very important that variables are written like this:
#'-var1 -var2', (with the '' included)
gs = r'D:\tmp\gs\bin\gswin64c.exe',
COMMON = '-dNOPAUSE -dBATCH -dQUIET', # REQUIRES the trailing comma for some odd reason

# Render Options:
GRAPHICS = '-dGraphicsAlphaBits=2'
JPEGQ = '-dJPEGQ=85'
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

CONTENTS_PATH = "D:/tmp/pdf/" #TODO: unify with uploader.py and set in a separate conf file

	


def process(dpi, upload_dir, filename, client, job, item): 
	render_dir = CONTENTS_PATH + str(client.pk) +"/"+ str(job.pk) +"/"+ str(item.pk) +"/render/"
	if os.path.isdir(render_dir):
		print("render_dir already exists")
		pass
	else:
		print("creating render_dir... " + render_dir)
		os.makedirs(render_dir) # TODO: don't stop on OSError and jump to writing chunks


# TODO: temp_dir & filename check before starting processing
	# RGB devices don't support overprint, conversion from CMYK tiff is neccesary
	jpg_render_proc = subprocess.Popen([
		gs,
		'-sDEVICE=jpeg', '-r' + str(dpi),
		COMMON,
		GRAPHICS,
		TEXT,
		JPEGQ,
		#"-dFirstPage=11",
		#"-dLastPage=22",
		#RENDER_INTENT,
		#ICC_FOLDER, RGB_PROFILE, #BPC,
		#COLOR, 
		'-sOUTPUTFILE=' + (render_dir + "%d.jpg"), upload_dir+filename,
	])
	

	# TODO: make CMYK_PROFILE and OVERPRINT work together
	# TODO: explore -sSourceObjectICC to set the rendering of RGB to CMYK (and maybe CMYK to CMYK)
	tiff_render_proc = subprocess.Popen([
		gs,
		'-sDEVICE=tiffsep', '-r' + str(dpi),
		COMMON,
		COLOR, 
		GRAPHICS,
		#"-dFirstPage=11",
		#"-dLastPage=22",
		TEXT,
		RENDER_INTENT,
		#ICC_FOLDER, CMYK_PROFILE, 
		#BPC,
		#PRESERVE_K,
		OVERPRINT,
		'-sOUTPUTFILE=' "D:/tmp/tiffsep/%d.tiff", upload_dir+filename, #'-sstdout=' "D:/tmp/file.txt",
	]) 
	
	jpg_render_proc.wait()
	print("finished rendering, assigning...")
	assign(render_dir, filename, client, job, item)
	tiff_render_proc.wait()
	print("finished separations")
	
	#if jpg_render_proc.returncode:
		#raise Exception('Test error: ')
		#assign(temp_dir, filename, client, job, item)
		#print("finished rendering, assigning...")
	#return float(stdout)
	
	#subprocess.Popen([
	#	gs,
	#	'-o', '-sDEVICE=inkcov', "D:/tmp/source.pdf",
	#]) 
	#print(subprocess.Popen.returncode)
	
def assign(render_dir, filename, client, job, item):
	if 1: #os.path.isdir(temp_dir) & os.path.isfile(filename):
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
				#raise OSError(next_rev)
			else:
				next_rev = 0
			
			# Construct page_dir, new_filename and original_filename
			page_dir = CONTENTS_PATH + str(client.pk) +"/"+ str(job.pk) +"/"+ str(item.pk) +"/pages/"+ str(current_pos) \
			+"/"+ str(next_rev) +"/"
			origin_filename = str(i+1) +".jpg"
			new_filename = str(current_pos) +"-render.jpg"
			
			# Create required dirs recursively only if they don't exist
			if os.path.isdir(page_dir):
				pass
				print("a path with the same name as the desired " \
				"dir, '%s', already exists, skipping." % page_dir)
			else:
				print("created dir: " + page_dir)
				os.makedirs(page_dir)
			
			# Create required files only if they don't exist
			# and remove them before exiting
			if os.path.isfile(page_dir + new_filename):
				os.remove(page_dir + new_filename)
				pass
			
			print("moving..." + render_dir + origin_filename)
			# IMPORTANT: use shutil's copy instead of os.rename because the 
			# latter gets stuck and causes os.remove to not find the files
			shutil.copy(render_dir + origin_filename, page_dir + new_filename)
			print("removing... " + render_dir + origin_filename)
			os.remove(render_dir + origin_filename)
	else:	
		raise OSError("no files given and/or no temp folder given")
		pass
	
	
	def cleanup(temp_dir, origin_filename):
		os.remove(temp_dir + origin_filename)