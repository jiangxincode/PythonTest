#coding=gbk
'''
Created on 2014年7月16日

@author: jiangxin
'''
import sys
import os

print(len(sys.argv))
print(sys.argv)
expression = sys.argv[1]
print(expression)

operand1 = ''
operand2 = ''

for i in expression:
    if i.isdigit():
        operand1 = operand1+i
    else:
        operator = i
        break

index_operator = expression.index(operator)
expression = expression[index_operator+1:]


for i in expression:
    if i.isdigit():
        operand2 = operand2+i

operand1 = int(operand1)
operand2 = int(operand2)

print(operand1,operator,operand2)
if(operator == '+'):
    result = operand1+operand2
elif(operator == '-'):
    result = operand1-operand2
print(result)
f_result = open('./test_D_3_result.py','w')
f_result.write(str(operand1) + operator + str(operand1) + '=' + str(result)+os.linesep)