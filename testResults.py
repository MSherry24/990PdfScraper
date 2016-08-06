from os import listdir
from os.path import isfile, join, dirname
import csv

def prettyPrint(school, schools):
	schoolObject = schools[school]
	percent = getPercent(float(schoolObject['actual']) / schoolObject['expected'])
	print school, percent
	print 'actual:', schoolObject['actual'], 'expected:', schoolObject['expected'], '\n' 
	

def getPercent(float):
	return "{0:.0f}%".format(float * 100)

schools = {
	'Boston U 2013 990.csv': { 'expected' : 56 },
	'Columbia 2013 990.csv': { 'expected' : 45 },
	'depaul 2013 990.csv': { 'expected' : 73 },
	'Grinnell 2013 990.csv': { 'expected' : 54 },
	'loyola 2013 990.csv': { 'expected' : 68 },
	'marquette 2013 990.csv': { 'expected' : 50 },
	'northwestern 2013 990.csv': { 'expected' : 58 },
	'Pomona 2013 990.csv': { 'expected' : 57 }
}

csvPath = "./csv"
csvFiles = [f for f in listdir(csvPath) if isfile(join(csvPath, f)) and '.csv' in f]

for file in csvFiles:
	with open('csv/' + file) as csvfile:
		numline = len(csvfile.readlines())
		if file in schools:
			schools[file]['actual'] = numline - 1

totalExpected = 0
totalActual = 0
for school in schools:
	if school in schools:
		prettyPrint(school, schools)
		totalActual += schools[school]['actual']
		totalExpected += schools[school]['expected']

totalPercent = getPercent(float(totalActual) / totalExpected)
print 'Totals:'
print totalPercent
print 'actual:', totalActual, 'expected:', totalExpected, '\n' 