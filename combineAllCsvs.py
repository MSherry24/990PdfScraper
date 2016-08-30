from os import listdir
from os.path import isfile, join, dirname
import csv

def processRow(row):
	return {
		'line1': row['line1'],
		'line2': row['line2'],
		'line3': row['line3'],
		'key': row['key'],
		'fein': row['fein'],
		'unitid' : row['unitid'],
		'institutionname' : row['institutionname']
	}


def writeRowsToFile(rows, filename):
	with open('allSchools.csv', "w") as csvfile:
		fieldNames = ['line1', 'line2', 'line3', 'key', 'fein', 'unitid', 'institutionname']
		out = csv.DictWriter(csvfile, fieldNames)
		out.writeheader()
		for row in rows:
			out.writerow({
				'line1': row['line1'],
				'line2': row['line2'],
				'line3': row['line3'],
				'key': row['key'],
				'fein': row['fein'],
				'unitid' : row['unitid'],
				'institutionname' : row['institutionname']
			})


csvPath = "./csv"
csvFiles = [f for f in listdir(csvPath) if isfile(join(csvPath, f)) and '.csv' in f]

rows = []
for file in csvFiles:
	with open('csv/' + file) as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			print row
			rowObject = processRow(row)
			rows.append(rowObject)

writeRowsToFile(rows, file)
