'''
和其他编程语言（如Java）有所不同，Java只支持单继承，但是Python是少有支持多继承的编程语言。
什么是多继承？
所谓的多继承就是一个类可以同时继承自多个父类
class A(object):
    pass
class B(object):
    pass

class C(A, B):
    pass
子类C会自动继承A以及B中的所有公共属性和公共方法
'''
class Father(object):
    # 定义公共方法
    def func1(self):
        print('我是Father类中的func1方法！')

class Mother(object):
    # 定义一个公共方法
    def func2(self):
        print('我是Mother类中的func2方法！')

class Child(Father, Mother):
    pass

child = Child()
child.func1()
child.func2()