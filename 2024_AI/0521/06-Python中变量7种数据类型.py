'''
python中变量的数据类型：
① 数值类型
整数类型 => int类型，10、20、30
浮点类型 => float类型，9.88、6.77
② 字符串类型 => str类型，'hello'、"python"
③ 布尔类型 => bool类型，只有两个值：True（真）、False（假）
--------------------------------------------------
④ 列表类型 => list类型，[10, 20, 30]，里面的数据可以支持增删改查操作
⑤ 元组类型 => tuple类型，(10, 20, 30)，一旦写入成功，就不能修改和删除了
⑥ 字典类型 => dict类型，{'name':'Tom', 'age':23, 'address':'深圳市宝安区'}
⑦ 集合类型 => set类型，天生去重，{10, 20, 30, 20} => 打印时，只有{10, 20, 30}

使用type()判断变量的数据类型
'''
a = 10
print(type(a))

b = 9.88
print(type(b))

c = 'hello'
print(type(c))

d = True
print(type(d))

f = [10, 20, 30]
print(type(f))

g = (10, 20, 30)
print(type(g))

h = {'name':'tom', 'age':23, 'mobile':'10086'}
print(type(h))

i = {10, 20, 30, 20, 30}
print(i)
print(type(i))