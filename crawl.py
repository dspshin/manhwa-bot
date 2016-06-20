# -*- coding: euc-kr -*-

import urllib2, sys, re, time, traceback
from bs4 import BeautifulSoup

if __name__ == "__main__":
	
	url = "http://onenable.net/bbs/board.php?bo_table=toonia14"

	req = urllib2.Request( url )
	response = urllib2.urlopen(req)
	contents = response.read()

	soup = BeautifulSoup(contents, 'html.parser')

	#articles = soup.find_all("td", class_="list-subject")
	#for article in articles:
	#	print article.a

	articles = soup.select("td.list-subject a")
	for article in articles:
		print article.attrs["href"]
		print article.text
		break