from urllib2 import urlopen, URLError, HTTPError
from bs4 import BeautifulSoup
import os

def downloadFile(url):
    # Open the url
    try:
        f = urlopen(url)
        print "downloading " + url

        # Open our local file for writing
        with open('pdf/' + os.path.basename(url), "wb") as local_file:
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


eins = ["390806251"]
for ein in eins:
	soup = getPageHtml(ein)
	for link in soup.find_all('a'):
		if '_2013_' in link.get('href'):
			downloadFile(link.get('href'))