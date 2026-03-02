'''
在其他编程语言中，属性一般分为三种情况：① 公有属性 ② 受保护属性 ③ 私有属性
在Python编程语言中，只有公有属性 和 私有属性
通过__init__魔术方法定义或者通过对象.属性定义的都是公有属性
在类的内部，通过__修饰的属性，如self.__属性就是私有属性，私有属性只能在类的内部使用，无法在类的外部使用
'''
# 1. 定义一个Girl类
class Girl(object):
    # 2. 定义属性（公有 + 私有）
    def __init__(self, name):
        self.name = name  # 属性就是公有属性
        self.__age = 18  # 私有属性

    # 3. 封装专门用于设置或获取私有属性的公共方法（接口）
    def get_age(self):
        # 更高级一些：我们可以针对用户请求添加一些限制
        # 添加一个权限控制，判断用户是否有私有属性的访问权限
        return self.__age

# 3. 实例化对象
girl = Girl('小美')
print(girl.name)

# 4. 尝试在类的外部访问私有属性
# print(girl.__age)
print(girl.get_age())