import subprocess
from os import listdir, remove
from os.path import isfile, join, exists

def getTiffKey(file):
	return file.replace('./tiff/', '').replace('.tiff', '')

def getHocrKey(file):
	return file.replace('./hocr/', '').replace('.hocr', '')

def convertTiffToHocr():
	tiffFiles = [f for f in listdir(tiffPath) if isfile(join(tiffPath, f))]
	hocrFiles = [f for f in listdir(hocrPath) if isfile(join(hocrPath, f))]

	hocrFileSet = set([])
	for hocrFile in hocrFiles:
		hocrFileSet.add(getHocrKey(hocrFile))

	for tiffFile in tiffFiles:
		if getTiffKey(tiffFile) not in hocrFileSet:
			fullPath = tiffPath + '/' + tiffFile
			fileName = 'hocr/' + tiffFile.replace('.tiff', '')
			print 'starting', tiffFile, fileName
			subprocess.call(["tesseract", fullPath, fileName, "hocr"])
			print 'finished ', tiffFile
		else:
			print 'skipping', tiffFile, 'hocr exists'

pdfPath = "./pdf"
tiffPath = "./tiff"
hocrPath = "./hocr"

pdfFiles = [f for f in listdir(pdfPath) if isfile(join(pdfPath, f)) and '.PDF' in f]
tiffFiles = [f for f in listdir(tiffPath) if isfile(join(tiffPath, f)) and '.tiff' in f]
hocrFiles = [f for f in listdir(hocrPath) if isfile(join(hocrPath, f)) and '.hocr' in f]

pdfFilesWithPath = []
outFiles = []
hocrKeys = set([])
numPdfFiles = len(pdfFiles)
processed = 1

for hocrFile in hocrFiles:
	fileNameSize = len(hocrFile)
	key = hocrFile[:fileNameSize - 5]
	hocrKeys.add(key)

for pdfFile in pdfFiles:
	tiffFile = './tiff/' + pdfFile.replace('.PDF', '.tiff')
	outFiles.append(tiffFile)
	pdfFileWithPath = './pdf/' + pdfFile
	pdfFilesWithPath.append(pdfFileWithPath)

for index, pdfFile in enumerate(pdfFilesWithPath):
	fileNameSize = len(pdfFile)
	key = pdfFile[6:fileNameSize - 4]
	if key not in hocrKeys:
		print "starting ", pdfFile, outFiles[index], "#", processed, "of", numPdfFiles
		subprocess.call(["convert", "-density", "300", pdfFile, "-depth", "8", outFiles[index]])
		convertTiffToHocr()
		if exists(outFiles[index]):
			remove(outFiles[index])
	else:
		print "skipping", pdfFile, "hocr file already exists"
	processed += 1