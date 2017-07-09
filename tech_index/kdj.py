import os
import talib as ta
import numpy as np
from pandas import DataFrame
import sys
sys.path.append(os.getcwd())
from utils import *


class KDJ(object):
    def __init__(self, code):
        self.code = code
        self.hist_day_path = os.path.join(os.getcwd(), 'hist_data', 'day')
        self.total = 0
        self.exit_bottom_cross = 0
        self.exit_right_cross = 0
        self.exit_invalid_code = 0
        self.getCurrentDate()
    
    def setCode(self, code):
        self.code = code
    
    def getCurrentDate(self):
        file_name = '601988_hist_d.csv' # china bank
        full_path = os.path.join(self.hist_day_path, file_name)
        df = DataFrame.from_csv(full_path)
        self.current_date = df.date.values[last_days['one']]
    
    def invalidCode(self):
        today = self.df.date.values[last_days['one']]
        if today == self.current_date:
            return False
        
        self.exit_invalid_code += 1
        return True

    
    def prepareData(self):
        file_name = self.code + '_hist_d.csv'
        full_path = os.path.join(self.hist_day_path, file_name)

        self.df = DataFrame.from_csv(full_path)
        self.high = self.df.high.values
        self.low = self.df.low.values
        self.close = self.df.close.values
        self.date = self.df.date.values

    def getKDJ(self):
        self.prepareData()
        # matype: 0=SMA, 1=EMA, 2=WMA, 3=DEMA, 4=TEMA, 5=TRIMA, 6=KAMA, 7=MAMA, 8=T3 (Default=SMA)
        self.k, self.d = ta.STOCH(self.high, self.low, self.close, fastk_period=9,slowk_period=3,slowk_matype=0,slowd_period=3,slowd_matype=0)


    def getRSV(self, N):
        self.rsv = [0] * len(self.close)
        # first day
        if self.high[0] == self.low[0]:
            d0 = 100
        else:
            d0 = (self.close[0] - self.low[0]) / (self.high[0] - self.low[0]) * 100
        self.rsv[0] = d0

        for i in range(1, len(self.close)):
            # first N days
            if i < N:
                d = (self.close[i] - min(self.low[:i+1])) / (max(self.high[:i+1]) - min(self.low[:i+1])) * 100
                self.rsv[i] = d
            else:
                d = (self.close[i] - min(self.low[i-N+1:i+1])) / (max(self.high[i-N+1:i+1]) - min(self.low[i-N+1:i+1])) * 100
                self.rsv[i] = d
        

    def getKDJ2(self, N1=9, N2=3, N3=3):
        try:
            self.prepareData()
            self.getRSV(N1)

            self.k = [0] * len(self.close)
            self.d = [0] * len(self.close)
            self.j = [0] * len(self.close)

            self.k[0] = float(2) / 3 * 50 + float(1) / 3 * self.rsv[0]
            self.d[0] = float(2) / 3 * 50 + float(1) / 3 * self.k[0]
            self.j[0] = 3 * self.k[0] - 2 * self.d[0]

            for i in range(1, len(self.close)):
                self.k[i] = float(2) / 3 * self.k[i-1] + float(1) / 3 * self.rsv[i]
                self.d[i] = float(2) / 3 * self.d[i-1] + float(1) / 3 * self.k[i]
                self.j[i] = 3 * self.k[i] - 2 * self.d[i]
        except Exception, e:
            print "getKDJ2 failed %s" %(str(e))
     
    def bottomCross(self):
        if self.k[last_days['one']] < self.d[last_days['one']]:
                self.exit_bottom_cross += 1
                return False
            
        for d in ['two', 'three', 'four']:
            #if self.k[last_days[d]] >= self.d[last_days[d]]:
            if self.d[last_days[d]] - self.k[last_days[d]] <= 10:
                self.exit_bottom_cross += 1
                return False
        
        if start_day == -4:
            if min(self.k[start_day:]) > 50:
                self.exit_bottom_cross += 1
                return False
        else:
            if min(self.k[start_day:start_day+4]) > 50:
                self.exit_bottom_cross += 1
                return False
        
        return True

    def rightCross(self):
        count = 0
        if self.d[last_days['one']] < self.d[last_days['two']]:
            self.exit_right_cross += 1
            return False
        
        for i in range(1, len(day_array) - 1):
            if self.d[last_days[day_array[i]]] > self.d[last_days[day_array[i+1]]]:
                self.exit_right_cross += 1
                return False
            
        return True

    def analysis(self):
        print "==== total codes : %s" %(self.total)
        print "==== exit from invalid code : %s" %(self.exit_invalid_code)
        print "==== exit from bottom cross : %s" %(self.exit_bottom_cross)
        print "==== exit from right cross : %s" %(self.exit_right_cross)
    
    def canBuy(self):
        try:
            self.total += 1
            self.getKDJ2()
            if self.invalidCode():
                return False
            
            if self.bottomCross() is False:
                return False
            if self.rightCross() is False:
                return False
            
            return True
        except Exception, e:
            print "KDJ.canBuy failed %s" %(str(e))

    

if __name__ == "__main__":
    kdj = KDJ('300406')
    #kdj.getKDJ()
    kdj.getKDJ2()
    
    for i in range(len(kdj.close)):
        print kdj.date[i], kdj.k[i], kdj.d[i], kdj.j[i]
    
