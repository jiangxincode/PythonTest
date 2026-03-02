'''
__call__()魔术方法：作用，当对象被调用时，对象 + ()，会自动被触发
'''
class Adder(object):
    # 1. 定义属性
    def __init__(self, value=0):
        self.data = value
    # 2. 定义方法
    def __call__(self, x):
        self.data += x

# 3. 实例化类
add = Adder()
# 4. 调用add对象
add(1)
add(2)
add(3)
print(add.data)