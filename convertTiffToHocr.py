import subprocess
from os import listdir
from os.path import isfile, join

def getTiffKey(file):
	return file.replace('./tiff/', '').replace('.tiff', '')

def getHocrKey(file):
	return file.replace('./hocr/', '').replace('.hocr', '')

tiffPath = './tiff'
hocrPath = './hocr'
tiffFiles = [f for f in listdir(tiffPath) if isfile(join(tiffPath, f))]
hocrFiles = [f for f in listdir(hocrPath) if isfile(join(hocrPath, f))]

hocrFileSet = set([])
for hocrFile in hocrFiles:
	hocrFileSet.add(getHocrKey(hocrFile))

print 'tiffFiles = ', tiffFiles
print 'hocrFileSet = ', hocrFileSet

for tiffFile in tiffFiles:
	if getTiffKey(tiffFile) not in hocrFileSet:
		fullPath = tiffPath + '/' + tiffFile
		fileName = 'hocr/' + tiffFile.replace('.tiff', '')
		print 'starting', tiffFile, fileName
		subprocess.call(["tesseract", fullPath, fileName, "hocr"])
		print 'finished ', tiffFile
	else:
		print 'skipping', tiffFile, 'hocr exists'