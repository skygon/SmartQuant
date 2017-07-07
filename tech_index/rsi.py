import os
import talib as ta
from pandas import DataFrame
import sys
sys.path.append(os.getcwd())
from utils import *

class RSI(object):
    def __init__(self, code):
        self.code = code
        self.hist_day_path = os.path.join(os.getcwd(), 'hist_data', 'day')

    def getCurrentDate(self):
        file_name = '601998_hist_d.csv' # china bank
        full_path = os.path.join(self.hist_day_path, file_name)
        df = DataFrame.from_csv(full_path)
        date = df.date.values
        return date

    def setCode(self, code):
        self.code = code

    def invalidCode(self):
        #return self.date[-1] != self.today
        return False

    def getRSI(self):
        file_name = self.code + '_hist_d.csv'
        full_path = os.path.join(self.hist_day_path, file_name)
        self.df = DataFrame.from_csv(full_path)
        self.date = self.df.date.values
        close = self.df.close.values
        self.rsi = {}
        self.rsi['6'] = ta.RSI(close, timeperiod=6)
        self.rsi['12'] = ta.RSI(close, timeperiod=12)
        self.rsi['24'] = ta.RSI(close, timeperiod=24)

    def canBuy(self):
        try:
            self.getRSI()
            if self.invalidCode():
                debug_logger("==== exit 0 ====")
                return False
            
            if self.rsi['6'][last_days['one']] < self.rsi['12'][last_days['one']]:
                debug_logger("==== exit 1 ====")
                return False
            
            for d in ['two', 'three', 'four']:
                if self.rsi['6'][last_days[d]] >= self.rsi['12'][last_days[d]]:
                    debug_logger("==== exit 2 ====")
                    return False
            
            if min(self.rsi['6'][-4:]) >= 20:
                debug_logger("==== exit 3 ====")
                return False
            
            return True
        except Exception, e:
            print "RSI.canBuy failed %s" %(str(e))
    

if __name__ == "__main__":
    r = RSI('603993', '2017-07-04')
    print r.current_date
    #r.getRSI()
    #date = r.df.date.values

    #for i in range(len(date)):
    #    print date[i], r.rsi['6'][i], r.rsi['12'][i], r.rsi['24'][i]
