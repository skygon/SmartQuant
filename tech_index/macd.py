#coding=utf-8
import os
import talib
import matplotlib.pyplot as plt
from pandas import DataFrame

class MACD(object):
    def __init__(self, code):
        self.code = code
        self.hist_day_path = os.path.join(os.getcwd(), 'hist_data', 'day')
    
    def setCode(self, code):
        self.code = code
    
    def getMACD(self):
        try:
            file_name = self.code + '_hist_d.csv'
            full_path = os.path.join(self.hist_day_path, file_name)
            self.df = DataFrame.from_csv(full_path)
            self.close = self.df.close.values
            self.dif, self.dea, self.macd = talib.MACD(self.close, fastperiod=12, slowperiod=26, signalperiod=9)
            return self.dif, self.dea, self.macd, self.df.date.values
        except Exception, e:
            print "getMACD error %s" %str(e)
    
    # MUST call after getMACD
    # 同时交叉点的涨幅不能多大，最好在1%一下
    def canBuy(self):
        ret = False
        if self.dif[-1] >= self.dea[-1]:
            if self.dif[-2] < self.dea[-2] and self.dif[-3] < self.dea[-3]:
                if (self.close[-1] - self.close[-2]) / self.close[-2] <= 0.1:
                    ret = True
            
        return ret
        
        

if __name__ == "__main__":
    m = MACD('603993')
    dif, dea, macd, date_str = m.getMACD()
    #for i in range(len(dif)):
    #    print "%s: DIF: %s, DEA: %s, MACD: %s" %(date_str[i], dif[i], dea[i], 2*macd[i])
    m.canBuy()
    
    
