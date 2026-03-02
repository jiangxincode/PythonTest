#coding=gbk
'''
Created on 2014年7月17日

@author: Administrator
'''
import socket
import sys

def query_client(querystr,resfile):

    fh = open(resfile,'w')
    
    HOST = "127.0.0.1"
    PORT = 5003

    print "Attempting connection"
    mySocket = socket.socket( socket.AF_INET, socket.SOCK_STREAM )

    try:
        mySocket.connect( ( HOST, PORT ) )
    except socket.error:
        print "Call to connect failed"
        return None

    print "Connected to Server"

    mySocket.send(querystr)
    recordstr = mySocket.recv( 1024 )

    while recordstr != "TERMINATE":
        if not recordstr:
            break
        recordstr = recordstr+'\n'
        print recordstr
        fh.write(recordstr)
        mySocket.send("OK")
        recordstr = mySocket.recv( 1024 )

    print "Connection terminated"
    mySocket.close()
    fh.close()

if __name__ == '__main__':

    query_client(sys.argv[1],sys.argv[2])
