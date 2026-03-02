#coding=gbk
"""
@author:jiangxin
"""
a=['12','3','45','36','890','105']
b=[0,0,0,0,0,0,0,0,0,0]
c=[0,1,2,3,4,5,6,7,8,9]
for i in a:
    for j in i:
        b[int(j)] += 1
print dict(zip(c,b))
            
