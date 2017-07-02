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
    
    def getFullPath(self, appendix, ftype='D'):
        file_name = self.code + appendix
        if ftype == 'D':
            full_path = os.path.join(self.hist_day_data_path, file_name)    
        else:
            raise Exception("Invalid file type")     
        
        return full_path
    
    def addSepToFirstLine(self, full_path):
        all_lines = []
        with open(full_path, 'r') as f:
            all_lines = f.readlines()
        
        line = all_lines[0]
        new_line = "," + line
        all_lines[0] = new_line

        with open(full_path, 'w') as f:
            for l in all_lines:
                f.write(l)
    
    # ================START LOGIC==================
    def get_today_deals(self):
        df = ts.get_today_ticks(self.code)
        return df
    
    def get_hist_day_data(self):
        try:
            df = ts.get_k_data(self.code, ktype='D')
            full_path = self.getFullPath('_hist_d.csv')
            Utils.save2CSVFile(df, full_path)
        except Exception, e:
            print "get_hist_day_data failed: %s" %(str(e))
    
    def get_hist_day_data_2(self):
        try:
            df = ts.get_hist_data(self.code, ktype='D')
            df = df.iloc[::-1]
            full_path = self.getFullPath('_hist_d_2.csv')
            Utils.save2CSVFile(df, full_path)
            self.addSepToFirstLine(full_path)
        except Exception, e:
            print "get_hist_day_data_2 failed: %s" %(str(e))
    

    def update_hist_day_data(self):
        full_path = self.getFullPath('_hist_d.csv')
        df = DataFrame.from_csv(full_path)
        last_frame = df.tail(1)
        date_string = last_frame.iloc[0,0] # date is the first cell of on row
        offset = df.shape[0]
        print "offset is %s" %(offset)
        
        with open(full_path, 'w') as f:
            new_df = ts.get_k_data(self.code, ktype='D', start=date_string)
            delta_df = new_df[1:] # first row is duplicated. skip it
            print delta_df.shape
            delta_len = delta_df.shape[0]
            print "delta len is %s" %(delta_len)
            delta_index = [i + offset for i in range(delta_len)]
            print delta_index
            delta_df = delta_df.set_index([delta_index])
            ndf = df.append(delta_df)
            ndf.to_csv(f)
            


if __name__ == "__main__":
    #tw = TsWrapper('603993')
    tw = TsWrapper('000001')
    tw.get_hist_day_data_2()