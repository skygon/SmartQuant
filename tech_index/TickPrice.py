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
        self.up = {}
        self.down = {}
        # for strategy statistic
        self.total = 0
        self.stock_pool = 0
        self.exit_count = 0
        self.exit_price = 0
        self.exit_volume = 0
        self.initStatisticData()

    def setDate(self, date_str):
        self.date_str = date_str

    def initStatisticData(self):
        self.up['count'] = 0
        self.up['price'] = 0
        self.up['volume'] = 0

        self.down['count'] = 0
        self.down['price'] = 0
        self.down['volume'] = 0

    # override base class. And before invoke, must setCode
    def prepareData(self):
        df = self.ts.getTick5Data(self.code, self.current_date)
        self.df = df[df.date.str.contains(self.current_date)]
        # save to disk for cache and regression test
        file_name = self.code + ".csv"
        f = os.path.join(self.tick_data_path, file_name)
        self.df.to_csv(f)
    
    def prepareDataFromDisk(self):
        file_name = self.code + ".csv"
        f = os.path.join(self.tick_data_path, file_name)
        df = DataFrame.from_csv(f)
        self.df = df[df.date.str.contains(self.current_date)]

    
    def getSummary(self):
        self.date = self.df.date.values
        self.open = self.df.open.values
        self.close = self.df.close.values
        self.high = self.df.high.values
        self.low = self.df.low.values
        self.volume = self.df.volume.values

        self.length = len(self.date)
        for i in range(self.length):
            if self.open[i] >= self.close[i]:
                self.down['count'] += 1
                self.down['price'] += (self.open[i] - self.close[i])
                self.down['volume'] += self.volume[i]
            else:
                self.up['count'] += 1
                self.up['price'] += (self.close[i] - self.open[i])
                self.up['volume'] += self.volume[i]

        # print "===== total[%s] / up[%s] / down[%s] =====" %(self.length, self.up['count'], self.down['count'])
        # print "===== Price change: total[%s] / up[%s] / down[%s] =====" %((self.close[self.length-1] - self.open[0]), self.up['price'], self.down['price'])
        # print "===== up volume : %s ======== down volume :: %s" %(self.up['volume'], self.down['volume'])


    def simple_1(self):
        if self.down['count'] == 0:
            return True
        
        if self.up['count'] / float(self.down['count']) < 1.3:
            self.exit_count += 1
            return False
       
        if self.up['price'] < self.down['price']:
            self.exit_price += 1
            return False
       
        if self.up['volume'] / self.down['volume'] < 1.5:
            self.exit_volume += 1
            return False

        return True

    
    def canBuy(self):
        try:
            self.prepareDataFromDisk()
            self.getSummary()
            return self.simple_1()
        except Exception, e:
            print "TickPrice-> canBuy exception [%s]" %(str(e))
    
    
    def analysis(self):
        print "==== total codes : %s" %(self.total)
        print "==== exit from count : %s" %(self.exit_count)
        print "==== exit from price : %s" %(self.exit_price)
        print "==== exit from volume : %s" %(self.exit_volume)
        print "==== stock pool : %s" %(self.stock_pool)

if __name__ == "__main__":
    t = TickPrice('2017-07-20')
    t.setCode('603993')
    t.prepareDataFromDisk()
    print t.df
    t.getSummary()
    