import subprocess


#PATH = "D:/tmp/"
#GRAPHICS = '-dGraphicsAlphaBits=4',
#TEXT = '-dTextAlphaBits=4',
#COLOR = '-dUseCIEColor', '-dDOINTERPOLATE',
#INPUT_PROFILE = sRGB|AdobeRGB
#OUTPUT_PROFILE = FOGRA27|FOGRA39|SWOP2
#RENDER_INTENT = -dRenderIntent=0/1/2/3 #relative|absolute|perceptual
#BPC = -dRenderIntent=0/1/2/3
#JPEGQ = 100

def handle_uploaded_file(dpi): 
	subprocess.Popen(['C:/Users/Pablo/Ghostscript/bin/gswin32c.exe', '-dSAFER', '-dNOPAUSE', '-dBATCH', '-sDEVICE=jpeg', '-r' + str(dpi) + 'x' + str(dpi), '-dTextAlphaBits=3', '-dGraphicsAlphaBits=3', '-dJPEGQ=0', '-sOUTPUTFILE=' "D:/tmp/result.jpg", "D:/tmp/source.pdf"], shell=True)	
	
	subprocess.Popen(['C:/Users/Pablo/Ghostscript/bin/gswin32c.exe', '-dSAFER', '-dNOPAUSE', '-dBATCH', '-dUseCIEColor', '-sDEVICE=tiffsep', '-r' + str(dpi) + 'x' + str(dpi), '-dTextAlphaBits=3', '-dGraphicsAlphaBits=3', '-sOUTPUTFILE=' "D:/tmp/tiffsep/result.tiff", "D:/tmp/source.pdf"], shell=True)	
	
