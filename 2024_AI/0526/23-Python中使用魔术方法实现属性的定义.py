'''
在实际工作中，属性往往都是通过__init__()魔术方法来进行定义的
'''
# 1. 定义一个学生类
class Student(object):
    # 2. 定义属性
    def __init__(self, name, age):  # 用于接收对象属性值
        self.name = name
        self.age = age

    # 3. 定义方法
    def eat(self):
        print('i can eat food')

    def drink(self):
        print('i can drink water')

# 4. 实例化对象
s1 = Student('Tom', 23)
print(s1.name)
print(s1.age)

s2 = Student('Rose', 22)
print(s2.name)
print(s2.age)