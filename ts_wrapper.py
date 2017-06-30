#coding=utf-8
import os
from pandas import DataFrame
from utils import Utils
import tushare as ts


class TsWrapper(object):
    def __init__(self, code):
        self.code = code
        self.hist_day_data_path = os.path.join(os.getcwd(), 'hist_data', 'day')
    
    def setCode(self, new_code):
        self.code = new_code
    
    def getFullPath(self, ftype='D'):
        if ftype == 'D':
            file_name = self.code + '_hist_d.csv'
        else:
            raise Exception("Invalid file type")
        
        full_path = os.path.join(self.hist_day_data_path, file_name)
        return full_path
    
    # ================START LOGIC==================
    def get_today_deals(self):
        df = ts.get_today_ticks(self.code)
        return df
    
    def get_hist_day_data(self):
        try:
            df = ts.get_k_data(self.code, ktype='D')
            full_path = self.getFullPath()
            Utils.save2CSVFile(df, full_path)
        except Exception, e:
            print "get_hist_day_data failed: %s" %(str(e))
        
    def update_hist_day_data(self):
        full_path = self.getFullPath()
        df = DataFrame.from_csv(full_path)
        last_frame = df.tail(1)
        date_string = last_frame.iloc[0,0] # date is the first cell of on row
        with open(full_path, 'a') as f:
            df = ts.get_k_data(self.code, ktype='D', start=date_string)
            delta_df = df[1:] # first row is duplicated. skip it
            delta_df.to_csv(f)


if __name__ == "__main__":
    tw = TsWrapper('603993')
    #tw = TsWrapper('000001')
    tw.update_hist_day_data()