#coding=utf-8
import os
import sys
sys.path.append(os.getcwd())
from VolumeBase import VolumeBase
from utils import *

class Shake(VolumeBase):
    def __init__(self):
        super(Shake, self).__init__()
        self.days = 8
        self.threshold = 3
        self.total = 0

    # 选择近期多空势力交战激烈的个股
    def shakeMode(self):
        start = last_days['one']
        count = 0
        
        for i in range(self.days):
            if self.open[start - i] == 0:
                return False
            
            body = abs(self.open[start - i] - self.close[start - i])
            shadow = min(self.close[start - i], self.open[start - i]) - self.low[start - i]
            if body == 0:
                continue
            
            if self.low[start - i] / min(self.close[start - i], self.open[start - i]) < 0.97:
                count += 1

        if count >=3:
            return True
        else:
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
            return ret  
        except Exception, e:
            print "Shark canBuy failed %s: %s" %(self.code, str(e))
            print len(self.open), len(self.close), len(self.low)