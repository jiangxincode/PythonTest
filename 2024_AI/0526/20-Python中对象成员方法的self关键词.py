'''
在类的内部，有两个内容：成员属性 与 成员方法
基本语法
class 类名(object):
    属性
    def func1(self):
        self...

    def func2(self)
        self...
探讨self关键词所表示含义？
'''
# 1. 定义一个学生类
class Student(object):
    # 2. 定义成员方法
    def eat(self):
        print(self)  # 打印self关键词
        return None

# 2. 实例化学生对象
stu1 = Student()
print(stu1)  # 显示对象在内存中的地址
stu1.eat()

# 结论：self关键词指向实例化对象（谁实例化了这个类，则成员方法中的self就指向谁）