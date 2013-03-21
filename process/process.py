from farproof.client_list.models import Page, Revision
import os, subprocess, re


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

PDF_PATH = "D:/tmp/pdf/" #TODO: unify with uploader.py and set in a separate conf file



def process(dpi, temp_dir, filename): 

# TODO: temp_dir & filename check before starting processing

	#TODO: RGB devices don't support overprint, conversion from CMYK tiff is neccesary
	subprocess.Popen([
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
		'-sOUTPUTFILE=' + (temp_dir + "%d.jpg"), temp_dir+filename,
		#'-sOUTPUTFILE=' + (temp_dir + filename.replace(".pdf","%d.jpg")), temp_dir+filename,
	])
	
	# TODO: make CMYK_PROFILE and OVERPRINT work together
	# TODO: explore -sSourceObjectICC to set the rendering of RGB to CMYK (and maybe CMYK to CMYK)
	subprocess.Popen([
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
		'-sOUTPUTFILE=' "D:/tmp/tiffsep/%d.tiff", temp_dir+filename, #'-sstdout=' "D:/tmp/file.txt",
	]) 
	
	#subprocess.Popen([
	#	gs,
	#	'-o', '-sDEVICE=inkcov', "D:/tmp/source.pdf",
	#]) 

	
def assign(temp_dir, filename, client, job, item, page):
	if 1: #os.path.isdir(temp_dir) & os.path.isfile(filename):
		# Check for page range in filename
		seq = re.findall('(\d+)', filename)
		start_pos = int(seq[0])
		end_pos = int(seq[-1])
		span = (end_pos-start_pos)+1 # sum +1 because the range is including both extremes
		#raise OSError("span=" + str(span))
		#remove#raise OSError("initial number:" + start_pos + ", ending number:" + end_pos)
		
		#TODO: use initial number to rename jpgs and send them to their proper page folder
		
		for i in range(0,span):
			current_pos = i+start_pos
			current_page = Page.objects.get(number=current_pos, item=item)
			current_rev = current_page.last_rev().rev_number
			#raise OSError(current_rev)
			page_dir = PDF_PATH + str(client.pk) +"/"+ str(job.pk) +"/"+ str(item.pk) +"/pages/"+ str(current_pos) \
			+"/"+ str(current_rev) +"/"
			
			
			new_filename = str(current_pos) +"-render.jpg"
			origin_filename = str(i+1) +".jpg"
			if os.path.isdir(page_dir):
				pass
				#raise OSError("a path with the same name as the desired " \
				#"dir, '%s', already exists." % page_dir)
			else:
				raise OSError(page_dir)
				os.makedirs(page_dir)
			
			if os.path.isfile(page_dir+new_filename):
				pass
			else:
				os.rename(temp_dir + origin_filename, page_dir + new_filename)
				#os.delete(temp_dir + origin_filename)
				#os.rename("c:/a", "c:/b")
				
	else:	
		raise OSError("no files given and/or no temp folder given")
		pass
	
	
