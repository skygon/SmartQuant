import os
import talib as ta
from pandas import DataFrame


class KDJ(object):
    def __init__(self, code):
        self.code = code
        self.hist_day_path = os.path.join(os.getcwd(), 'hist_data', 'day')
    
    def setCode(self, code):
        self.code = code

    
    def getKDJ(self):
        file_name = self.code + '_hist_d.csv'
        full_path = os.path.join(self.hist_day_path, file_name)

        df = DataFrame.from_csv(full_path)
        high = df.high.values
        low = df.low.values
        close = df.close.values
        self.date = df.date.values
        # matype: 0=SMA, 1=EMA, 2=WMA, 3=DEMA, 4=TEMA, 5=TRIMA, 6=KAMA, 7=MAMA, 8=T3 (Default=SMA)
        K, D = ta.STOCH(high, low, close, fastk_period=9,slowk_period=3,slowk_matype=0,slowd_period=3,slowd_matype=0)
        return K, D

if __name__ == "__main__":
    kdj = KDJ('603993')
    k, d = kdj.getKDJ()
    for i in range(len(k)):
        print kdj.date[i], k[i], d[i]
    
