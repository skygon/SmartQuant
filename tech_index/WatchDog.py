#coding=utf-8
import os
import sys
import threading
import json
import time
from pandas import DataFrame
sys.path.append(os.getcwd())
from ts_wrapper import TsWrapper
import  requests
from RedisOperator import RedisOperator
from utils import *


class WatchDog(threading.Thread):
    def __init__(self):
        super(WatchDog, self).__init__()
        self.url_type = 'sina'
        self.table = "watch_table"
        self.per = {}
        self.code = []
        self.conf_file = os.path.join(os.getcwd(), 'config', 'watchdog.json')
        self.redis = RedisOperator("localhost", 6379, 0)
        self.readConfFile()
        self.prepareURL()
        #self.readConfFromRedis()

    def readConfFile(self):
        with open(self.conf_file, 'r') as f:
            self.conf = json.load(f)
        try:
            for k, v in self.conf.items():
                self.code.append(k)
                self.per[k] = {}
                self.per[k]['c'] = 1.0
                self.per[k]['b'] = 1.0
                self.redis.hsetJson(self.table, k, v)
                #v['bottom'] = v['bottom'] * 0.98
            print self.conf
        except Exception, e:
            print "readConfFile failed %s" %(str(e))
    
    
    def readConfFromRedis(self):
        try:
            keys = self.redis.hkeys(self.table)
            self.code = []
            #print "conf has keys: %s" %(keys)
            for k in keys:
                self.code.append(k)
                strv = self.redis.hget(self.table, k)
                v = json.loads(strv)
                self.conf[k] = v
            #print self.conf
        except Exception, e:
            print "read conf from redis failed -> %s" %(str(e))

    def prepareURL(self):
        codes = ','.join(self.code)
        if self.url_type == 'sina':
            self.url = SINA_INDEX_URL + codes
        elif self.url_type == 'tx':
            self.url = TX_INDEX_URL + codes
        #print "watch dog index url is %s" %(self.url)
    
    def getMsg(self, code, current, per1, per2):
        msg = "monitor:[%s] IN (%s, %s). Price is %s" %(code, per1, per2, current)
        print msg
        return msg

    def parseLineSina(self, line):
        a = line.split(',')
        a0 = a[0].split('=')[0]
        code = a0[-8:] #shxxxxxx or szxxxxxx
        op = float(a[1])
        settlement = float(a[2])
        current = float(a[3])
        return code, current

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
        return code, current

    def parseLine(self, alllines):
        hasMsg = False
        try:
            for line in alllines:
                if self.url_type == 'sina':
                    code, current = self.parseLineSina(line)
                elif self.url_type == 'tx':
                    code, current, op = self.parseLineTx(line)
                
                if current > self.conf[code]['ceilling']:
                    # adjust box ceilling and bottom percentage
                    while self.per[code]['c'] * self.conf[code]['keep'] < current:
                        self.per[code]['b'] = self.per[code]['c']
                        self.per[code]['c'] += 0.01
                    
                    # adjust box high and low price
                    self.conf[code]['bottom'] = round(self.conf[code]['keep'] * self.per[code]['b'] ,2)
                    self.conf[code]['ceilling'] = round(self.conf[code]['keep'] * self.per[code]['c'] ,2)

                    msg = self.getMsg(code, current, self.per[code]['b'], self.per[code]['c'])
                    g_utils.msg_queue.put(msg)
                    
                elif current < self.conf[code]['bottom']:
                    while self.per[code]['b'] * self.conf[code]['keep'] > current:
                        self.per[code]['c'] = self.per[code]['b']
                        self.per[code]['b'] -= 0.01

                    self.conf[code]['ceilling'] = round(self.conf[code]['keep'] * self.per[code]['c'] , 2)
                    self.conf[code]['bottom'] = round(self.conf[code]['keep'] * self.per[code]['b'] , 2)

                    msg = self.getMsg(code, current, self.per[code]['b'], self.per[code]['c'])
                    g_utils.msg_queue.put(msg)
                    

        except Exception, e:
            print "parse line failed %s" %(str(e))
    
    def run(self):
        s = requests.Session()
        while True:
            try:
                self.readConfFromRedis()
                self.prepareURL()
                if len(self.code) == 0:
                    time.sleep(60)
                    continue

                r = s.get(self.url)
                # last line is empty line
                alllines = r.text.encode("utf-8").split(';')[:-1]
                self.parseLine(alllines)
                time.sleep(30)
            except Exception, e:
                print "WatchDog error %s" %(str(e))
                time.sleep(3)
                s = requests.Session()

if __name__ == "__main__":
    w = WatchDog()
    w.start()
