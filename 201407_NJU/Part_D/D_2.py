#coding=gbk
'''
Created on 2014年7月15日

@author: jiangxin
'''
import os
f_source = open('./test_D_2_source.py','r+')
f_result = open('./test_D_2_result.py','w')

for everyline in f_source:
    if everyline.find("#") != -1:
        #print everyline
        index_comment = everyline.index('#')
        everyline = everyline[:index_comment]+os.linesep
        #print everyline
    else:
        pass
    f_result.write(everyline)
        