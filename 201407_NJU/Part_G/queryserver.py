#coding=gbk
'''
Created on 2014年7月17日

@author: Administrator
'''

import socket
import sqlite3

def QueryDataBase(condition):
    conn = sqlite3.connect('food.db')
    curs = conn.cursor()
    query = 'SELECT * FROM food WHERE %s' % condition
    curs.execute(query)
    res = []
    for row in curs.fetchall():
        itemstr = ''
        for x in row[:6]:
            itemstr = itemstr + ' ' + str(x)
        res.append(itemstr)

    conn.close()
    return res

HOST = 'localhost'
PORT = 5003
ADDR = (HOST,PORT)
BUFSIZE = 1024

SerSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

SerSocket.bind(ADDR)

SerSocket.listen(1)

while True:
    print "Waiting for connection..."
    transconn, cliaddr = SerSocket.accept()
    print "connection from:", cliaddr

    data = transconn.recv(BUFSIZE)
    print data
    if not data:
        transconn.close()
        print 'client error...'
        key = raw_input('continue?(Y/N):')
        if key == 'N' or key == 'n':
            break
        else :
            pass

    recordlist = QueryDataBase(data)
    for rec in recordlist:
        transconn.send(rec)
        transconn.recv(BUFSIZE)

    print 'total %d transferd...\n' % len(recordlist)

    transconn.send('TERMINATE')
    transconn.close()

    print 'client over...'
    key = raw_input('continue?(Y/N):')
    if key == 'N' or key == 'n':
        break
    else :
        pass   


SerSocket.close()


