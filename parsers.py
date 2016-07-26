# -*- coding: utf-8 -*-

import urllib2, sys, re, time, traceback
from bs4 import BeautifulSoup

def onenable(url):
	req = urllib2.Request( url )
	response = urllib2.urlopen(req)
	contents = response.read()

	soup = BeautifulSoup(contents, 'html.parser')

	#articles = soup.find_all("td", class_="list-subject")
	#for article in articles:
	#	print article.a

	articles = soup.select("td.list-subject a")
	res = []
	for article in articles:
		res.append({
			"url": article.attrs["href"],
			"title": article.text.strip().split("\t")[0]
		})
	return res

def naver(url):
	req = urllib2.Request( url )
	response = urllib2.urlopen(req)
	contents = response.read()

	soup = BeautifulSoup(contents, 'html.parser')

	res=[]
	articles = soup.select("td.title a")
	for a in articles:
		a_url = "http://comic.naver.com"+a.attrs["href"]
		# &weekday= 부분 제거
		weekday = a_url.find('&weekday')
		if weekday>-1:
			a_url = a_url[:weekday]
		res.append({
			"url": a_url,
			"title": a.text.strip()
		})
	return res