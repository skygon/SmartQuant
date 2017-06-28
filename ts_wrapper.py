#coding=utf-8
import os
import tushare as ts


class TsWrapper(object):
    def __init__(self, code):
        self.code = code
    
    def setCode(self, new_code):
        self.code = new_code
    
    def get_current_deals(self):
        df = ts.get_today_ticks(self.code)
        return df



if __name__ == "__main__":
    tw = TsWrapper('603993')
    df = tw.get_current_deals()
    print df.shape
    print df.head(20)
    
    s = df.iloc[1,6]
    print type(s)
    #print s
    df.to_csv('data.csv', encoding='utf-8')