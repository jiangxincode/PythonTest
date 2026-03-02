'''
在Python中，不仅有公共属性，还有公共方法；同样，不仅有私有属性，也有私有方法。
在class类中，通过__修饰的方法就是私有方法
'''
class Person(object):
    # 公共属性
    def __init__(self, name, age):
        self.name = name
        self.age = age

    # 公共方法
    def eat(self):
        print('i can eat food!')

    # 私有方法
    def __func(self):
        print('我是Person类中的私有方法!')

# 实例化Person类
p1 = Person('Tom', 23)
p1.eat()
p1.__func()
