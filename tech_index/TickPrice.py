#coding=utf-8
import os
import sys
from pandas import DataFrame
sys.path.append(os.getcwd())
from ts_wrapper import TsWrapper
from utils import *
from RealTimeDataAcq import RTDA
from VolumeBase import VolumeBase


class TickPrice(VolumeBase):
    def __init__(self, date_str):
        super(TickPrice, self).__init__()
        self.ts = TsWrapper('-1')
        # override base class
        self.current_date = date_str
        self.tick_data_path = os.path.join(os.getcwd(), 'tick_data')
        self.total = 0
        self.stock_pool = 0


    # override base class. And before invoke, must setCode
    def prepareData(self):
        df = self.ts.getTick5Data(self.code, self.current_date)
        self.df = df[df.date.str.contains(self.current_date)]
        # save to disk for cache and regression test
        file_name = self.code + ".csv"
        f = os.path.join(self.tick_data_path, file_name)
        self.df.to_csv(f)
    
    def canBuy(self):
        try:
            self.prepareData()
        except Exception, e:
            print "TickPrice-> canBuy exception [%s]" %(str(e))
    
    
    def analysis(self):
        print "==== total codes : %s" %(self.total)
        print "==== stock pool : %s" %(self.stock_pool)

if __name__ == "__main__":
    t = TickPrice('2017-07-19')
    t.setCode('603993')
    t.prepareData()
    print t.df