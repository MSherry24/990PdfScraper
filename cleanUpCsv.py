from os import listdir
from os.path import isfile, join, dirname
import csv

def processRow(row):
	name = getName(row)
	hours = getHours(row)
	salary = getSalary(row)
	title = getTitle(row)
	return {
		'name': name,
		'hours': hours,
		'salary1': salary[0],
		'salary2': salary[1],
		'salary3': salary[2],
		'title': title
	}

def getTitle(row):
	lineAsArray = getLineAsArrayOfStrings(row, 'line3')
	wordsInTitle = []
	for word in lineAsArray:
		if not IsInt(word):
			wordsInTitle.append(word)
	title =  ' '.join(wordsInTitle)
	return title

def getName(row):
	lineAsArray = getLineAsArrayOfStrings(row, 'line1')
	wordsInName = []
	for word in lineAsArray:
		if not IsInt(word):
			wordsInName.append(word)
	name =  ' '.join(wordsInName)
	return name

def getHours(row):
	lineAsArray = getLineAsArrayOfStrings(row, 'line1')
	for word in lineAsArray:
		if IsInt(word):
			return word
	return ''

def getSalary(row):
	lineAsArray = getLineAsArrayOfStrings(row, 'line2')
	salaries = []
	for word in lineAsArray:
		wordWithoutCommas = removeCommas(word)
		if IsInt(wordWithoutCommas):
			salaries.append(wordWithoutCommas)
	formattedSalaries = createOneByThreeArray(salaries)
	return formattedSalaries

def createOneByThreeArray(inputArray):
	while len(inputArray)  < 3:
		inputArray.append('0')
	return inputArray

def getLineAsArrayOfStrings(row, line):
	targetLine = row[line]
	return targetLine.split(' ')

def removeCommas(word):
	return word.replace(',', '')

def IsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def writeRowsToFile(rows, filename):
	with open(getFormattedCsvFilePath(filename), "w") as csvfile:
		fieldNames = ['name', 'title', 'hours', 'salary1', 'salary2', 'salary3']
		out = csv.DictWriter(csvfile, fieldNames)
		out.writeheader()
		for row in rows:
			out.writerow({
				'name' : row['name'],
				'title' : row['title'],
				'hours' : row['hours'],
				'salary1' : row['salary1'],
				'salary2' : row['salary2'],
				'salary3' : row['salary3']
			})

def getFormattedCsvFilePath(file):
	return 'formattedCsv/' + file


csvPath = "./csv"
csvFiles = [f for f in listdir(csvPath) if isfile(join(csvPath, f)) and '.csv' in f]
print csvFiles


for file in csvFiles:
	rows = []
	with open('csv/' + file) as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
		    rowObject = processRow(row)
		    rows.append(rowObject)
		writeRowsToFile(rows, file)



