import subprocess

from os import listdir
from os.path import isfile, join

pdfPath = "./pdf"
tiffPath = "./tiff"

pdfFiles = [f for f in listdir(pdfPath) if isfile(join(pdfPath, f)) and '.pdf' in f]
tiffFiles = [f for f in listdir(tiffPath) if isfile(join(tiffPath, f)) and '.tiff' in f]

pdfFilesWithPath = []
outFiles = []

for pdfFile in pdfFiles:
	tiffFile = './tiff/' + pdfFile.replace('.pdf', '.tiff')
	outFiles.append(tiffFile)
	pdfFileWithPath = './pdf/' + pdfFile
	pdfFilesWithPath.append(pdfFileWithPath)

for index, pdfFile in enumerate(pdfFilesWithPath):
	if outFiles[index].replace('./tiff/', '') not in tiffFiles:
		print "starting ", pdfFile, outFiles[index]
		subprocess.call(["convert", "-density", "300", pdfFile, "-depth", "8", outFiles[index]])
		print "finished ", pdfFile
	else:
		print "skipping", pdfFile, "tiff already exists"
