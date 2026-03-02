'''
带参数的lambda表达式
lambda 参数:返回值
'''
# 1. 普通参数
func1 = lambda a, b:a + b
print(func1(10, 20))  # 返回30

# 2. 默认值参数
func2 = lambda a, b, c=30 : a + b + c
print(func2(10, 20))  # 10 + 20 + 30

# 3. 不定长参数
func3 = lambda *args : args
print(func3(10, 20, 30))

func4 = lambda **kwargs : kwargs
print(func4(a=1,b=2,c=3))