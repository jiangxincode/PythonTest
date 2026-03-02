#coding=gbk
"""
@author:jiangxin
"""
def is_prime(n):
    if n==1:
        return False
    elif n==2:
        return False
    else:
        while n>1:
            for i in range(2,n):
                if n%i==0:
                    return False
            return True

if __name__ == '__main__':
    m = input("Input the start num: ")
    n = input("Input the end num: ")
    if m%2==0:
        pass
    else:
        m += 1
    for i in range(m,n+1,2):
        for j in range(1,i):
            if is_prime(j) and is_prime(i-j):
                print str(i) + '=' + str(j) + '+' + str(i-j)
                break


