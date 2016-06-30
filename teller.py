#!/usr/bin/python
# coding=utf-8
import sys
import time
import sqlite3
import telepot
from pprint import pprint
from datetime import date, datetime
import re
import traceback
import manhwa_list

ROOT = '/root/git/manhwa-bot/'

def sendMessage(id, msg):
    try:
        bot.sendMessage(id, msg)
    except:
        print str(datetime.now()).split('.')[0]
        traceback.print_exc(file=sys.stdout)

def help(id):
    sendMessage(id, """<명령어>
 /list : 전체 만화 리스트 조회
 /sub 만화이름 : 원하는 만화를 구독
  ex. /sub 킹덤
 /sub : 자신의 구독 목록 조회
 /unsub 만화이름 : 구독해제

 주의!! 구독할때 만화이름을 /list상의 제목으로 정확하게 입력 안하면 동작 안 할 수 있습니다!
""")

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type != 'text':
        sendMessage(chat_id, '난 텍스트 이외의 메시지는 처리하지 못해요.')
        return
    #pprint(msg["from"])
    try:
        name = msg["from"]["last_name"] + msg["from"]["first_name"]
    except:
        name = ""

    text = msg['text'].lower()

    args = text.split(' ')
    if text.startswith('/'):
        if text.startswith('/list'):
            res=""
            cnt=0
            for title in manhwa_list.lists:
                res+= title + " - " + manhwa_list.lists[title] + "\n"
                cnt+=1
                if cnt>14:
                    cnt=0
                    sendMessage(chat_id, res)
                    res=""
            if res:
                sendMessage(chat_id, res)

        elif text.startswith('/sub'):
            conn = sqlite3.connect(ROOT+'subscribe.db')
            c = conn.cursor()
            c.execute('CREATE TABLE IF NOT EXISTS subscribe( user TEXT, title TEXT, name TEXT, PRIMARY KEY(user,title) )')
            conn.commit()

            if len(args)>1:
                title = args[1]
                try:
                    c.execute( 'INSERT INTO subscribe (user,title,name) VALUES ("%s", "%s", "%s")'%(chat_id,title,name) )
                except sqlite3.IntegrityError:
                    # means already inserted
                    sendMessage(chat_id, "동일한 신청목록이 존재하거나 제목오류 입니다.")
                else:
                    # means success
                    conn.commit()
                    sendMessage(chat_id, "성공적으로 추가되었습니다.")
            else:
                # subscribe list
                c.execute('SELECT * from subscribe WHERE user="%s"'%chat_id)
                res=""
                for data in c.fetchall():
                    res+=data[1]+","
                if res:
                    res=res[:-1]
                    sendMessage(chat_id, res)
                else:
                    sendMessage(chat_id, "조회 결과가 없습니다.")

        elif text.startswith('/unsub'):
            if len(args)>1:
                title = args[1]
                conn = sqlite3.connect(ROOT+'subscribe.db')
                c = conn.cursor()
                try:
                    c.execute( 'DELETE FROM subscribe WHERE user="%s" AND title="%s"'%(chat_id,title) )
                except sqlite3.IntegrityError:
                    # means already inserted
                    sendMessage(chat_id, "삭제가 실패했습니다.")
                else:
                    # means success
                    conn.commit()
                    sendMessage(chat_id, "성공적으로 삭제 되었습니다.")
            else:
                sendMessage(chat_id, "제목을 입력하세요.")
        elif text.startswith('/stat'):
            if chat_id=="68399557": #means me
                conn = sqlite3.connect(ROOT+'subscribe.db')
                c = conn.cursor()
                c.execute('SELECT count(*) from subscribe')
                sendMessage( chat_id, c.fetch() )
        else:
            help(chat_id)
    else:
        help(chat_id)


TOKEN = sys.argv[1]
print 'received token :', TOKEN

bot = telepot.Bot(TOKEN)
pprint( bot.getMe() )

bot.notifyOnMessage(handle)

print 'Listening...'

while 1:
    time.sleep(10)