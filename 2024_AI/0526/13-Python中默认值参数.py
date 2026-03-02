'''
在函数中，可以为某些参数定义默认值，这种参数就称之为默认值参数
注意：name，age称之为普通参数，gender默认值参数，在实际应用中，默认值参数必须要放在普通参数的右侧
'''
def func(name, age, gender='male'):
    print(name)
    print(age)
    print(gender)

# 1. 默认值参数在传参中可以不传递参数，则这个参数的值就是默认值
# func('Tom', 23)

# 2. 默认值传递在传参中也可以传递参数，则传递的参数会自动覆盖默认值
func('Rose', 22, 'female')