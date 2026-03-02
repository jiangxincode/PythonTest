'''
在Python代码中，我们可以使用input()方法来接收外部设备的输入
基本语法：
变量名称 = input('给用户的提示信息')   含义：把外部设备的输入信息保存在变量中

注意事项：① input()接收到的所有数据类型都是字符串 ② input()具有阻塞代码能力
'''
# 1. 提示用户输入6位的交易密码
password = int(input('请输入您的6位银行卡密码：'))
# 2. print()对其进行打印输出
print(password)
print(type(password))

# 3. 问题：如何把字符串转化为数字类型
# int()：把其他类型转int整数
# float()：把其他类型转float浮点类型
# str()：把其他类型转str字符串类型