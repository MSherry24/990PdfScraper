from os import listdir
from os.path import isfile, join, dirname
import csv

def processRow(row):
	line2 = row['line2']
	line2Array = line2.split(' ')
	print line2Array



csvPath = "./csv"
csvFiles = [f for f in listdir(csvPath) if isfile(join(csvPath, f)) and '.csv' in f]
print csvFiles

for file in csvFiles:
	with open('csv/' + file) as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
		    processRow(row)

