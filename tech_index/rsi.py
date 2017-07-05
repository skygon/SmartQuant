import os
import talib as ta
from pandas import DataFrame

class RSI(object):
    def __init__(self, code):
        self.code = code
        self.hist_day_path = os.path.join(os.getcwd(), 'hist_data', 'day')

    def setCode(self, code):
        self.code = code

    def getRSI(self):
        file_name = self.code + '_hist_d.csv'
        full_path = os.path.join(self.hist_day_path, file_name)
        self.df = DataFrame.from_csv(full_path)
        close = self.df.close.values
        rsi = {}
        rsi['6'] = ta.RSI(close, timeperiod=6)
        rsi['12'] = ta.RSI(close, timeperiod=12)
        rsi['24'] = ta.RSI(close, timeperiod=24)
        return rsi
    

if __name__ == "__main__":
    r = RSI('603993')
    rsi = r.getRSI()
    date = r.df.date.values

    for i in range(len(date)):
        print date[i], rsi['6'][i], rsi['12'][i], rsi['24'][i]
