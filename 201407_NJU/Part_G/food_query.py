#coding=gbk
'''
Created on 2014年7月17日

@author: Administrator
'''
import sqlite3
import sys
conn = sqlite3.connect('food.db')
curs = conn.cursor()
query = 'select * from food where %s' % (sys.argv[1])
curs.execute(query)
column_name = [des[0] for des in curs.description]
for row in curs.fetchall():
    for pair in zip(column_name,row):
        print("%s:%s" % pair)
    print
