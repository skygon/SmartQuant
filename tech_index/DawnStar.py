#coding=utf-8
import os
import sys
from pandas import DataFrame
sys.path.append(os.getcwd())
from utils import *
from RealTimeDataAcq import RTDA
from VolumeBase import VolumeBase

class DawnStar(VolumeBase):
    def __init__(self):
        super(DawnStar, self).__init__()
        self.total = 0
        self.exit_invalid_code = 0
        self.exit_check_1 = 0
        self.exit_check_2 = 0
        self.exit_check_3 = 0
        self.stock_pool = 0

    # 长阴线，仅仅对比该天的open和close的数值
    def checkDay_3(self):
        if float(self.open[last_days['three']]) == 0.0:
            print "======1======="
            return False
        
        if float(self.close[last_days['three']]) / self.open[last_days['three']] > 0.95:
            return False
        
        return True

    # 跳空低开，十字星
    def checkDay_2(self):
        if self.open[last_days['two']] > self.close[last_days['three']]:
            return False
        
        if float(self.close[last_days['two']]) == 0.0:
            return False
        
        if abs(self.close[last_days['two']] - self.open[last_days['two']]) / float(self.close[last_days['two']]) > 0.015:
            return False
        
        # TODO 当日放量，警惕主力出货
        return True

    # 长阳线，价格回到两天前的阴线范围之内
    def checkDay_1(self):
        if float(self.open[last_days['one']]) == 0.0:
            return False

        if float(self.close[last_days['one']]) / self.open[last_days['one']] < 1.05:
            return False
        
        if float(self.close[last_days['one']]) < self.close[last_days['three']]:
            return False

        # TODO 增加判断价格是否长期处于历史相对地位
        # TODO 上涨无量，警惕主力诱多
        return True

    def canBuy(self):
        try:
            self.total += 1
            self.prepareData()

            if self.invalidCode() or self.isNewStock():
                self.exit_invalid_code += 1
                return False
            
            if self.isStartUp():
                return False
            

            if self.checkDay_3() is False:
                self.exit_check_3 += 1
                return False
            
            if self.checkDay_2() is False:
                self.exit_check_2 += 1
                return False
            
            if self.checkDay_1() is False:
                self.exit_check_1 += 1
                return False
            
            self.stock_pool += 1
            return True
        except Exception, e:
            print "DawnStar->canBuy failed %s" %(str(e))
            return False

    def analysis(self):
        print "==== total codes : %s" %(self.total)
        print "==== exit from invalid code : %s" %(self.exit_invalid_code)
        print "==== exit from check 3 size is %s" %(self.exit_check_3)
        print "==== exit from check 2 size is %s" %(self.exit_check_2)
        print "==== exit from check 1 size is %s" %(self.exit_check_1)
        print "==== stock pool size is %s" %(self.stock_pool)

    
if __name__ == "__main__":
    pass