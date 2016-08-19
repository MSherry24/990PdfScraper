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
				"Name and Title Average"]
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
		fieldNames = ['line1', 'line2', 'line3', 'key']
		out = csv.DictWriter(csvfile, fieldNames)
		out.writeheader()
		for person in people:
			out.writerow({
				'line1' : person['line1'],
				'line2' : person['line2'],
				'line3' : person['line3'],
				'key' : person['key']
			})
	

def processForm(filename):
	with open(filename, 'r') as myfile:
		data = myfile.read().replace('\n','')
	soup = bs4.BeautifulSoup(data)
	people = getSectionVIIPersonInfo(soup)
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

hocrPath = "./hocr"
hocrFiles = [f for f in listdir(hocrPath) if isfile(join(hocrPath, f)) and '.hocr' in f]

global nameSet
nameSet = getNamesSet()


for school in hocrFiles:
	processForm('hocr/' + school)






