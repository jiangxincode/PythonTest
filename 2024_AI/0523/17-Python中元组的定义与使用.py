'''
列表支持增删改查
元组一旦定义，其就不能修改和删除了，作为系统变量或者用于保护数据
基本语法
tuple1 = (10, )  如果元组中只有一个元素，必须要保留逗号
tuple2 = (10, 20, 30)
'''
tuple1 = (10,)
print(tuple1)
print(type(tuple1))

tuple2 = (10, 20, 30)
print(tuple2)
print(type(tuple2))

print(tuple2[0])
print(tuple2[1])
print(tuple2[2])

for i in tuple2:
    print(i)

# 不能修改也不能删除，否则报错
# tuple2[2] = 40
# del tuple2[1]  # del，用于删除容器中的元素
