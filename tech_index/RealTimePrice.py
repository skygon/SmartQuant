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

class RealtimePrice(object):
    def __init__(self):
        pass

    # code should be like shxxxxxx szxxxxxx
    def setCode(self, code):
        self.code = code
        self.url = INDEX_URL + self.code
    

    def getCurrentPrice(self):
        try:
            r = requests.get(self.url)
            #print r.text.encode("utf-8")
            res = r.text.encode("utf-8").split(',')
            if len(res) > 1:
                current_price = res[3]
                return float(current_price)
        except Exception, e:
            print "Get Exception in getting info from code[%s]: [%s]" %(self.code, str(e))


if __name__ == "__main__":
    r = RealtimePrice()
    r.setCode('sh603993')
    p = r.getCurrentPrice()
    print "current price : %s" %(p)