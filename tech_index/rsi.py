import os
import talib as ta
from pandas import DataFrame
from utils import *

class RSI(object):
    def __init__(self, code, today):
        self.code = code
        self.today = today
        self.hist_day_path = os.path.join(os.getcwd(), 'hist_data', 'day')

    def setCode(self, code):
        self.code = code

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
        self.getRSI()
        if self.invalidCoe():
            return False
        
        if self.rsi['6'][last_days.one] < self.rsi['12'][last_days.two]:
            return False
        
        for d in ['two', 'three', 'four']:
            if self.rsi['6'][d] >= self.rsi['12'][d]:
                return False
        
        if min(self.rsi['6'][-4:]) >= 25:
            return False
        
        return True

    def invalidCode(self):
        return self.date[-1] != self.today
    

if __name__ == "__main__":
    r = RSI('603993', '2017-07-04')
    r.getRSI()
    date = r.df.date.values

    for i in range(len(date)):
        print date[i], r.rsi['6'][i], r.rsi['12'][i], r.rsi['24'][i]
