#coding=gbk
'''
Created on 2014年7月16日

@author: jiangxin
用 reduce()进行函数式编程以及递归。
(a)用一分钟写个带 x,y并返回他们乘积的名为 mult(x,y)的简单小巧函数。
(b)用你在 a中创建的 mult()函数以及 reduce来计算阶乘。
(c)彻底抛弃掉 mult()的使用 。用 lamda表达式替代。
(d)我们描绘了一个递归解决方案来找到 N!
'''
def mult(x,y):
    return x*y

def factorial1(n):
    return reduce(mult,range(1,n+1))

def factorial2(n):
    return reduce((lambda x,y:x*y),range(1,n+1))

def factorial3(n):
    if n==1:
        return 1
    else:
        return n*factorial3(n-1)


"""This is a test"""
print mult(12, 13)
print factorial1(10)
print factorial2(10)
print factorial3(10)

