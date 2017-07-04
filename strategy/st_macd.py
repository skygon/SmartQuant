import os
import sys
import threading
import Queue
sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), 'tech_index'))

from macd import MACD
from utils import *

tp_num = 1
class ST_MACD(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        #self.que = Utils.getHS300Queue()
        self.que = Utils.getHS300AndZZ500()
        self.macd = MACD('000001')
        self.start()

    def processOneCode(self, code):
        self.macd.setCode(code)
        self.macd.getMACD()
        if self.macd.canBuy():
            print "code [%s] can buy " %(code)
    
    def handleNumericCode(slef, code):
        c = str(code)
        if len(c) < 6:
            c = "0" * (6 - len(c)) + c
        
        return c
    
    def run(self):
        while True:
            try:
                code = self.que.get(False)
                code = self.handleNumericCode(code)
                self.processOneCode(code)
            except Queue.Empty:
                print "All works of ST_MACD have been done \n"
                break
            except Exception, e:
                print "ST_MACD Error : %s \n" %(str(e))


if __name__ =="__main__":
    threads = []
    for i in range(tp_num):
        t = ST_MACD()
        threads.append(t)
    
    for t in threads:
        if t.isAlive():
            t.join()
