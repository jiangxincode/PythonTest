'''
*args：不定长位置参数，不仅可以普通的参数，还可以接收列表、元组等数据容器
**kwargs：不定长关键词参数，不可以接收普通的关键词参数，还可以接收字典容器
'''
def func(*args, **kwargs):
    print(args)  # 元组
    print(kwargs)  # 字典

# 1. 定义一个列表
list1 = [10, 20, 30]
# 2. 定义一个字典
dict2 = {"a":40, "b":50}

func(*list1, **dict2)  # 把list1传递给args参数，dict2传递给kwargs参数
