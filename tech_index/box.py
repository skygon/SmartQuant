#coding=utf-8
import os
import sys
sys.path.append(os.getcwd())
from VolumeBase import VolumeBase
from RealTimePrice import RealtimePrice
from utils import *


class Box(VolumeBase):
    def __init__(self):
        super(Box, self).__init__()
        self.total = 0
        self.stock_pool = 0
        self.exit_check_price = 0
        self.exit_current_price = 0
        self.rt = RealtimePrice()


    def checkPrice(self):
        try:
            high = []
            low = []
            self.max_high = 0.0
            self.min_low = 0.0
            for i in range(-1, -120, -1):
                high.append(self.high[i])
                low.append(self.low[i])

            high.sort(reverse=True) # high[0] is the largest
            low.sort() #low[0] is the lowest

            #ommit the largest and lowest
            if low[1] == 0:
                return False
            
            if (high[1] - low[1]) / low[1] < 0.15:
                self.max_high = high[1]
                self.min_low = low[1]
                print "high : %s, low : %s" %(high[1], low[1])
                return True

            return False
        except Exception, e:
            print "check price failed %s" %(str(e))
    
    def checkCurrentPrice(self):
        try:
            if self.code.find("60") == 0:
                c = "sh" + self.code
            else:
                c = "sz" + self.code
                
            self.rt.setCode(c)
            cp = self.rt.getCurrentPrice()
            if (cp - self.min_low) / self.min_low < 0.02:
                return True
            
            return False
        except Exception, e:
            print "check current price failed %s" %(str(e))

    def canBuy(self):
        try:
            self.total += 1
            self.prepareData()
            if self.isNewStock():
                return False
            
            if self.invalidCode():
                return False
            
            if self.isStartUp():
                return False

            ret = self.checkPrice()
            if ret is False:
                self.exit_check_price += 1
                return False

            ret = self.checkCurrentPrice()
            if ret is False:
                self.exit_current_price += 1
                return False
            
            return True
        except Exception, e:
            print "box canBuy failed %s" %(str(e))

    
    def analysis(self):
        print "==== total codes : %s" %(self.total)
        print "==== exit from check price : %s" %(self.exit_check_price)
        print "==== exit from current price: %s" %(self.exit_current_price)
        print "==== stock pool size is %s" %(self.stock_pool)

if __name__ == "__main__":
    b = Box()
    b.setCode("603993")
    b.canBuy()