#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, re, time, traceback
from pprint import pprint
import parsers
import manhwa_list
import sqlite3
import telepot
from datetime import date, datetime, timedelta

ROOT = '/root/git/manhwa-bot/'

conn2 = sqlite3.connect(ROOT+'logs.db')
c2 = conn2.cursor()
c2.execute('CREATE TABLE IF NOT EXISTS logs( url TEXT, PRIMARY KEY(url) )')
conn2.commit()

conn = sqlite3.connect(ROOT+'subscribe.db')
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS subscribe( user TEXT, title TEXT, name TEXT, PRIMARY KEY(user,title) )')
conn.commit()

def sendMessage(user,msg):
	try:
		bot.sendMessage(user,msg)
	except:
		traceback.print_exc(file=sys.stdout)

def getParser(url):
	# get proper parser
	if url.find("onenable.net")>-1:
		return parsers.onenable
	elif url.find("comic.naver.com")>-1:
		return parsers.naver

	print "No proper parsers for", url
	return None

def getNewArticles(url):
	parser = getParser(url)
	if parser:
		articles = parser(url)
		# need to filter new articles
		filtered = []
		for article in articles:
			try:
				c2.execute('INSERT INTO logs (url) VALUES ("%s")'%(article["url"]))
			except sqlite3.IntegrityError:
				# means already sent
				pass
			else:
				# means new
				filtered.append( article )
		conn2.commit()
		return filtered
	return []

def crawl(lists):
	for title in lists:
		#print title, lists[title]
		articles = getNewArticles(lists[title])

		users = []
		c.execute('SELECT user FROM subscribe WHERE title="'+title+'"') # get subscribing users
		for data in c.fetchall():
			users.append( data[0] )

		for article in articles:
			pprint(article)
			# send messages to subscribing users
			msg = article["title"] +" "+ article["url"]
			#print msg

			for user in users:
				sendMessage( user, msg )

		print 'sent to', len(users)
		#delay
		time.sleep(2)

today = date.today()
now=datetime.now()

TOKEN = sys.argv[1]
print '[',now,']received token :', TOKEN

bot = telepot.Bot(TOKEN)
pprint( bot.getMe() )

crawl( manhwa_list.lists )


