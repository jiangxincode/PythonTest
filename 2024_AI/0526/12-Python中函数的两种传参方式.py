'''
调用函数时，传递参数的过程就称之为传参，在Python中，传参有两种方式：
① 位置参数 => 按照位置来实现参数传递
② 关键词参数 => 按照参数的名称来实现参数传递
'''
# 1. 位置传参
def func(name, age, address):
    print(name)
    print(age)
    print(address)

# 2. 传参 => 位置传参 => 按照参数的位置来实现值的传递
# func('Tom', 23, '北京市昌平区')

# 3. 传参 => 关键词传参 => 关键词就是参数的名称
func(name='Tom', address='北京市昌平区', age=23)