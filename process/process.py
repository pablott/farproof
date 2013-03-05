import subprocess


# See: http://ghostscript.com/doc/current/Use.htm
# and: http://ghostscript.com/doc/current/Devices.htm#TIFF
# and: http://ghostscript.com/doc/current/GS9_Color_Management.pdf

# CAUTION: is very important that variables are written like this:
#'-var1 -var2', (with the '' included)
gs = r'D:\tmp\gs\bin\gswin64c.exe',
#PATH = "D:/tmp/"
COMMON = '-dNOPAUSE -dBATCH -dQUIET', # REQUIRES the trailing comma for some odd reason

# Render Options:
GRAPHICS = '-dGraphicsAlphaBits=2'
JPEGQ = '-dJPEGQ=95'
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

def handle_uploaded_file(dpi): 
	#TODO: RGB devices don't support overprint, conversion from CMYK tiff is neccesary
	subprocess.Popen([
		gs,
		'-sDEVICE=jpeg', '-r' + str(dpi),
		COMMON,
		GRAPHICS,
		TEXT,
		JPEGQ,
		#RENDER_INTENT,
		#ICC_FOLDER, RGB_PROFILE, #BPC,
		#COLOR, 
		'-sOUTPUTFILE=' "D:/tmp/result.jpg", "D:/tmp/upload.pdf",
	])
	# TODO: make CMYK_PROFILE and OVERPRINT work together
	# TODO: explore -sSourceObjectICC to set the rendering of RGB to CMYK (and maybe CMYK to CMYK)
	subprocess.Popen([
		gs,
		'-sDEVICE=tiffsep', '-r' + str(dpi),
		COMMON,
		COLOR, 
		GRAPHICS,
		TEXT,
		RENDER_INTENT,
		#ICC_FOLDER, CMYK_PROFILE, 
		#BPC,
		#PRESERVE_K,
		OVERPRINT,
		'-sOUTPUTFILE=' "D:/tmp/tiffsep/result.tiff", "D:/tmp/upload.pdf", #'-sstdout=' "D:/tmp/file.txt",
	]) 
	
	#subprocess.Popen([
	#	gs,
	#	'-o', '-sDEVICE=inkcov', "D:/tmp/source.pdf",
	#], shell=True) 

#TODO: just delete this function
def handle_uploaded_file2(dpi): 
	subprocess.Popen([
		gs, 
		'-dNOPAUSE', '-dBATCH', '-dQUIET', 
		'-sDEVICE=jpeg', '-sOUTPUTFILE=' "D:/tmp/resultqq.jpg", "D:/tmp/source.pdf"
	], shell=True)

	
