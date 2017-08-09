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
        self.base_len = 0
        self.enter = 0.95
        self.confirm = 0.96
        self.sleep = 2 # 2 seconds
        self.flash_time = 180 # flash crash must happen in 180 seconds
        self.total_ticks = 0
        self.init_ticks = self.flash_time / self.sleep
        self.initCodeBase()
        print "I have code base %s" %(self.code)
        if self.base_len > 0:
            self.prepareURL()
            self.start()

    def initCodeBase(self):
        try:
            self.code = []
            self.conf = {}
            while True:
                if self.base_len >= 10:
                    break
                
                c = g_utils.full_queue.get(False)
                if c.find("300") == 0:
                    continue
                if c.find("60") == 0:
                    c = "sh" + c
                else:
                    c = "sz" + c
                self.conf[c] = []
                self.code.append(c)
                self.base_len += 1
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
                code = a0[-8:] #shxxxxxx or szxxxxxx
                settlement = float(a[2])
                current = float(a[3])
                #print "code[%s], close[%s], now[%s]" %(code, settlement, current)
                if self.total_ticks < self.init_ticks:
                    self.conf[code].append(current)
                    continue
                
                if current / settlement <= self.enter:
                    index = self.total_ticks % self.init_ticks
                    p = self.conf[code][index]
                    if current / p <= self.confirm:
                        msg = "crash:%s" %(code)
                        g_utils.msg_queue.put(msg)
                        # replace the init price
                        self.conf[code][index] = current

            self.total_ticks += 1
        except Exception, e:
            print "parseLine failed %s" %(str(e))

    def run(self):
        while True:
            try:
                r = requests.get(self.url)
                # last line is empty line
                alllines = r.text.encode("utf-8").split(';')[:-1]
                self.parseLine(alllines)
                time.sleep(self.sleep)
            except Exception, e:
                print "Watcher error: %s" %(str(e))


def start_monitor():
    p = Pusher({})
    p.start()

    watchers = []
    for i in range(200):
        w = Watcher()
        watchers.append(w)
    
    for t in watchers:
        if t.isAlive():
            t.join()

if __name__ == "__main__":
    start_monitor()
    #p = Pusher({})
    #p.start()
    #w = Watcher()
    #w.join()