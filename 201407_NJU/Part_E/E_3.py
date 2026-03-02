#coding=gbk
'''
Created on 2014年7月16日

@author: jiangxin
'''
def min2(obj_one,obj_two):
    if obj_one <= obj_two:
        return obj_one
    else:
        return obj_two

def max2(obj_one,obj_two):
    if obj_one >= obj_two:
        return obj_one
    else:
        return obj_two
    
"""This is a test"""
print max2(4,8)
print min2(4,8)