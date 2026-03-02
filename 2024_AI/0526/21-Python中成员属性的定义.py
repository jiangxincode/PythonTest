'''
对象是由两部分内容组成的：属性（变量，对象自身特征） + 方法（函数）

对象.属性 = 属性值
'''
class Student(object):
    # 获取对象属性
    def get_attr(self):
        print(self.name, self.age)

# 1. 实例化对象
stu1 = Student()
# 2. 为其添加属性
stu1.name = 'Tom'
stu1.age = 23
# 3. 获取属性
# print(stu1.name)
# print(stu1.age)
stu1.get_attr()

# 4. 每定义一个对象，都需要添加属性
stu2 = Student()
stu2.name = 'Rose'
stu2.age = 24

# print(stu2.name)
# print(stu2.age)
stu2.get_attr()