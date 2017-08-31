#coding=utf-8
import os
import sys
from pandas import DataFrame
sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), 'information_service'))
from ts_wrapper import TsWrapper
from utils import *
from RealTimeDataAcq import RTDA
from VolumeBase import VolumeBase
from hot_industry import HotIndustry


class TickPrice(VolumeBase):
    def __init__(self, date_str):
        super(TickPrice, self).__init__()
        self.ts = TsWrapper('-1')
        # override base class
        self.current_date = date_str
        self.tick_data_path = os.path.join(os.getcwd(), 'tick_data')
        self.hist_day_path = os.path.join(os.getcwd(), 'hist_data', 'day')
        self.up = {}
        self.down = {}
        # for strategy statistic
        self.total = 0
        self.stock_pool = 0
        self.exit_count = 0
        self.exit_price = 0
        self.exit_volume = 0
        self.accept_no_down_count = 0
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
    
    def getNextDayInfo(self):
        try:
            file_name = self.code + '_hist_d.csv'
            full_path = os.path.join(self.hist_day_path, file_name)
            df = DataFrame.from_csv(full_path)
            close = df.close.values
            high = df.high.values
            date = df.date.values
            if len(date) < 100:
                return None, None
            #print "next date : %s" %(date[last_days['one']+1])
            return close[last_days['one']+1], high[last_days['one']+1]
            
        except Exception, e:
            print "get next day info failed %s" %(str(e))

    def getSettlement(self):
        try:
            file_name = self.code + '_hist_d.csv'
            full_path = os.path.join(self.hist_day_path, file_name)
            df = DataFrame.from_csv(full_path)
            close = df.close.values
            if len(close) < 100:
                return 0
            self.settlement = close[last_days['two']]
            return close[last_days['two']]
        except Exception, e:
            print "getSettlement faield %s" %(str(e))


    def findDownBoard(self):
        try:
            board_price = self.settlement * 0.905
            board = False
            if len(self.tick) == 0:
                return
            
            for i in range(len(self.tick)):
                h = self.high[i]
                l = self.low[i]
                o = self.open[i]
                c = self.close[i]
                if board:
                    if l > board_price:
                        print "**** [%s] open board at %s ****" %(self.code, self.tick[i])
                        return
                elif h == l and c <= board_price:
                    print "[%s] on board" %(self.code)
                    board = True
        except Exception, e:
            print "find open board failed %s" %(str(e))

    def findOpenBoard(self):
        try:
            board_price = self.settlement * 1.1
            board = False
            if len(self.tick) == 0:
                return
            
            for i in range(len(self.tick)):
                h = self.high[i]
                l = self.low[i]
                o = self.open[i]
                c = self.close[i]
                if board:
                    if l < board_price:
                        print "**** [%s] open board at %s ****" %(self.code, self.tick[i])
                        return
                elif h == l and c >= board_price:
                    #print "[%s] on board" %(self.code)
                    board = True
        except Exception, e:
            print "find open board failed %s" %(str(e))


    def prepareTickData(self):
        file_name = self.code + ".csv"
        f = os.path.join(self.tick_data_path, file_name)
        if os.path.isfile(f) is False:
            df = DataFrame()
        else:
            df = DataFrame.from_csv(f)
        self.tick_df = [] if df.empty else df[df.date.str.contains(self.current_date)]
        self.tick_high = [] if df.empty else self.tick_df.high.values
        self.tick_low = [] if df.empty else self.tick_df.low.values
        self.tick_open = [] if df.empty else self.tick_df.open.values
        self.tick_close = [] if df.empty else self.tick_df.close.values
        self.tick = [] if df.empty else self.tick_df.date.values

    def getMA(self, days):
        try:
            start = last_days['one']
            end = last_days['one'] - days
            total = 0.0
            for i in range(start, end, -1):
                total += self.close[i]
            ma = total / days
            return ma
        except Exception,e:
            print "getMA failed %s" %(str(e))
    # Currnetly, we only have the 5 min tick data. So there are 48 ticks in one day
    def findCrash(self):
        try:
            self.prepareData()
            if len(self.date) < 100:
                return

            #ma = self.getMA(15)
            #if self.low[last_days['one']] < ma:
            #    return

            if len(self.tick) == 0:
                return None, None, None
            th = self.tick_open[0]


            for i in range(len(self.tick)):
                h = self.tick_high[i]
                l = self.tick_low[i]
                o = self.tick_open[i]
                c = self.tick_close[i]
                if h == 0:
                    return None, None, None

                #if float(o) / th > 1.02 or float(o) / th < 0.98:
                #    return

                if l / h <= 0.97 and o >= c:
                    if self.code in g_utils.hot_codes:
                        print "**** code[%s] crash at %s -> open[%s], close[%s], high[%s], low[%s]****" %(self.code, self.tick[i], o, c, h, l)
                    else:
                        print "++++ find code[%s] crash. But not in hot industry ++++" %(self.code)    
                    #print "**** code[%s] crash at %s -> open[%s], close[%s], high[%s], low[%s]****" %(self.code, self.tick[i], o, c, h, l)
                    return self.code, l, self.tick[i]

            return None, None, None
        except Exception, e:
            print "find crash failed %s" %(str(e))
            
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

        print "===== total[%s] / up[%s] / down[%s] =====" %(self.length, self.up['count'], self.down['count'])
        print "===== Price change: total[%s] / up[%s] / down[%s] =====" %((self.close[self.length-1] - self.open[0]), self.up['price'], self.down['price'])
        print "===== up volume : %s ======== down volume :: %s" %(self.up['volume'], self.down['volume'])


    def simple_1(self):
        self.total += 1
        if self.down['count'] == 0:
            if self.up['count'] == 0:
                return False
            
            self.accept_no_down_count += 1
            self.stock_pool += 1
            return True
        
        if self.up['count'] / float(self.down['count']) < 1.5:
            #print "up : %s down : %s" %(self.up['count'], self.down['count'])
            self.exit_count += 1
            return False
       
        if self.up['price'] < self.down['price']:
            self.exit_price += 1
            return False
       
        if self.up['volume'] / self.down['volume'] < 1.5:
            self.exit_volume += 1
            return False
        
        self.stock_pool += 1
        return True

    
    def canBuy(self):
        try:
            self.initStatisticData()
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
        print "==== accept because no down count: %s" %(self.accept_no_down_count)
        print "==== stock pool : %s" %(self.stock_pool)

def crash_monitor():
    hi = HotIndustry()
    hi.oneTimeRun()

    t = TickPrice('2017-08-29')
    #t = TickPrice("")
    #t.getCurrentDate()
    print t.current_date
    while True:
        try:
            c = g_utils.full_queue.get(False)
            t.setCode(c)
            t.prepareTickData()
            t.findCrash()
        except Queue.Empty:
            break
        except Exception,e:
            print "monitor error %s" %(str(e))


def open_board():
    t = TickPrice(last_days['one'])
    t.getCurrentDate()
    print t.current_date
    while True:
        try:
            c = g_utils.full_queue.get(False)
            t.setCode(c)
            st = t.getSettlement()
            #print "[%s] settlement: %s" %(t.code, st)
            if st == 0:
                continue
            t.prepareDataFromDisk()
            #t.findOpenBoard()
            t.findDownBoard()
        except Queue.Empty:
            break
        except Exception,e:
            print "monitor error %s" %(str(e))

if __name__ == "__main__":
    crash_monitor()
    #open_board()
    