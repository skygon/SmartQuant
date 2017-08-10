import os
import sys
sys.path.append(os.getcwd())
import itchat
from itchat.content import *
from utils import *
import threading
import time

# filehelper
# skygon: @cefaa7f2ca6905f870a3e54147f46f6f
#CLIENT_NAME = "filehelper"
CLIENT_NAME = "skygon"

class Pusher(threading.Thread):
    def __init__(self, conf):
        threading.Thread.__init__(self)
        self.conf = conf
    
    def handlePriceMsg(self):
        #msg = ':'.join(self.data)
        msg = None
        code = self.data[1]
        price = float(self.data[2])
        if price < self.conf[code]['low']:
            msg = "[LOW] " + code + "--> " + str(price)
        elif price > self.conf[code]['high']:
            msg = "[HIGH] " + code + "--> " + str(price)
        
        return msg
    
    #crash:code
    def handleCrashMsg(self):
        try:
            code = self.data[1]
            msg = "CRASH --> [%s]" %(code)
            return msg
        except Exception, e:
            msg = "handleCrashMsg failed"
            return msg
        

    def parseMessage(self, data):
        self.data = data.split(':')
        msg = None
        if self.data[0] == 'price':
            msg = self.handlePriceMsg()
        if self.data[0] == 'crash':
            msg = self.handleCrashMsg()
        if self.data[0] == 'test':
            return self.data[1]
        
        return msg

    def run(self):
        itchat.auto_login(True)
        author = itchat.search_friends(nickName='skygon')[0]
        author.send('greeting !')
        #itchat.send_msg("hello world", CLIENT_NAME)
        while True:
            try:
                item = g_utils.msg_queue.get()
                msg = self.parseMessage(item)
                
                if msg is not None:
                    print "******* send to client *******"
                    print msg
                    #msg = "@skygon " + msg
                    #itchat.send_msg(msg, CLIENT_NAME)
                    author.send_msg(msg)
            except Exception, e:
                print "Pusher failed [%s]" %(str(e))