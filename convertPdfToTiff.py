import subprocess

from os import listdir
from os.path import isfile, join

pdfPath = "./pdf"
pdfFiles = [f for f in listdir(pdfPath) if isfile(join(pdfPath, f)) and '.pdf' in f]
pdfFilesWithPath = []
outFiles = []

for pdfFile in pdfFiles:
	tiffFile = './tiff/' + pdfFile.replace('.pdf', '.tiff')
	outFiles.append(tiffFile)
	pdfFileWithPath = './pdf/' + pdfFile
	pdfFilesWithPath.append(pdfFileWithPath)

print 'pdf files = ', pdfFilesWithPath
print 'outfiles = ', outFiles
for index, pdfFile in enumerate(pdfFilesWithPath):
	print "starting ", pdfFile, outFiles[index]
	subprocess.call(["convert", "-density", "300", pdfFile, "-depth", "8", outFiles[index]])
	print "finished ", pdfFile
