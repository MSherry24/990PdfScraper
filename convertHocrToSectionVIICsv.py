from lxml import html
import requests
from HTMLParser import HTMLParser
import bs4
import subprocess
from os import listdir
from os.path import isfile, join, dirname
import csv

def encodeUtf8(text):
	return text.encode('utf-8').strip()

def person(line1, line2, line3, key):
	info = {}
	info['line1'] = encodeUtf8(line1.text)
	info['line2'] = encodeUtf8(line2.text)
	info['line3'] = encodeUtf8(line3.text)
	info['key'] = encodeUtf8(key)
	return info

def getSectionVIIPersonInfo(tree):
	people = []
	pages = tree.select('.ocr_page')

	formYear = getFormYear(pages)
	if formYear is 0:
		return people

	for page in pages:
		if pageIsPartVII(page):
			# print 'found part vii page'
			peopleOnPage = lookForPeopleOnPage(page)
			people = people + peopleOnPage

	return people

def getFormYear(pages):
	for page in pages:
		if blobContainsListValue(page, ['990 (2013)']):
			return 2013
		if blobContainsListValue(page, ['990 (2014)']):
			return 2014
	return 0


def pageIsPartVII(page):
	keywords = ["Part VII - Compensation", 
				"Part VII Compensation", 
				"Compensation of Officers",
				"w-2/1099-misc",
				"W- 2/1099-"]
	return blobContainsListValue(page, keywords)

def lookForPeopleOnPage(page):
	people = []
	paragraphs = page.select('.ocr_par')
	for paragraph in paragraphs:
		if paragraphContainsPersonInformation(paragraph):
			# print 'found line'
			foundPeople = findPeopleFromParagraph(paragraph)
			people = people + foundPeople
	return people

def paragraphContainsPersonInformation(paragraph):
	keywords = ["dotted line", 
				"dotted IIne", 
				"organizations a", 
				"9 related below", 
				"Name and Title Average",
				"dotted |Ine"]
	return blobContainsListValue(paragraph, keywords)

def findPeopleFromParagraph(paragraph):
	people = []
	lines = paragraph.select('.ocr_line')
	lineLength = len(lines)
	for index, line in enumerate(lines):
		foundAName, key = lineContainsAName(line)
		if foundAName and (index + 2) < lineLength:
			newPerson = person(lines[index], lines[index + 1], lines[index + 2], key)
			people.append(newPerson)
	return people

def lineContainsAName(line):
	words = line.select('.ocrx_word')
	for word in words:
		if word.text.lower() in nameSet:
			return True, word.text.lower()
	return False, ''

def blobContainsListValue(blob, listOfStrings):
	if any (x.lower() in blob.text.lower() for x in listOfStrings):
		return True
	return False

def writePeopleToFile(people, filename):
	with open(getCsvFilePath(filename), "w") as csvfile:
		fieldNames = ['line1', 'line2', 'line3', 'key', 'fein', 'unitid', 'institutionname']
		out = csv.DictWriter(csvfile, fieldNames)
		out.writeheader()
		for person in people:
			out.writerow({
				'line1' : person['line1'],
				'line2' : person['line2'],
				'line3' : person['line3'],
				'key' : person['key'],
				'fein': person['fein'],
				'unitid' : person['unitid'],
				'institutionname' : person['institutionname']
			})
	

def processForm(filename, fein):
	with open(filename, 'r') as myfile:
		data = myfile.read().replace('\n','')
		
	soup = bs4.BeautifulSoup(data)
	people = getSectionVIIPersonInfo(soup)
	for person in people:
		person['fein'] = fein
		person['unitid'] = feinDict[fein]['unitid']
		person['institutionname'] = feinDict[fein]['institutionname']
	writePeopleToFile(people, filename)

def getCsvFilePath(filename):
	script_dir = dirname(__file__)
	rel_path = filename.replace('hocr', 'csv')
	return join(script_dir, rel_path)

def getNamesSet():
	names = set([])
	namePath = './names'
	nameFiles = [f for f in listdir(namePath) if isfile(join(namePath, f)) and '.csv' in f]
	for nameFile in nameFiles:
		with open('./names/' + nameFile, 'r') as csvfile:
			content = csvfile.readlines()
			for line in content:
				names.add(line.lower().replace('\n', '').replace('\r', '').replace(' ', ''))

	ignoreNames = getIgnoreNames()
	for ignoreName in ignoreNames:
		if ignoreName in names:
			names.remove(ignoreName)
	return names

def getIgnoreNames():
	names = set([])
	namePath = './'
	nameFiles = [f for f in listdir(namePath) if isfile(join(namePath, f)) and 'ignoreNames.csv' in f]
	for nameFile in nameFiles:
		with open('./' + nameFile, 'r') as csvfile:
			content = csvfile.readlines()
			for line in content:
				names.add(line.lower().replace('\n', '').replace('\r', '').replace(' ', ''))
	return names

def getFeinDictionary():
    feinDict = {}
    path = './'
    files = [f for f in listdir(path) if isfile(join(path, f)) and 'PrivateNonProfitEIN.csv' in f]
    for file in files:
        with open('./' + file, 'r') as csvfile:
            content = csvfile.readlines()
            for line in content:
                keys = line.split(',')
                if len(keys[2]) == 8:
                    keys[2] = '0' + keys[2]
                fein = keys[2]
                feinDict[fein] = { 'unitid': keys[0], 'institutionname': keys[1] }
    return feinDict


print 'getting files'
hocrPath = "./hocr"
hocrFiles = [f for f in listdir(hocrPath) if isfile(join(hocrPath, f)) and '.hocr' in f]

print 'getting names'
global nameSet
nameSet = getNamesSet()

print 'generating fein dictionary'
feinDict = getFeinDictionary()

# overRideList = ["020222120_2013_0b829fa9.hocr"]
overRideList = []

numFiles = len(hocrFiles)
filesProcessed = 0

print 'start processing'
if len(overRideList) == 0:
	for school in hocrFiles:
		print 'processing', school, '#', filesProcessed, 'of', numFiles
		filesProcessed += 1
		fein = school[:9]
		processForm('hocr/' + school, fein)
else:
	for school in overRideList:
		print 'processing', school
		fein = school[:9]
		processForm('hocr/' + school, fein)






