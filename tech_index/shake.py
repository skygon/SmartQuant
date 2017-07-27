#coding=utf-8
import os
import sys
sys.path.append(os.getcwd())
from VolumeBase import VolumeBase
from utils import *

class Shake(VolumeBase):
    def __init__(self):
        super(Shake, self).__init__()
        self.days = 20
        self.shake_day = 5
        self.total = 0

    def shakeMode(self):
        start = last_days['one']
        count = 0
        
        for i in range(self.days):
            if self.open[start - i] == 0:
                return False
            
            if self.low[start - i] / min(self.close[start - i], self.open[start - i]) < 0.97:
                count += 1

        if count >= self.shake_day:
            return True
        else:
            return False
    
    def boxPeriod(self):
        start = last_days['one']
        count = 0
        for i in range(self.days):
            ma = self.getMA(start-i-1, 'price', 5)
            if abs(ma - self.close[start-i]) / float(ma) > 0.02:
                count += 1
        
        if count <= 3:
            return True

        return False

    
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
            
            ret = self.shakeMode()
            #ret = True
            #if ret:
            #    ret = self.boxPeriod()
            
            return ret  
        except Exception, e:
            print "Shark canBuy failed %s: %s" %(self.code, str(e))
            print len(self.open), len(self.close), len(self.low)