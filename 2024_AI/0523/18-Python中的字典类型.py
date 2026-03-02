'''
字典也是一种比较常见的数据类型，支持增删改查操作
作用：在实际工作中，主要用于保存某个事物的信息，比如一个人，一个学生，一本书等等
基本语法
字典名称 = {key:value, key:value, key:value}
'''
# 定义一个空字典
dict1 = {}
dict2 = {'name':'Tom', 'age':23, 'mobile':'10086'}

print(dict1)
print(dict2)
print(type(dict2))  # dict

# 1. 增加元素/修改元素
dict1['name'] = 'Jack'  # 添加操作 => {'name':'Jack'}，如果字典中没有这个key，则这个就是添加操作
dict1['name'] = 'Rose'  # 修改操作 => 如果字典中已经存在了这个key，则这个就是修改操作

# 2. 删除与清空
# del dict2['age']  # 删除dict2中的'age':23
# print(dict2)

# 清空
# dict2.clear()
# print(dict2)

# 3. 查询
print(dict2['name'])
print(dict2['age'])
print(dict2['mobile'])