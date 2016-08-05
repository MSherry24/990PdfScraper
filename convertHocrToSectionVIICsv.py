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

def listToString(list):
	return " ".join(list)

def person(line1, line2, line3):
	info = {}
	info['line1'] = encodeUtf8(line1.text)
	info['line2'] = encodeUtf8(line2.text)
	info['line3'] = encodeUtf8(line3.text)
	return info

def getSectionVIIPersonInfo(tree):
	people = []
	pages = tree.select('.ocr_page')
	for page in pages:
		if pageIsPartVII(page):
			peopleOnPage = lookForPeoplOnPage(page)
			people = people + peopleOnPage
	return people

def pageIsPartVII(page):
	keywords = ["Part VII - Compensation"]
	return blobContainsListValue(page, keywords)

def lookForPeoplOnPage(page):
	people = []
	paragraphs = page.select('.ocr_par')
	for paragraph in paragraphs:
		if paragraphContainsPersonInformation(paragraph):
			foundPeople = findPeopleFromParagraph(paragraph)
			people = people + foundPeople
	return people

def paragraphContainsPersonInformation(paragraph):
	keywords = ["dotted line", "organizations a"]
	return blobContainsListValue(paragraph, keywords)

def findPeopleFromParagraph(paragraph):
	people = []
	processedIndicies = set([])
	lines = paragraph.select('.ocr_line')
	lineLength = len(lines)
	for index, line in enumerate(lines):
		if foundPrefix(line) and (index + 2) < lineLength:
			people.append(person(lines[index], lines[index + 1], lines[index + 2]))
			processedIndicies.add(index)
		if foundTitle(line) and (index - 2) not in processedIndicies:
			people.append(person(lines[index-2], lines[index - 1], lines[index]))
			processedIndicies.add(index - 2)
	return people

def foundPrefix(line):
	prefixes = ['Mr', 'Dr', 'Ms', 'Rev', 'Hon']
	return blobContainsListValue(line, prefixes)

def foundTitle(line):
	titles = ['Trustee', 'President', 'CEO', 'Chairman', 'Chair', 'Vice', 'VP', 'Provost', 'Dir', 'Dean', 'Coach', 'Profesor']
	return blobContainsListValue(line, titles)

def blobContainsListValue(blob, listOfStrings):
	if any (x.lower() in blob.text.lower() for x in listOfStrings):
		return True
	return False

def writePeopleToFile(people, filename):
	with open(getCsvFilePath(filename), "w") as csvfile:
		fieldNames = ['line1', 'line2', 'line3']
		out = csv.DictWriter(csvfile, fieldNames)
		out.writeheader()
		for person in people:
			out.writerow({
				'line1' : person['line1'],
				'line2' : person['line2'],
				'line3' : person['line3']
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


hocrPath = "./hocr"
hocrFiles = [f for f in listdir(hocrPath) if isfile(join(hocrPath, f)) and '.hocr' in f]
print hocrFiles

for school in hocrFiles:
	processForm('hocr/' + school)





