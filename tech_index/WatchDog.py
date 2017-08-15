#coding=utf-8
import os
import sys
import threading
import json
from pandas import DataFrame
sys.path.append(os.getcwd())
from ts_wrapper import TsWrapper
import  requests
from utils import *


class WatchDog(threading.Thread):
    def __init__(self):
        super(WatchDog, self).__init__()
        self.url_type = 'sina'
        self.code = []
        self.conf_file = os.path.join(os.getcwd(), 'config', 'watchdog.json')
        self.readConfFile()
        self.prepareURL()

    def readConfFile(self):
        with open(self.conf_file, 'r') as f:
            self.conf = json.load(f)
        try:
            for k, v in self.conf.items():
                self.code.append(k)
                v['bottom'] = v['bottom'] * 0.98
            print self.conf
        except Exception, e:
            print "readConfFile failed %s" %(str(e))
    
    def prepareURL(self):
        codes = ','.join(self.code)
        if self.url_type == 'sina':
            self.url = SINA_INDEX_URL + codes
        elif self.url_type == 'tx':
            self.url = TX_INDEX_URL + codes
        print "watch dof index url is %s" %(self.url)
    
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
        try:
            for line in alllines:
                if self.url_type == 'sina':
                    code, current = self.parseLineSina(line)
                elif self.url_type == 'tx':
                    code, current, op = self.parseLineTx(line)
                
                if current < self.conf[code]['bottom']:

        except Exception, e:
            print "parse line failed %s" %(str(e))
    
    def run(self):
        s = requests.Session()
        while True:
            try:
                r = s.get(self.url)
                # last line is empty line
                alllines = r.text.encode("utf-8").split(';')[:-1]
                self.parseLine(alllines)
                time.sleep(3)
            except Exception, e:
                print "WatchDog error %s" %(str(e))
                time.sleep(3)
                s = requests.Session()

if __name__ == "__main__":
    w = WatchDog()
    w.readConfFile()