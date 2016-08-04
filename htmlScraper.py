from lxml import html
import requests
from HTMLParser import HTMLParser
import bs4
import subprocess
from os import listdir
from os.path import isfile, join, dirname
import csv

def writeToFile(text):
	out.write(text.encode('utf-8').strip())

def listToString(list):
	return " ".join(list)

def person(line1, line2, line3):
	info = {}
	info['compensationD'] = ''
	info['compensationE'] = ''
	info['compensationF'] = ''
	line1split = line1.text.split(' ')
	line2split = line2.text.split(' ')
	info['name'] = listToString(line1split[:-3])
	info['title'] = line3.text
	info['line2'] = line2.text
	info['line1'] = line1.text
	if len(line2split) > 1:
		info['compensationD'] = line2split[1].replace(',','.')
	if len(line2split) > 2:
		info['compensationE'] = line2split[2].replace(',','.')
	if len(line2split) > 3:
		info['compensationF'] = line2split[3].replace(',','.')
	info['hours'] = listToString(line1split[-3:])
	return info

def printPerson(person):
	writeToFile(person['name'])
	writeToFile(',')
	writeToFile(person['title'])
	writeToFile(',')
	writeToFile(person['hours'].replace(' ', '.', 1))
	writeToFile(',')
	writeToFile(person['compensationD'])
	writeToFile(',')
	writeToFile(person['compensationE'])
	writeToFile(',')
	writeToFile(person['compensationF'])
	out.write('\n')

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

def writePeopleToFile(people):
	writeToFile('Name,Title,Hours,CompensationD,CompensationE,CompensationF')
	out.write("\n")
	for person in people:
		printPerson(person)

def processForm(filename):
	global out
	filepath = getCsvFilePath(filename)
	out = openFile(filepath.replace('.hocr', ''))
	__processForm(filename)
	closeFile(out)

def __processForm(filename):
	with open(filename, 'r') as myfile:
		data = myfile.read().replace('\n','')
	soup = bs4.BeautifulSoup(data)
	people = getSectionVIIPersonInfo(soup)
	writePeopleToFile(people)

def getCsvFilePath(filename):
	script_dir = dirname(__file__)
	rel_path = "csv/" + filename.replace('hocr/', '')
	return join(script_dir, rel_path)

def openFile(title):
	return open(title, "w")

def closeFile(file):
	file.close()

hocrPath = "./hocr"
hocrFiles = [f for f in listdir(hocrPath) if isfile(join(hocrPath, f)) and '.hocr' in f]
print hocrFiles

for school in hocrFiles:
	processForm('hocr/' + school)





