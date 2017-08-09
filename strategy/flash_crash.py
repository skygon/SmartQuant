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

SINA_INDEX_URL = "http://hq.sinajs.cn/list="
TX_INDEX_URL = "http://qt.gtimg.cn/q="

class Watcher(threading.Thread):
    def __init__(self):
        super(Watcher, self).__init__()
        self.url_type = 'sina'
        self.base_len = 0
        self.enter_max = 1.02
        self.enter_min = 0.98
        self.confirm = 0.97
        self.sleep = 1 # sleep seconds
        self.flash_time = 5 # flash crash must happen in xxx seconds
        self.total_ticks = 0
        self.init_ticks = self.flash_time / self.sleep
        self.initCodeBase()
        self.indicate = True
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
        if self.url_type == 'sina':
            self.url = SINA_INDEX_URL + codes
        elif self.url_type == 'tx':
            self.url = TX_INDEX_URL + codes
        print "index url is %s" %(self.url)

    def parseLineSina(self, line):
        a = line.split(',')
        a0 = a[0].split('=')[0]
        code = a0[-8:] #shxxxxxx or szxxxxxx
        settlement = float(a[2])
        current = float(a[3])
        return code, settlement, current

    def parseLineTx(self, line):
        a = line.split('~')
        code = a[2]
        if code.find("60") == 0:
            code = "sh" + code
        else:
            code = "sz" + code
        current = a[3]
        settlement = a[4]
        return code, settlement, current

    def parseLine(self, alllines):
        try:
            for line in alllines:
                if self.url_type == 'sina':
                    code, settlement, current = self.parseLineSina(line)
                elif self.url_type == 'tx':
                    code, settlement, current = self.parseLineTx(line)
                print "code: %s, settlement: %s, current: %s" %(code, settlement, current)
                #print "code[%s], close[%s], now[%s]" %(code, settlement, current)
                if self.total_ticks < self.init_ticks:
                    self.conf[code].append(current)
                    continue
                if settlement == 0 or current == 0:
                    continue

                if current / settlement <= self.enter_max and current / settlement >= self.enter_min:
                    index = self.total_ticks % self.init_ticks
                    p = self.conf[code][index]
                    if current / p <= self.confirm:
                        msg = "crash:%s" %(code)
                        print msg
                        g_utils.msg_queue.put(msg)
                        # replace the init price
                        self.conf[code][index] = current
            print "-------------------------------------------"
            self.total_ticks += 1
        except Exception, e:
            print "parseLine failed %s" %(str(e))

    def run(self):
        start = time.time()
        s = requests.Session()
        while True:
            try:
                r = s.get(self.url)
                # last line is empty line
                alllines = r.text.encode("utf-8").split(';')[:-1]
                self.parseLine(alllines)
                time.sleep(self.sleep)

                if self.total_ticks >= self.init_ticks and self.indicate:
                    end = time.time()
                    self.indicate = False
                    print "Collect init ticks cost %s seconds" %(end-start)
            except Exception, e:
                print "Watcher error: %s" %(str(e))
                time.sleep(2)
                s = requests.Session()


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
    #start_monitor()
    #p = Pusher({})
    #p.start()
    w = Watcher()
    w.join()