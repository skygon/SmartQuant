import os
import talib as ta
from pandas import DataFrame
import sys
sys.path.append(os.getcwd())
from utils import *


class KDJ(object):
    def __init__(self, code):
        self.code = code
        self.hist_day_path = os.path.join(os.getcwd(), 'hist_data', 'day')
    
    def setCode(self, code):
        self.code = code
    
    def getCurrentDate(self):
        file_name = '601998_hist_d.csv' # china bank
        full_path = os.path.join(self.hist_day_path, file_name)
        df = DataFrame.from_csv(full_path)
        date = df.date.values
        return date
    
    def getKDJ(self):
        file_name = self.code + '_hist_d.csv'
        full_path = os.path.join(self.hist_day_path, file_name)

        self.df = DataFrame.from_csv(full_path)
        high = self.df.high.values
        low = self.df.low.values
        close = self.df.close.values
        # matype: 0=SMA, 1=EMA, 2=WMA, 3=DEMA, 4=TEMA, 5=TRIMA, 6=KAMA, 7=MAMA, 8=T3 (Default=SMA)
        self.k, self.d = ta.STOCH(high, low, close, fastk_period=9,slowk_period=3,slowk_matype=0,slowd_period=3,slowd_matype=0)
    
    def bottomCross(self):
        if self.k[last_days['one']] < self.d[last_days['one']]:
                return False
            
        for d in ['two', 'three', 'four']:
            if self.k[last_days[d]] >= self.d[last_days[d]]:
                return False
            
        if min(self.k[-4:]) > 20:
            return False
        
        return True

    def rightCross(self):
        count = 0
        for i in range(len(day_array) - 1):
            if self.d[last_days[day_array[i]]] < self.d[last_days[day_array[i+1]]]:
                print "==== exit rigthCross ===="
                return False
            
        return True

    
    def canBuy(self):
        try:
            self.getKDJ()
            if self.bottomCross() is False:
                return False
            if self.rightCross() is False:
                return False
            
            return True
        except Exception, e:
            print "KDJ.canBuy failed %s" %(str(e))

if __name__ == "__main__":
    kdj = KDJ('603993')
    
