'''
案例：用于生成一个4位长度的验证码
① 必须要有一个字符串 => 包含数字 + 字母
② 程序循环抽取4个字符（必须在字符串中，且必须是随机抽取的）
③ 给这个函数要定义一个返回值，返回4位长度的验证码

注意：pass关键字，这个关键字的作用：代表占位符，用来占用某个位置，没有实际的意义
PyCharm快捷键 => Ctrl + Shift + U（实现大小写转换）
'''
# 导入一个随机模块
import random
def generate_code():
    # 1. 定义字符串
    str1 = '23456789abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ'
    # 2. 抽取4位长度的验证码，考虑循环抽取
    code = ''
    for i in range(4):
        # 3. 采用随机方式抽取验证码，字符对应的索引下标（字符串中的每一个字符，都有一个索引下标，默认从0开始）
        index = random.randint(0, len(str1)-1)  # index下标，不是真正的字符 => 真正的字符 str1[index]
        code += str1[index]  # 从字符串中抽取一个随机字符以后，放入code中
    # 4. 返回最终结果
    return code

# 调用函数，生成4位长度的验证码
print(generate_code())