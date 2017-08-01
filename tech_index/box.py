#coding=utf-8
import os
import sys
import threading
sys.path.append(os.getcwd())
from VolumeBase import VolumeBase
from RealTimePrice import RealtimePrice
from utils import *


class Box(VolumeBase):
    def __init__(self, start_day=-1):
        self.total = 0
        self.stock_pool = 0
        self.exit_check_price = 0
        self.exit_current_price = 0
        self.exit_uniform_distribute = 0
        self.rt = RealtimePrice()
        self.test = True

        if self.test:
            self.start_day = start_day
            last_days['one'] = self.start_day
        else:
            self.start_day = -1  # we can set this to early days for test

        super(Box, self).__init__()
        self.box_len = 180
        self.partition = 4
        self.max_shake = 0.5
        self.uniform_shake = 0.05
        self.enter = 0.08
        self.getStdDate()


    def getStdDate(self):
        file_name = '601988_hist_d.csv' # china bank
        full_path = os.path.join(self.hist_day_path, file_name)
        df = DataFrame.from_csv(full_path)
        self.std_date = df.date.values
    
    def isNewStock(self):
        if len(self.close) < self.box_len + abs(self.start_day):
            return True
        return False

    
    def checkShake(self):
        try:
            high = []
            low = []
            self.max_high = 0.0
            self.min_low = 0.0
            for i in range(self.start_day, -self.box_len+self.start_day, -1):
                high.append(self.high[i])
                low.append(self.low[i])

            high.sort(reverse=True) # high[0] is the largest
            low.sort() #low[0] is the lowest

            #omit the largest and lowest
            if low[1] == 0:
                return False
            
            if (high[1] - low[1]) / low[1] < self.max_shake:
                self.max_high = high[1]
                self.min_low = low[1]
                return True

            return False
        except Exception, e:
            print "check shake failed %s" %(str(e))
    
    # check if high price exist uniformly
    def uniformDistribute(self):
        try:
            step = self.box_len / self.partition
            lh = []
            for i in range(self.partition):
                high = []
                offset = 1 if i==0 else 0
                start = i * (-step) - offset + self.start_day + 1
                end = (i+1) * (-step) + self.start_day + 1
                for j in range(start, end, -1):
                    high.append(self.high[j])
                    high.sort(reverse=True)
                if abs(high[1] - self.max_high) / self.max_high > self.uniform_shake:
                    return False
                lh.append(high[1])
            #print "three highs: %s" %(lh)
            return True
        except Exception, e:
            print "uniformDistribute failed %s" %(str(e))

    # dict 排序， 选出value 大于 self.max_high * 0.98的所有day_index, 观察是否均匀分布
    def uniformDistribute_2(self):
        try:
            dh_map = {}
            for i in range(self.start_day, -self.box_len+self.start_day, -1):
                dh_map[i] = self.high[i]
            
            # tuple_list is list of tuple, item is (day, price)
            tuple_list = sorted(dh_map.items(), key=lambda x:x[1], reverse=True)
            high_index = []
            for i in range(len(tuple_list)):
                if tuple_list[i][1] >= self.max_high * 0.96:
                    high_index.append(tuple_list[i][0])
            
            # uniform distribute of high_index
            bucket = 4
            samples = 16
            if len(high_index) < samples:
                return False
            
            average = samples / bucket
            step = self.box_len / bucket
            tops = high_index[0:samples]
            dist = {}
            # init dist
            for i in range(bucket):
                dist[i] = 0

            for i in range(samples):
                d = tops[i]
                index = abs(d - self.start_day) / step
                dist[index] += 1

            total = 0
            for i in range(bucket):
                total += pow((dist[i] - average), 2)
            
            if total <= 8:
                print "[%s] dist: %s, total %s" %(self.code, dist, total)
                return True
            
            return False
        except Exception, e:
            print "uniformDistribute_2 failed %s" %(str(e))


    def checkCurrentPriceFake(self):
        cp = self.low[self.start_day]
        if (cp - self.min_low) / self.min_low < self.enter:
            for i in range(2):
                if self.close[self.start_day-i] < self.close[self.start_day-i-1]:
                    return False
            print "high : %s, low : %s, current: %s" %(self.max_high, self.min_low, cp)
            return True
            
        return False

    def checkCurrentPrice(self):
        try:
            if self.code.find("60") == 0:
                c = "sh" + self.code
            else:
                c = "sz" + self.code

            self.rt.setCode(c)
            cp = self.rt.getCurrentPrice()
            if (cp - self.min_low) / self.min_low < self.enter:
                for i in range(2):
                    if self.close[self.start_day-i] < self.close[self.start_day-i-1]:
                        return False

                print "high : %s, low : %s, current: %s" %(self.max_high, self.min_low, cp)
                return True
            
            return False
        except Exception, e:
            print "check current price failed %s" %(str(e))

    def canBuy(self):
        try:
            self.total += 1
            self.prepareData()
            if self.isNewStock():
                return False
            
            if self.invalidCode():
                return False
            
            if self.isStartUp():
                return False

            ret = self.checkShake()
            if ret is False:
                self.exit_check_price += 1
                return False

            ret = self.uniformDistribute_2()
            if ret is False:
                self.exit_uniform_distribute += 1
                return False
            
            #self.uniformDistribute_2()

            if self.test:
                ret = self.checkCurrentPriceFake()
            else:
                ret = self.checkCurrentPrice()
            
            if ret is False:
                self.exit_current_price += 1
                return False
            
            self.stock_pool += 1
            return True
        except Exception, e:
            print "box canBuy failed %s" %(str(e))

    
    def analysis(self):
        print "==== End day: %s" %(self.std_date[-self.box_len+self.start_day])
        print "==== total codes : %s" %(self.total)
        print "==== exit from check price : %s" %(self.exit_check_price)
        print "==== exit from uniform distribute : %s" %(self.exit_uniform_distribute)
        print "==== exit from current price: %s" %(self.exit_current_price)
        print "==== stock pool size is %s" %(self.stock_pool)


class Test(threading.Thread):
    def __init__(self, start_day):
        super(Test, self).__init__()
        self.start_day = start_day
        self.index_obj = Box(start_day)
        self.count = 0
        print self.index_obj.current_date
        self.start()

    def processOneCode(self, code):
        self.index_obj.setCode(code)
        if self.index_obj.canBuy():
            self.count += 1
        
    def handleNumericCode(slef, code):
        c = str(code)
        if len(c) < 6:
            c = "0" * (6 - len(c)) + c
        
        return c

    def singleThread(self):
        full_queue = g_utils.getFullQueIns()
        while True:
            try:
                code = full_queue.get(False)
                code = self.handleNumericCode(code)

                self.processOneCode(code)
            except Queue.Empty:
                print "All works of single index have been done \n"
                break
            except Exception, e:
                print "single index Error : %s \n" %(str(e))
        
        if self.count >= 3:
            print "=== try day: %s ===" %(self.start_day)
    
    def run(self):
        full_queue = g_utils.getFullQueIns()
        while True:
            try:
                code = full_queue.get(False)
                code = self.handleNumericCode(code)

                #print "%s get code %s" %(threading.currentThread().name, code)
                self.processOneCode(code)
            except Queue.Empty:
                print "All works of single index have been done \n"
                break
            except Exception, e:
                print "single index Error : %s \n" %(str(e))
        
        if self.count >= 3:
            print "=== try day: %s ===" %(self.start_day)



if __name__ == "__main__":
    #workers = []
    for i in range(-60, -100, -5):
        t = Test(i)
        t.singleThread()
    
    #for t in workers:
    #    if t.isAlive():
    #        t.join()
        
