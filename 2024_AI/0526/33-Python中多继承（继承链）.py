'''
问题：如果子类中同时继承了多个父类，而且父类中拥有相同的属性或方法，会报错么？如果不报错，使用哪个父类中的属性或方法
'''
class Father(object):
    def func(self):
        print('我是Father父类中的func方法')

class Mother(object):
    def func(self):
        print('我是Mother父类中的func方法')

class Child(Father, Mother):
    pass

# 实例化子类
child = Child()
child.func()