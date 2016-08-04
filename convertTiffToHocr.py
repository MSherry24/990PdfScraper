import subprocess
from os import listdir
from os.path import isfile, join

tiffPath = './tiff'
tiffFiles = [f for f in listdir(tiffPath) if isfile(join(tiffPath, f))]
print 'tiffFiles = ', tiffFiles

for tiffFile in tiffFiles:
	if '.tiff' in tiffFile:
		fullPath = tiffPath + '/' + tiffFile
		fileName = 'hocr/' + tiffFile.replace('.tiff', '')
		print 'starting', tiffFile, fileName
		subprocess.call(["tesseract", fullPath, fileName, "hocr"])
		print 'finished ', tiffFile