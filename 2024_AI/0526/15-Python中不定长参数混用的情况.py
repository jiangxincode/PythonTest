'''
在定义函数时，如果不确定传参时有多少个参数，也不确定调用时的传参类型，可以考虑把*args与**kwargs一起使用
'''
def func(*args, **kwargs):
    print(args)
    print(kwargs)

# 以上代码的写法有一个好处，既可以接收不定长的位置参数，也可以接收关键词参数
func(1, 2, 3, a=4, b=5)