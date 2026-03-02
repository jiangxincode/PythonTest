'''
所谓的容器就是一个变量中，可以同时保存多份数据 => 容器
字符串、列表、元组、字典、集合
列表元素，每个元素都有一个下标，第一个元素下标为0， 第二个元素下标为1，依次类推
'''
# 1. 定义列表
list1 = ['刘备', '关羽']
print(list1)
print(type(list1))

# 2. 增加数据 => append()，在列表尾部追加元素
list1.append('张飞')
print(list1)

# 3. 删除数据 => remove()方法
list1.remove('刘备')
print(list1)  # 关羽和张飞

# 4. 修改数据 => 把关羽更改为关平
list1[0] = '关平'
print(list1)

# 5. 查询数据 => 可以根据索引显示、也可以通过for循环遍历
print(list1[0])
print(list1[1])

for i in list1:
    print(i)