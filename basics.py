import os
import tushare as ts

class Basics(object):
    def __init__(self):
        pass
    
    def get_all_stocks_basics(self):
        df = ts.get_stock_basics()
        print df.shape
        print df.head(20)
        df.to_csv('stock_basics.csv', encoding='utf-8')
    

if __name__ == "__main__":
    b = Basics()
    b.get_all_stocks_basics()