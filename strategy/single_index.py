import os
import sys
import threading
import Queue
sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), 'tech_index'))

from macd import MACD
from rsi import RSI
from kdj import KDJ
from VolumeMotivation import VolumeMotivation
from utils import *

tp_num = 1
class SingleIndex(threading.Thread):
    def __init__(self, index_type='macd'):
        threading.Thread.__init__(self)
        self.que = g_utils.sz50_que
        #self.que = g_utils.hs300_que
        #self.que = g_utils.zz500_que
        if index_type == 'macd':
            self.index_obj = MACD('000001')
        elif index_type == 'rsi':
            self.index_obj = RSI('000001')
        elif index_type == 'kdj':
            self.index_obj = KDJ('000001')
        elif index_type == 'vol_motivation':
            self.index_obj = VolumeMotivation()
        
        print self.index_obj.current_date
        self.start()

    def processOneCode(self, code):
        self.index_obj.setCode(code)
        if self.index_obj.canBuy():
            print "[%s]" %(code)
    
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
        t = SingleIndex('vol_motivation')
        threads.append(t)
    
    for t in threads:
        if t.isAlive():
            t.join()
