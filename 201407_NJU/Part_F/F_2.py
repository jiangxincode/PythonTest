#coding=gbk
'''
Created on 2014年7月16日

@author: jiangxin
'''
import math
from F_1 import Point

class Line(Point):
    def __init__(self,p1_x=0,p1_y=0,p2_x=0,p2_y=0):
        self.p1 = Point(p1_x,p1_y)
        self.p2 = Point(p2_x,p2_y)
        
    def __repr__(self):
        return '((%f,%f)(%f,%f))' % (self.p1.X,self.p1.Y,self.p2.X,self.p2.Y)
        
    def length(self):
        return math.sqrt((self.p1.X-self.p2.X)**2+(self.p1.Y-self.p2.Y)**2)
    
    def gradient(self):
        return (self.p2.Y-self.p1.X)/float(self.p2.X-self.p1.X)
    
def test():
    """This is a test"""
    line1 = Line(4,5,9,12)
    print line1.__repr__()
    print line1.length()
    print line1.gradient()

if __name__ == '__main__':    
    test()