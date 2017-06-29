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

if __name__ == "__main__":
    t = Tutorial()
    t.parseStockBasics()