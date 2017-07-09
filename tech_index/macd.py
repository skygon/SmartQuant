#coding=utf-8
import os
import talib
import matplotlib.pyplot as plt
from pandas import DataFrame
import sys
sys.path.append(os.getcwd())
from utils import *

class MACD(object):
    def __init__(self, code):
        self.code = code
        self.hist_day_path = os.path.join(os.getcwd(), 'hist_data', 'day')
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
        
        return True
    
    def getMACD(self):
        try:
            file_name = self.code + '_hist_d.csv'
            full_path = os.path.join(self.hist_day_path, file_name)
            self.df = DataFrame.from_csv(full_path)
            self.date = self.df.date.values
            self.close = self.df.close.values
            self.volume = self.df.volume.values
            self.dif, self.dea, self.macd = talib.MACD(self.close, fastperiod=12, slowperiod=26, signalperiod=9)
        except Exception, e:
            print "getMACD error %s" %str(e)
    
    def isUpCross(self):
        if self.dif[last_days['one']] < self.dea[last_days['one']]:
            return False
        
        for i in range(1, len(day_array)):
            if self.dif[last_days[day_array[i]]] >= self.dea[last_days[day_array[i]]]:
                return False
        
        return True
    
    def isSmallIncPrice(self):
        ret = False
        if (self.close[last_days['one']] - self.close[last_days['two']] > 0) and (self.close[last_days['one']] - self.close[last_days['two']]) / self.close[last_days['two']] <= 0.015:
            ret = True

        return ret

    def isDeclineVolume(self):
        ret = False
        if self.volume[last_days['one']] < self.volume[last_days['two']]:
            ret = True
        
        return ret

    # MUST call after getMACD
    # strategy 0: simple cross
    # strategy 1: cross and small increase price
    # strategy 2: cross; decline volume; small increase price
    def canBuy(self, strategy=2):
        self.getMACD()
        ret = False
        if self.invalidCode():
            return ret
        
        if strategy == 0:
            ret = self.isUpCross()
        elif strategy == 1:
            ret = self.isUpCross() and self.isSmallIncPrice()
        elif strategy == 2:
            ret = self.isUpCross() and self.isSmallIncPrice() and self.isDeclineVolume()
            
        return ret
        
    def analysis(self):
        pass


if __name__ == "__main__":
    m = MACD('600007')
    m.canBuy(2)
    for i in range(len(m.dif)):
        print "%s: DIF: %s, DEA: %s, MACD: %s" %(m.date[i], m.dif[i], m.dea[i], 2*m.macd[i])
    
    
    
