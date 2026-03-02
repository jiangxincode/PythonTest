'''
在其他编程语言中，不仅有构造函数，还有析构函数。
构造函数：类实例化产生对象时触发
析构函数：当对象被删除或销毁时会自动触发
在Python代码中，也可以通过__del__()魔术方法来实现析构函数的操作
主要作用：负责程序的收尾工作
'''
class Person(object):
    # 1. 定义属性
    def __init__(self, name, age):
        self.name = name
        self.age = age
    # 2. 定义方法
    def eat(self):
        print('i can eat food!')
    # 3. 析构方法
    def __del__(self):
        print('当对象被删除或销毁时会自动被触发')

# 4. 实例化对象 => 构造方法
p1 = Person('小明', 23)
print(p1.name)
print(p1.age)
p1.eat()

# 5. 删除对象 => 自动触发__del__魔术方法
# del p1