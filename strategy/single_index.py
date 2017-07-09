import os
import sys
import threading
import Queue
sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), 'tech_index'))

from macd import MACD
from rsi import RSI
from kdj import KDJ
from utils import *

tp_num = 1
class SingleIndex(threading.Thread):
    def __init__(self, index_type='macd'):
        threading.Thread.__init__(self)
        #self.que = Utils.getHS300Queue()
        self.que = g_utils.full_queue
        if index_type == 'macd':
            self.index_obj = MACD('000001')
        elif index_type == 'rsi':
            self.index_obj = RSI('000001')
        elif index_type == 'kdj':
            self.index_obj = KDJ('000001')
        
        print self.index_obj.current_date
        self.start()

    def processOneCode(self, code):
        self.index_obj.setCode(code)
        if self.index_obj.canBuy():
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
                print "All works of single index have been done \n"
                break
            except Exception, e:
                print "single index Error : %s \n" %(str(e))
        
        self.index_obj.analysis()


if __name__ =="__main__":
    threads = []
    for i in range(tp_num):
        t = SingleIndex('kdj')
        threads.append(t)
    
    for t in threads:
        if t.isAlive():
            t.join()
