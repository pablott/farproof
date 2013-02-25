import subprocess


# See: http://ghostscript.com/doc/current/Use.htm
# and: http://ghostscript.com/doc/current/Devices.htm#TIFF

gs = 'C:/Users/Pablo/Ghostscript/bin/gswin32c.exe'
#PATH = "D:/tmp/"
COMMON = '-dSAFER', '-dNOPAUSE', '-dBATCH', #'-dQUIET',

# Render Options:
GRAPHICS = '-dGraphicsAlphaBits=2', 
JPEGQ = '-dJPEGQ=95'
TEXT = '-dTextAlphaBits=4', #'-dAlignToPixels=0', 
COLOR = '-dUseCIEColor', '-dDOINTERPOLATE',  '-dCOLORSCREEN', 

# Color Management: 
#INPUT_PROFILE = sRGB|AdobeRGB
#OUTPUT_PROFILE = '-sOutputICCProfile=filename'
#RENDER_INTENT = '-dRenderIntent=0/1/2/3' #relative|absolute|perceptual
#BPC = '-dRenderIntent=0/1/2/3'
#K_PRESERVE = 0/1/2

def handle_uploaded_file(dpi): 
	subprocess.Popen([
		gs, 
		COMMON,
		'-sDEVICE=jpeg', '-r' + str(dpi) + 'x' + str(dpi), 
		TEXT, GRAPHICS, COLOR, JPEGQ,
		'-sOUTPUTFILE=' "D:/tmp/result.jpg", "D:/tmp/source.pdf"
	], shell=True)	
	
	subprocess.Popen([
		gs, 
		COMMON, 
		'-sDEVICE=tiffsep', '-r' + str(dpi) + 'x' + str(dpi), 
		TEXT, GRAPHICS, COLOR, 
		'-sOUTPUTFILE=' "D:/tmp/tiffsep/result.tiff", "D:/tmp/source.pdf", '-sstdout=' "D:/tmp/file.txt"
	], shell=True)	
	
