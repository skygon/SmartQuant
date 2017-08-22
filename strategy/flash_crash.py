#encoding=utf-8
import os
import sys
import threading
import Queue
import requests
import time
from pandas import DataFrame
sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), 'tech_index'))
sys.path.append(os.path.join(os.getcwd(), 'information_service'))


from TickPrice import TickPrice
from WatchDog import WatchDog
from shake import Shake
from box import Box
from message_pusher import Pusher
from utils import *


# TODO
# 排除crash时跌幅太大的股票，比如超过8%，可能会到跌停板
# 不要重复发送。发送一次后，记录ticks， 到达一定的ticks后才能再次发送
# 日志的控制开关放到redis中
# 从热门板块中挑选crash

class Watcher(threading.Thread):
    def __init__(self):
        super(Watcher, self).__init__()
        self.url_type = 'sina'
        self.base_len = 0
        self.enter_max = 1.02
        self.enter_min = 0.98
        self.confirm = 0.97
        self.sleep = 2 # sleep seconds
        self.flash_time = 210 # flash crash must happen in xxx seconds. Best practice: 3 - 4 mins
        self.total_ticks = 0
        self.init_ticks = self.flash_time / (self.sleep)
        self.hist_day_path = os.path.join(os.getcwd(), 'hist_data', 'day')
        self.indicate = True
        self.show = 0

        self.initCodeBase()
        print "I have code base %s" %(self.code)
        if self.base_len > 0:
            self.prepareURL()
            self.start()


    def prepareData(self, code):
        file_name = code + '_hist_d.csv'
        full_path = os.path.join(self.hist_day_path, file_name)

        if os.path.isfile(full_path) is False:
            df = DataFrame()
        else:
            df = DataFrame.from_csv(full_path)

        self.close = [] if df.empty else df.high.values
    
    def initCodeBase(self):
        try:
            self.code = []
            self.conf = {}
            while True:
                if self.base_len >= 10:
                    break
                
                c = g_utils.full_queue.get(False)
                #check if stock fresh
                self.prepareData(c)
                if len(self.close) < 120:
                    continue

                if c.find("300") == 0:
                    continue
                if c.find("60") == 0:
                    c = "sh" + c
                else:
                    c = "sz" + c
                self.conf[c] = {}
                self.conf[c]['ticks'] = []
                self.conf[c]['send'] = False
                self.conf[c]['count'] = 0
                self.conf[c]['log'] = 0
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
        op = float(a[1])
        settlement = float(a[2])
        current = float(a[3])
        return code, settlement, current, op

    def parseLineTx(self, line):
        a = line.split('~')
        code = a[2]
        if code.find("60") == 0:
            code = "sh" + code
        else:
            code = "sz" + code
        current = float(a[3])
        settlement = float(a[4])
        op = float(a[5])
        return code, settlement, current, op

    def parseLine(self, alllines):
        try:
            for line in alllines:
                if self.url_type == 'sina':
                    code, settlement, current, op = self.parseLineSina(line)
                elif self.url_type == 'tx':
                    code, settlement, current, op = self.parseLineTx(line)
                #print "code: %s, settlement: %s, current: %s" %(code, settlement, current)
                #print "code[%s], close[%s], now[%s]" %(code, settlement, current)
                if self.total_ticks < self.init_ticks:
                    self.conf[code]['ticks'].append(current)
                    continue
                if settlement == 0 or current == 0:
                    continue

                #if current / settlement <= self.enter_max and current / settlement >= self.enter_min:
                index = self.total_ticks % self.init_ticks
                p = self.conf[code]['ticks'][index]
                if p == 0:
                    if self.conf[code]['log'] >= 50:
                        print "Get zero from code[%s]. Check this please." %(code)
                        self.conf[code]['log'] = 0
                    self.conf[code]['log'] += 1
                    continue
                
                if current / p <= self.confirm:
                    if self.conf[code]['send'] is False:
                        msg = "crash:%s" %(code)
                        print msg
                        g_utils.msg_queue.put(msg)
                        self.conf[code]['send'] = True
                        self.conf[code]['count'] = 0
                elif current / p <= 0.975:
                    print "=-=-= 2.5 backup : [%s] =-=-=" %(code)
                elif current / p <= 0.98:
                    print "=*=*= 2.0 backup : [%s] =*=*=" %(code)
                
                self.conf[code]['count'] += 1    
                if self.conf[code]['count'] >= 50:
                    self.conf[code]['send'] = False
                    self.conf[code]['count'] = 0

                # replace the init price
                self.conf[code]['ticks'][index] = current
            
            self.total_ticks += 1
        except Exception, e:
            print "parseLine failed %s" %(str(e))

    def run__(self):
        while True:
            g_utils.msg_queue.put("test:hello")
            time.sleep(5)

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

                end = time.time()
                if (self.total_ticks >= self.init_ticks or (int)(end - start) > self.flash_time) and self.indicate:
                    self.indicate = False
                    self.init_ticks = self.total_ticks
                    print "Collect init ticks[%s] cost %s seconds" %(self.total_ticks, (end-start))
            except Exception, e:
                print "Watcher error: %s" %(str(e))
                time.sleep(2)
                s = requests.Session()


def start_monitor():
    p = Pusher({})
    p.start()

    wd = WatchDog()
    wd.start()

    #watchers = []
    #for i in range(200):
    #    w = Watcher()
    #    watchers.append(w)
    
    while True:
        print "=============================================="
        time.sleep(10)

if __name__ == "__main__":
    start_monitor()
    #  p = Pusher({})
    #  p.start()
    #  w = Watcher()
    #  w.join()