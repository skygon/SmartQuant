import os
import sys
import threading
import Queue
import requests
import time
sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), 'tech_index'))
sys.path.append(os.path.join(os.getcwd(), 'information_service'))


from TickPrice import TickPrice
from shake import Shake
from box import Box
from message_pusher import Pusher
from utils import *

INDEX_URL = "http://hq.sinajs.cn/list="

class Watcher(threading.Thread):
    def __init__(self):
        super(Watcher, self).__init__()
        self.base_len = 10
        self.initCodeBase()
        print "I have code base %s" %(self.code)
        self.prepareURL()

    def initCodeBase(self):
        try:
            self.code = []
            for i in range(self.base_len):
                c = g_utils.full_queue.get(False)
                if c.find("300") == 0:
                    continue
                if c.find("60") == 0:
                    c = "sh" + c
                else:
                    c = "sz" + c
                self.code.append(c)
        except Queue.Empty:
            return
        except Exception, e:
            print "initCodeBase failed %s" %(str(e))
        
    def prepareURL(self):
        codes = ','.join(self.code)
        self.url = INDEX_URL + codes

    def parseLine(self, alllines):
        try:
            for line in alllines:
                a = line.split(',')
                a0 = a[0].split('=')[0]
                code = a0[-6:]
                settlement = a[2]
                current = a[3]
                print "code[%s], close[%s], now[%s]" %(code, settlement, current)
        except Exception, e:
            print "parseLine failed %s" %(str(e))

    def run(self):
        while True:
            try:
                r = requests.get(self.url)
                # last line is empty line
                alllines = r.text.encode("utf-8").split(';')[:-1]
                self.parseLine(alllines)
                time.sleep(2)
            except Exception, e:
                print "Watcher error: %s" %(str(e))


if __name__ == "__main__":
    w = Watcher()
    w.start()
    w.join()