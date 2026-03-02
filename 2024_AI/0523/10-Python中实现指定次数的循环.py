'''
Python中的range()，专门用于生成一个数据容器。
range() => 返回结果类似列表 => [1, 2, 3]
基本语法
range(start, stop, step) ：只顾头来尾不管，包含start但是不包含stop
从start开始，到stop-1结束，每次前进step个步长
作用：实现指定次数的循环
'''
for i in range(5):  # 没有起始值，则起始值默认为0
    print(i)

print('-' * 80)  # 把-横岗复制80份

for i in range(1, 6):  # 1 ~ 5
    print(i)

print('-' * 80)  # 把-横岗复制80份

for i in range(1, 10, 2):  # 1 (1+2) (1+2+2) ...
    print(i)