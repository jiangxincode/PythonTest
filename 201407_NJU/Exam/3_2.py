#coding=gbk
"""
@authon jiangxin
"""
movies = ["The Holy Grail",1975,"Terry Jones & Terry Gilliam",91,["Graham Chapman",["Michael Palin","john Cleese","Terry Gilliam","Eric Idle", "Terry Jones"]]]

def print_list(my_list):
    for i in my_list:
        if type(i)==type([]):
            print_list(i)
        else:
            print i
            
if __name__ == '__main__':
    print_list(movies)
