#coding=utf-8
import os
import talib
import matplotlib.pyplot as plt
from pandas import DataFrame

class MACD(object):
    def __init__(self, code, today):
        self.today = today # last record of hist data files
        self.code = code
        self.hist_day_path = os.path.join(os.getcwd(), 'hist_data', 'day')
    
    def setCode(self, code):
        self.code = code
    
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
        ret = False
        if self.dif[-1] >= self.dea[-1]:
            if self.dif[-2] < self.dea[-2] and self.dif[-3] < self.dea[-3]:
                return True
    
    def isSmallIncPrice(self):
        ret = False
        if (self.close[-1] - self.close[-2] > 0) and (self.close[-1] - self.close[-2]) / self.close[-2] <= 0.015:
            ret = True

        return ret

    def isDeclineVolume(self):
        ret = False
        if self.volume[-1] < self.volume[-2]:
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
        
    
    def invalidCode(self):
        return self.date[-1] != self.today


if __name__ == "__main__":
    m = MACD('603993', '2017-07-04')
    #for i in range(len(dif)):
    #    print "%s: DIF: %s, DEA: %s, MACD: %s" %(date_str[i], dif[i], dea[i], 2*macd[i])
    m.canBuy(2)
    
    
