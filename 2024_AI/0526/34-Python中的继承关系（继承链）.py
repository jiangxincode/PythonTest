'''
好奇：多继承中，到底继承谁的问题？
答：在Python中，有一个魔术变量方法mro()，可以表示类与类之间的继承关系（查看先继承谁？后继承谁的问题）
'''
class Father(object):
    def func(self):
        print('Father类中的func方法')

class Mother(object):
    def func(self):
        print('Mother类中的func方法')

class Child(Father, Mother):
    pass

print(Child.mro())

# 结论：在实际工作中，如果不清楚类与类之间的继承关系，我们可以使用"子类名称.mro()"方法来查看类与类之间的继承关系！