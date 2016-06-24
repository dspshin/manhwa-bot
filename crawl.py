# -*- coding: utf-8 -*-

import sys, re, time, traceback
import pprint
import parsers

def getParser(url):
	# get proper parser 
	if url.find("onenable.net")>-1:
		return parsers.onenable 

	print "No proper parsers for", url
	return None

def getNewArticles(url):
	parser = getParser(url)
	if parser:
		articles = parser(url)
		# need to filter new articles

		return articles

	return []

def crawl(lists):
	for i in lists:
		articles = getNewArticles(lists[i])

		for article in articles:
			pprint.pprint(article)
			# send messages to subscribing users

if __name__ == "__main__":

	lists = {
		"킹덤":"http://onenable.net/bbs/board.php?bo_table=toonia14"
	}
	#pprint.pprint(lists)

	crawl( lists )


