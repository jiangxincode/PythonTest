#coding=gbk
'''
Created on 2014年7月16日

@author: jiangxin
'''
def fibonacci(n):
    fib_list = []
    i1=0
    i2=1
    i=0
    while i<n:
        fib_list.append(i1)
        i1,i2 = i2,i1+i2
        i+=1
    return fib_list

"""This is a test"""
print fibonacci(100)