from pandas import DataFrame
import tushare as ts
import time
import os

class Tutorial(object):
    def __init__(self):
        self.path = os.getcwd()
    
    def parseStockBasics(self):
        full_path = os.path.join(self.path, 'config', 'stock_basics.csv')
        df = DataFrame.from_csv(full_path)
        #print u'603933' == '603933'
        return df
    
    def parseSZ50(self):
        full_path = os.path.join(self.path, 'config', 'sz50.csv')
        df = DataFrame.from_csv(full_path)
        return df
        #print df[df.code.isin(['600016','600028'])]
    
    def parseHS300(self):
        full_path = os.path.join(self.path, 'config', 'hs300.csv')
        df = DataFrame.from_csv(full_path)
        #print df.code
        #print df[df.code.isin([600016,'600028'])]
        return df

    def parseZZ500(self):
        full_path = os.path.join(self.path, 'config', 'zz500.csv')
        df = DataFrame.from_csv(full_path)
        print df.code
        print df[df.code.isin([600993, '002277'])]
    
    def getDeltaHistData(self):
        df = ts.get_k_data('603993', ktype='D', start='2017-06-28')
        ndf = df.set_index([[0,1]])
        #ndf = df.reset_index()
        print ndf
    
    def getTickData(self):
        df = ts.get_k_data('603993', ktype='5', start='2017-07-18', end='2017-07-18')
        return df

if __name__ == "__main__":
    t = Tutorial()
    df = t.getTickData()
    #print df.head(10)
    #print df.code.isin(['603993'])
    print df[df.date.str.contains('2017-07-18')]
    