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
from DawnStar import DawnStar
from TickPrice import TickPrice
from shake import Shake
from box import Box
from utils import *

tp_num = 1
#g_class_gue = g_utils.sz50_que
#g_class_gue = g_utils.hs300_que
#g_class_gue = g_utils.hs300_zz500_que
#g_class_gue = g_utils.zz500_que
g_class_gue = g_utils.full_queue

class SingleIndex(threading.Thread):
    def __init__(self, index_type='macd'):
        threading.Thread.__init__(self)
        if index_type == 'macd':
            self.index_obj = MACD('000001')
        elif index_type == 'rsi':
            self.index_obj = RSI('000001')
        elif index_type == 'kdj':
            self.index_obj = KDJ('000001')
        elif index_type == 'vol_motivation':
            self.index_obj = VolumeMotivation()
        elif index_type == 'k-dawnstar':
            self.index_obj = DawnStar()
        elif index_type == 'tick_price':
            self.index_obj = TickPrice('2017-07-19')
        elif index_type == 'shake':
            self.index_obj = Shake()
        elif index_type == 'box':
            self.index_obj = Box()
        
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
                code = g_class_gue.get(False)
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
        t = SingleIndex('box')
        threads.append(t)
    
    for t in threads:
        if t.isAlive():
            t.join()
