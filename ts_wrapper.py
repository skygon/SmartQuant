#coding=utf-8
import os
import tushare as ts


class TsWrapper(object):
    def __init__(self, code):
        self.code = code
        self.hist_day_data_path = os.path.join(os.getcwd(), 'hist_day_data')
    
    def setCode(self, new_code):
        self.code = new_code
    
    def get_today_deals(self):
        df = ts.get_today_ticks(self.code)
        return df
    
    def get_hist_day_data(self):
        try:
            df = ts.get_k_data(self.code, ktype='D')
            file_name = self.code + '_hist_d.csv'
            full_path = os.path.join(self.hist_day_data_path, file_name)
            df.to_csv(full_path, encoding='utf-8')
        except Exception, e:
            print "get_hist_day_data failed: %s" %(str(e))




if __name__ == "__main__":
    tw = TsWrapper('603993')
    df = tw.get_today_deals()
    print df.shape
    print df.head(20)
    
    s = df.iloc[1,6]
    print type(s)
    #print s
    df.to_csv('data.csv', encoding='utf-8')