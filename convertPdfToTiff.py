import subprocess
import time

from os import listdir
from os.path import isfile, join

pdfPath = "./pdf"
tiffPath = "./tiff"
hocrPath = "./hocr"

pdfFiles = [f for f in listdir(pdfPath) if isfile(join(pdfPath, f)) and '.PDF' in f]
tiffFiles = [f for f in listdir(tiffPath) if isfile(join(tiffPath, f)) and '.tiff' in f]
hocrFiles = [f for f in listdir(hocrPath) if isfile(join(hocrPath, f)) and '.hocr' in f]

pdfFilesWithPath = []
outFiles = []
hocrKeys = set([])

for hocrFile in hocrFiles:
	fileNameSize = len(hocrFile)
	key = hocrFile[:fileNameSize - 5]
	hocrKeys.add(key)

for pdfFile in pdfFiles:
	tiffFile = './tiff/' + pdfFile.replace('.PDF', '.tiff')
	outFiles.append(tiffFile)
	pdfFileWithPath = './pdf/' + pdfFile
	pdfFilesWithPath.append(pdfFileWithPath)

convertedFiles = 0
globalStart = time.time()

for index, pdfFile in enumerate(pdfFilesWithPath):
	if convertedFiles < 100:
		fileNameSize = len(pdfFile)
		key = pdfFile[6:fileNameSize - 4]
		if key not in hocrKeys:
			fileStart = time.time()
			print "starting ", pdfFile, outFiles[index]
			subprocess.call(["convert", "-density", "300", pdfFile, "-depth", "8", outFiles[index]])
			fileFinish = time.time()
			print "finished ", pdfFile, "time for this file:", fileFinish - fileStart, "totalTime:", fileFinish - globalStart
			convertedFiles += 1
		else:
			print "skipping", pdfFile, "hocr file already exists"

globalFinish = time.time()
print "total time:", (globalFinish - globalStart) / convertedFiles