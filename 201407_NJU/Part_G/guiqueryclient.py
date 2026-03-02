import socket
import wx 
import sys
import threading
from wx.lib.pubsub import setupkwargs
from wx.lib.pubsub import pub as Publisher

def query_client(querystr):
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
        print recordstr
        wx.CallAfter(Publisher.sendMessage, "update", msg=recordstr)
        mySocket.send("OK")
        recordstr = mySocket.recv( 1024 )

    print "Connection terminated"
    mySocket.close()


class Frame1(wx.Frame):
    def __init__(self, superior):
        wx.Frame.__init__(self, parent=superior, title="Chat Server", pos= (100,200), size= (640,345))
        self.GUI_INIT()
        self.Centre()
        Publisher.subscribe(self.updateDisplay, "update")        

    def GUI_INIT(self):
        panel = wx.Panel(self)
        
        SendBtn = wx.Button(panel,label='SEND')
        QuitBtn = wx.Button(panel,label='Exit')
        self.ChatText = wx.TextCtrl(panel)
        self.ChatList = wx.ListBox(panel)

        hbox = wx.BoxSizer()
        hbox.Add(self.ChatText, proportion=1, flag=wx.EXPAND)
        hbox.Add(SendBtn, proportion=0, flag=wx.LEFT,border=5)
        hbox.Add(QuitBtn, proportion=0, flag=wx.LEFT,border=5)

        vbox=wx.BoxSizer(wx.VERTICAL)
        vbox.Add(hbox,proportion=0,flag=wx.EXPAND|wx.ALL,border=5)
        vbox.Add(self.ChatList,proportion=1,flag=wx.EXPAND|wx.LEFT|wx.BOTTOM|wx.RIGHT,border=5)

        panel.SetSizer(vbox)

        SendBtn.Bind(wx.EVT_BUTTON, self.OnSend)
        QuitBtn.Bind(wx.EVT_BUTTON,self.OnQuit)

    def OnSend(self,event):
        SendString = self.ChatText.GetValue()
        if str(SendString) == "":
            MsgBox = wx.MessageDialog(None,"Please give send content","warning",wx.OK)
            MsgBox.ShowModal()
            return

        querycli = threading.Thread(target=query_client, args=(SendString,),name='query_client thread')
        querycli.setDaemon(True)
        querycli.start()        
        
    def OnQuit(self,event):
        sys.exit()

    def updateDisplay(self,msg):
        self.ChatList.Append(msg)

if __name__ == '__main__':
    app =  wx.App( )   		
    frame=Frame1(None)     
    frame.Show(True)  		
    app.MainLoop( )   
