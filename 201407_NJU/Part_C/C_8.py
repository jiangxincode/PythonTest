# coding=gbk
'''
Created on 2014年7月15日

@author: jiangxin
'''
list_name_origin = ['Tom', 'Mary', 'John', 'Mike', 'Julia', 'Mary', 'Tom', 'Mary']
print list_name_origin
set_name = set(list_name_origin)
print set_name

list_name = list(set_name)
print sorted(list_name)
for i in range(0,len(list_name_origin)):
    for j in range(i+1,len(list_name_origin)):
        #print i,j
        if list_name_origin[i]==list_name_origin[j]:
            set_name.discard(list_name_origin[i])

list_name = list(set_name)
print sorted(list_name)
