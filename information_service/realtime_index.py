# -*-coding:utf-8 -*-
import requests
import time
import os
import sys
import threading
from Queue import Queue
#itchat, a wechat autoreply tool
import itchat
from itchat.content import *

sys.path.append(os.getcwd())
from utils import *

INDEX_URL = "http://hq.sinajs.cn/list="

class RealtimeIndex(threading.Thread):
    def __init__(self):
        super(RealtimeIndex, self).__init__() 
        # message service will use this flag to handle different type of msg
        self.flag = "price" 

    # code should be like shxxxxxx szxxxxxx
    def setCode(self, code):
        self.code = code
        self.url = INDEX_URL + self.code
    

    def run(self):
        while True:
            try:
                r = requests.get(self.url)
                #print r.text.encode("utf-8")
                res = r.text.encode("utf-8").split(',')
                if len(res) > 1:
                    print "============"
                    current_price = res[3]
                    msg = self.flag + ":" + self.code + ":" + current_price
                    print "message is [%s]" %(msg)
                    put2MsgQue(msg)
                time.sleep(5)
            except Exception, e:
                print "Get Exception in getting info from code[%s]: [%s]" %(self.code, str(e))


if __name__ == "__main__":
    r = RealtimeIndex()
    r.setCode('sh603993')
    r.start()
    r.join()