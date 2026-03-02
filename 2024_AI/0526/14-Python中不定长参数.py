'''
在函数定义时，不确定调用时会传递多少个参数，这种情况，我们可以考虑使用不定长参数。
不定长位置参数 => *args => 接收位置参数的
不定长关键词参数 => **kwargs => 接收关键词参数的
'''
def func1(*args):
    print(args)
    print(type(args))

# 1. 不传参
func1()
# 2. 传递1个参数
func1(10)
# 3. 传递多个参数
func1(10, 20, 30, 40, 50)

# ------------------------------------------
def func2(**kwargs):
    print(kwargs)
    print(type(kwargs))

# 1. 不传参
func2()
# 2. 传递1个参数
func2(name='Tom')
# 3. 传递多个参数
func2(name='Tom', age=23, mobile='10086')