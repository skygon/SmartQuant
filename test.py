import tushare as ts
import time

class Tutorial(object):
    def __init__(self):
        pass
    
    def basic_usage(self):
        self.get_hist_data()

    def getzz500(self):
        df = ts.get_zz500s()
        print type(df)
        print df[['code', 'weight']].head(20)

    def get_hist_data(self):
        start = time.time()
        df = ts.get_k_data('603993', ktype='D')
        print df.shape
        print df.head(20)
        df.to_csv('603993_hist_d.csv', encoding='utf-8')
        end = time.time()
        print "time eclipse: %s" %(end-start)
    
    def get_current_deals(self):
        df = ts.get_today_ticks('603993')

if __name__ == "__main__":
    t = Tutorial()
    t.basic_usage()