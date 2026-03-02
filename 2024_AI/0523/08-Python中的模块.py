'''
什么是模块？
模块的本质是一个Python文件，模块有两种：① 系统模块 ② 自定义模块
系统模块就是官方提前开发好的Python功能代码
自定义模块就是我们根据业务的需要，自己开发的Python功能代码
有一个系统模块叫做：random（随机模块，作用：生成一个随机数）

模块导入：
① import 模块名称
模块名称.方法名()

② from 模块名称 import 方法名（推荐）
方法名()
'''
# import random
# print(random.randint(1, 3))

from random import randint
print(randint(1, 3))