#coding=gbk
'''
Created on 2014年7月16日

@author: jiangxin
首先产生一个随机数序列，然后过滤（利用filter()函数)掉所有的偶数
'''
from random import randint

def is_odd(n):
    return n%2

numbers = []
for each in range(100):
    numbers.append(randint(1,99))
print filter(is_odd, numbers)
