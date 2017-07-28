#coding=utf-8
import os
import sys
sys.path.append(os.getcwd())
from VolumeBase import VolumeBase
from RealTimePrice import RealtimePrice
from utils import *


class Box(VolumeBase):
    def __init__(self):
        self.total = 0
        self.stock_pool = 0
        self.exit_check_price = 0
        self.exit_current_price = 0
        self.exit_uniform_distribute = 0
        self.rt = RealtimePrice()
        self.test = True

        if self.test:
            self.start_day = -30
            last_days['one'] = self.start_day
        else:
            self.start_day = -1  # we can set this to early days for test

        super(Box, self).__init__()
        self.box_len = 180
        self.partition = 4
        self.max_shake = 0.4
        self.uniform_shake = 0.06
        self.enter = 0.04

    def isNewStock(self):
        if len(self.close) < self.box_len + abs(self.start_day):
            return True
        return False

    
    def checkPrice(self):
        try:
            high = []
            low = []
            self.max_high = 0.0
            self.min_low = 0.0
            for i in range(self.start_day, -self.box_len+self.start_day, -1):
                high.append(self.high[i])
                low.append(self.low[i])

            high.sort(reverse=True) # high[0] is the largest
            low.sort() #low[0] is the lowest

            #omit the largest and lowest
            if low[1] == 0:
                return False
            
            if (high[1] - low[1]) / low[1] < self.max_shake:
                self.max_high = high[1]
                self.min_low = low[1]
                return True

            return False
        except Exception, e:
            print "check price failed %s" %(str(e))
    
    # check if high price exist uniformly
    def uniformDistribute(self):
        try:
            step = self.box_len / self.partition
            lh = []
            for i in range(self.partition):
                high = []
                offset = 1 if i==0 else 0
                start = i * (-step) - offset + self.start_day + 1
                end = (i+1) * (-step) + self.start_day + 1
                for j in range(start, end, -1):
                    high.append(self.high[j])
                    high.sort(reverse=True)
                if abs(high[1] - self.max_high) / self.max_high > self.uniform_shake:
                    return False
                lh.append(high[1])
            #print "three highs: %s" %(lh)
            return True
        except Exception, e:
            print "uniformDistribute failed %s" %(str(e))


    def checkCurrentPriceFake(self):
        cp = self.low[self.start_day]
        if (cp - self.min_low) / self.min_low < self.enter:
            print "high : %s, low : %s, current: %s" %(self.max_high, self.min_low, cp)
            return True
            
        return False

    def checkCurrentPrice(self):
        try:
            if self.code.find("60") == 0:
                c = "sh" + self.code
            else:
                c = "sz" + self.code

            self.rt.setCode(c)
            cp = self.rt.getCurrentPrice()
            if (cp - self.min_low) / self.min_low < self.enter:
                print "high : %s, low : %s, current: %s" %(self.max_high, self.min_low, cp)
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

            ret = self.uniformDistribute()
            if ret is False:
                self.exit_uniform_distribute += 1
                return False
            
            if self.test:
                ret = self.checkCurrentPriceFake()
            else:
                ret = self.checkCurrentPrice()
            
            if ret is False:
                self.exit_current_price += 1
                return False
            
            self.stock_pool += 1
            return True
        except Exception, e:
            print "box canBuy failed %s" %(str(e))

    
    def analysis(self):
        print "==== total codes : %s" %(self.total)
        print "==== exit from check price : %s" %(self.exit_check_price)
        print "==== exit from uniform distribute : %s" %(self.exit_uniform_distribute)
        print "==== exit from current price: %s" %(self.exit_current_price)
        print "==== stock pool size is %s" %(self.stock_pool)

if __name__ == "__main__":
    b = Box()
    b.setCode("603993")
    b.canBuy()