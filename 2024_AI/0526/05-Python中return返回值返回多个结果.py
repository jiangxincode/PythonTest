'''
在他的编程语言中，return返回值一次只能返回一个结果，但是在Python中比较特殊：可以同时返回多个结果
'''
def func():
    return 1, 2, 3

# 调用func()函数
print(func())
print(type(func()))

'''
[1, 2, 3] ：列表
(1, 2, 3) ：元组
{1, 2, 3} ：集合
'''