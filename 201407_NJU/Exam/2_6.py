#coding=gbk
"""
@author:jiangxin
"""
class MyClass():
    def __init__(self,tea_name):
        self.tea_name = tea_name
        self.stu_list = []

    def add(self,stu_name):
        self.stu_list.append(stu_name)

    def remove(self,stu_name):
        self.stu_list.remove(stu_name)
        
    def print_all(self):
        print self.tea_name
        if self.stu_list != []:
            print self.stu_list

if __name__ == '__main__':
    myclass = MyClass('Teacher Wang')
    print 'Before add students:'
    myclass.print_all()
    
    myclass.add('LiMing')
    myclass.add('XiaoHong')
    print 'After add students:LiMing,XiaoHong:'
    myclass.print_all()

    myclass.remove('LiMing')
    print 'After remove students:LiMing:'
    myclass.print_all()
