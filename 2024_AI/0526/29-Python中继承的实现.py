'''
基本语法：
class 父类(object):
    # 公共属性
    # 公共方法

class 子类(父类):
    pass

子类对象 = 子类()
由子类产生的对象，自动继承父类中的公共属性与公共方法
'''
# 1. 定义一个父类
class Animal(object):
    # 2. 定义公共属性
    def __init__(self, name, age):
        self.name = name
        self.age = age

    # 3. 定义公共方法
    def eat(self):
        print('i can eat food!')

    def drink(self):
        print('i can drink water!')

# 4. 定义一个子类
class Dog(Animal):
    pass

# 5. 实例化子类对象
dog = Dog('史努比', 6)
print(dog.name)
print(dog.age)

dog.eat()
dog.drink()