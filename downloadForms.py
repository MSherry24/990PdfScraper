from urllib2 import urlopen, URLError, HTTPError
from bs4 import BeautifulSoup
from os import listdir
from os.path import isfile, join, dirname, basename

def downloadFile(url):
    # Open the url
    try:
        f = urlopen(url)
        print "downloading " + url

        # Open our local file for writing
        with open('pdf/' + basename(url), "wb") as local_file:
            local_file.write(f.read())

    #handle errors
    except HTTPError, e:
        print "HTTP Error:", e.code, url
    except URLError, e:
        print "URL Error:", e.reason, url

def getPageHtml(ein):
	url = "http://www.eri-nonprofit-salaries.com/index.cfm?FuseAction=NPO.Summary&EIN=" + ein + "&BMF=1&Cobrandid=0&Syndicate=No"
	page = urlopen(url).read()
	return BeautifulSoup(page, 'html.parser')

def getEins():
    eins = set([])
    path = './'
    files = [f for f in listdir(path) if isfile(join(path, f)) and 'PrivateNonProfitEIN.csv' in f]
    for file in files:
        with open('./' + file, 'r') as csvfile:
            content = csvfile.readlines()
            for line in content:
                keys = line.split(',')
                if len(keys[2]) == 8:
                    keys[2] = '0' + keys[2]
                eins.add(keys[2])
    return eins

eins = getEins()
fileCount = 0
einCount = len(eins)
for ein in eins:
    soup = getPageHtml(ein)
    for link in soup.find_all('a'):
        if '_2013_' in link.get('href'):
            fileCount += 1
            print 'downloading', ein, '#', fileCount, 'of', einCount
            downloadFile(link.get('href'))

