import os
import sys
sys.path.append(os.getcwd())
import itchat
from itchat.content import *
from utils import *
import threading
import time


class Pusher(threading.Thread):
    def __init__(self, conf):
        threading.Thread.__init__(self)
        self.conf = conf
    
    def handlePriceMsg(self):
        #msg = ':'.join(self.data)
        msg = None
        price = float(self.data[2])
        if price < 
        return msg

    def parseMessage(self, data):
        self.data = data.split(':')
        msg = None
        if self.data[0] == 'price':
            msg = self.handlePriceMsg()
        
        return msg

    def run(self):
        itchat.auto_login(True)
        itchat.send_msg("hello world", "filehelper")
        while True:
            try:
                item = g_utils.msg_queue.get()
                msg = self.parseMessage(item)
                msg = "@skygon " + msg
                if msg is not None:
                    itchat.send_msg(msg ,"filehelper")
            except Exception, e:
                print "Pusher failed [%s]" %(str(e))