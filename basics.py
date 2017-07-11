import os
import tushare as ts

class Basics(object):
    def __init__(self):
        pass
    
    def insertIndex(self, in_file, out_file):
        f = open(in_file, 'r')
        out = open(out_file, 'w')
        line = f.readline()
        new_line = "," + line
        out.write(new_line)
        line = f.readline()
        count = 0
        while line:
            new_line = str(count) + "," + line
            out.write(new_line)
            line = f.readline()
            count += 1
        f.close()
        out.close()

    # get the whole market stock information.
    def get_all_stocks_basics(self):
        df = ts.get_stock_basics()
        print df.shape
        print df.head(20)
        df.to_csv('stock_basics.csv')

    # shang zheng 50
    def get_sz50(self):
        df = ts.get_sz50s()
        #print df
        print df.head(20)
        df.to_csv('sz50.csv', encoding='utf-8')
    
    # hu sheng 300
    def get_hs300(self):
        df = ts.get_hs300s()
        df.to_csv('hs300.csv')
    
    # zhong zheng 500
    def get_zz500(self):
        df = ts.get_zz500s()
        print df
        #df.to_csv('zz500.csv')

    def get_startUp(self):
        df = ts.get_gem_classified()
        df.to_csv('startup.csv')

if __name__ == "__main__":
    b = Basics()
    #b.get_zz500()
    b.get_startUp()