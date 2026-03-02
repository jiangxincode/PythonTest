# 1. 定义一个class类
class Student(object):
    # 属性 => 变量
    # 方法 => 函数
    def eat(self):
        print('i can eat food!')

    def drink(self):
        print('i can drink water!')

# 2. 实例化学生对象 => 一个类可以生成多个对象
stu1 = Student()
print(stu1)

stu2 = Student()
print(stu2)

# 3. 调用eat与drink方法
stu1.eat()
stu1.drink()

stu2.eat()
stu2.drink()