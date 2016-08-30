import subprocess
import time
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

numTiffFiles = len(tiffFiles)
processed = 0
globalStart = time.time()

for tiffFile in tiffFiles:
	processed += 1
	print 'processing #', processed, 'of', numTiffFiles
	if getTiffKey(tiffFile) not in hocrFileSet:
		tiffStart = time.time()
		fullPath = tiffPath + '/' + tiffFile
		fileName = 'hocr/' + tiffFile.replace('.tiff', '')
		print 'starting', tiffFile, fileName
		subprocess.call(["tesseract", fullPath, fileName, "hocr"])
		finishTime = time.time()
		timeForThisFile = finishTime - tiffStart
		print 'finished ', tiffFile, 'time for this file', timeForThisFile
	else:
		print 'skipping', tiffFile, 'hocr exists'

finishTime = time.time()
print 'totalTime:', finishTime - globalStart
print 'average time per file:', (finishTime - globalStart) / processed