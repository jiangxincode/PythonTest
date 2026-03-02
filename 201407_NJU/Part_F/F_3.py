# coding=gbk
'''
Created on 2014年7月16日

@author: jiangxin
'''

import math

class MoneyFmt():
    
    def __init__(self, value):
        self.value = value
        
    def update(self, value):
        self.value = value
        
    def __nonzero__(self):
        if self.value == 0:
            return False
        else:
            return True
        
    def __repr__(self):
        print self.value
        
    def __str__(self):
        
        result = ''
        
        if(self.value < 0):
            result = '-'
            
        result += '$'
        
        value = math.fabs(self.value)
        value = round(value,2)
        str_value = format(value,',')
        
        if (value*10)%1==0:
            str_value += '0'
        
        print result+str_value

def test():
    """This is a test"""
    money = MoneyFmt(3478.7)
    money.__str__()
    money.update(-123473.983)
    money.__str__()
    
#test()
