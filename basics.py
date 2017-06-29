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


    def get_all_stocks_basics(self):
        df = ts.get_stock_basics()
        print df.shape
        print df.head(20)
        df.to_csv('stock_basics.csv')
    

if __name__ == "__main__":
    b = Basics()
    b.insertIndex('stock_basics.csv', 'stock_basic_refine.csv')