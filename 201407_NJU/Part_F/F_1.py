#coding=gbk
'''
Created on 2014年7月16日

@author: jiangxin
'''

class Point():
    """A class related point"""
    
    def __init__(self,x=0,y=0):
        """The init function"""
        self.X = x
        self.Y = y
        
    def output(self):
        """Print the point coordinate with the way of(x,y)"""
        print 'The coordinate is: %d,%d' % (self.X,self.Y)
    
    def get_X(self):
        """Get the x-coordinate"""
        return self.X
    
    def get_Y(self):
        """Get the y-coordinate"""
        return self.X

def test():    
    """This is a test"""
    point1 = Point()
    point1.output()
    print point1.get_X()

    point2 = Point(2,3)
    point2.output()
    print point2.get_Y()

if __name__ == '__main__':
    test()