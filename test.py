import tushare as ts

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
        df = ts.get_k_data('603993', ktype='D', start='2017-06-26', end='2017-06-28')
        print df
    
    def get_current_deals(self):
        df = ts.get_today_ticks('603993')

if __name__ == "__main__":
    t = Tutorial()
    t.basic_usage()