'''
__str__()作用：打印输出对象的信息
触发条件：当对象被打印时，会自动触发__str__()魔术方法
注意事项：__str__()方法只能返回"字符串"类型的数据
'''
class Student(object):
    # 1. 定义属性
    def __init__(self, name, age):
        self.name = name
        self.age = age

    # 2. 定义方法 => 只需要通过__str__()魔术方法
    # def print_object_info(self):
    #     print(f'我的名字叫做{self.name}，今年{self.age}岁了！')

    def __str__(self):
        return f'我的名字叫做{self.name}，今年{self.age}岁了！'


# 3. 实例化对象
s1 = Student('Tom', 23)
print(s1)  # 打印对象，相当于打印对象名称，返回对象在内存中的地址