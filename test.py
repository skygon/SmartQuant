from pandas import DataFrame
import tushare as ts
import time
import os

class Tutorial(object):
    def __init__(self):
        self.path = os.getcwd()
    
    def parseStockBasics(self):
        full_path = os.path.join(self.path, 'config', 'stock_basics_refine.csv')
        df = DataFrame.from_csv(full_path)
        print type(df)
        print type(df.code)
        print df.dtypes
        print df.code.iloc[0]
        #print u'603933' == '603933'
        print df[df['code'].isin(['603933', '603993'])]
    
    def parseSZ50(self):
        full_path = os.path.join(self.path, 'config', 'sz50.csv')
        df = DataFrame.from_csv(full_path)
        print df.code
        print df[df.code.isin([600016,'600028'])]
        #print df[df.code.isin(['600016','600028'])]
    
    def parseHS300(self):
        full_path = os.path.join(self.path, 'config', 'hs300.csv')
        df = DataFrame.from_csv(full_path)
        #print df.code
        print df[df.code.isin([600016,'600028'])]

    def parseZZ500(self):
        full_path = os.path.join(self.path, 'config', 'zz500.csv')
        df = DataFrame.from_csv(full_path)
        print df.code
        print df[df.code.isin([600993, '002277'])]
    
    def getDeltaHistData(self):
        df = ts.get_k_data('603993', ktype='D', start='2017-06-28')
        print type(df[1:])
        print df.tail(1).iloc[0,0]

if __name__ == "__main__":
    t = Tutorial()
    #t.parseStockBasics()
    t.getDeltaHistData()