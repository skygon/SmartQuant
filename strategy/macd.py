import os
import talib
import matplotlib.pyplot as plt
from pandas import DataFrame

class MACD(object):
    def __init__(self, code):
        self.code = code
        self.hist_day_path = os.path.join(os.getcwd(), 'hist_data', 'day')
    
    def setCode(self):
        self.code = code
    
    def getMACD(self):
        file_name = self.code + '_hist_d.csv'
        full_path = os.path.join(self.hist_day_path, file_name)
        df = DataFrame.from_csv(full_path)
        close = df.close.values
        dif, dea, macd = talib.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
        return dif, dea, macd

class StrategyMACD(object):
    def __init__(self, code):
        self.code = code

if __name__ == "__main__":
    m = MACD('603993')
    dif, dea, macd = m.getMACD()
    for i in range(len(dif)):
        print "DIF: %s, DEA: %s, MACD: %s" %(dif[i], dea[i], 2*macd[i])
    
    
    
