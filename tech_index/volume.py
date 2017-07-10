#coding=utf-8
import os
import sys
from pandas import DataFrame
sys.path.append(os.getcwd())
from utils import *
from RealTimeDataAcq import RTDA

'''
以前一天的为量能突破分析的起始点，往前倒推。同时结合当前的K线和成交量等数据分析走势
'''
class Volume(object):
    def __init__(self, code):
        self.code = code
        self.hist_day_path = os.path.join(os.getcwd(), 'hist_data', 'day')
        self.total = 0
        self.exit_invalid_code = 0
        self.exit_motivation_break = 0
        self.exit_big_bill = 0
        self.stock_pool = 0
        self.rtda = RTDA()
        self.getCurrentDate()

    def setCode(self, code):
        self.code = code
    
    def getCurrentDate(self):
        file_name = '601988_hist_d.csv' # china bank
        full_path = os.path.join(self.hist_day_path, file_name)
        df = DataFrame.from_csv(full_path)
        self.current_date = df.date.values[last_days['one']]
    
    def invalidCode(self):
        today = self.df.date.values[last_days['one']]
        if today == self.current_date:
            return False
        
        self.exit_invalid_code += 1
        return True

    def isNewStock(self):
        if len(self.close) < 200:
            return True
        return False
    
    def prepareData(self):
        file_name = self.code + '_hist_d.csv'
        full_path = os.path.join(self.hist_day_path, file_name)

        self.df = DataFrame.from_csv(full_path)
        self.close = self.df.close.values
        self.volume = self.df.volume.values
        self.date = self.df.date.values

    def getVolumeMA(self, day_index, interval=5):
        try:
            total = 0
            for i in range(interval):
                total += self.volume[day_index - i]
            
            ma = float(total) / interval
            return ma
        except Exception, e:
            print "getVolumeMA failed %s" %(str(e))
    
    def quickIncVolume(self, day_index):
        try:
            ma = self.getVolumeMA(day_index-1)
            if ma == 0:
                return False
            # special stop stock
            if self.volume[day_index-1] == 0:
                return False
            
            if float(self.volume[day_index]) / self.volume[day_index-1] < 2.0:
                return False
            
            if float(self.volume[day_index]) / ma < 2.0:
                return False
            
            return True
        except Exception, e:
            print "quickIncCVolume failed %s" %(str(e))
            return False

    def motivationBreak(self):
        for i in range(4, 30):
            if self.quickIncVolume(last_days['one'] - i):
                if self.close[last_days['one']] > self.close[last_days['one']-i]:
                    return True

        return False
    
    def positiveBigBill(self, day_index):
        try:
            if self.code.find("60") == 0:
                code = "sh" + self.code
            else:
                code = "sz" + self.code
            
            self.rtda.setCode(code)
            self.rtda.setDate(self.date[day_index])
            self.rtda.setParams('bill', amount=200*100*100, type=0)
            data = self.rtda.getBillListSummary()
            if data is None:
                return True
            
            if data[0]['kuvolume'] < data[0]['kdvolume']:
                return False
            #if float(data[0]['kuvolume']) == 0:
            #    return False
            
            #if float(data[0]['kdvolume']) / float(data[0]['kuvolume']) > 1.2:
            #    return False
            
            return True
        except Exception, e:
            print "positiveBigBill failed %s" %(str(e))
            return False
    
    #量能突破后，连续两天外盘大单占多
    def conPositiveBigBill(self):
        if self.positiveBigBill(last_days['one']) is False:
            return False
        
        if self.positiveBigBill(last_days['one'] + 1) is False:
            return False
        
        return True
    
    def canBuy(self):
        try:
            self.prepareData()
            if self.invalidCode() or self.isNewStock():
                self.exit_invalid_code += 1
                return False
            
            if self.quickIncVolume(last_days['one']) is False:
                return False
            
            if self.motivationBreak() is False:
                self.exit_motivation_break += 1
                return False
            
            if self.conPositiveBigBill() is False:
                self.exit_big_bill += 1
                return False



            self.stock_pool += 1
            return True
        except Exception, e:
            print "canBuy failed %s" %(str(e))
            return False

    def analysis(self):
        print "==== total codes : %s" %(self.total)
        print "==== exit from invalid code : %s" %(self.exit_invalid_code)
        print "==== exit from motivation break : %s" %(self.exit_motivation_break)
        print "==== exit from positive big bill : %s" %(self.exit_big_bill)
        print "==== stock pool size is %s" %(self.stock_pool)


if __name__ == "__main__":
    v = Volume('603993')
    for i in range(10):
        last_days['one'] = -1 - i
        ma = v.getVolumeMA(5)
        print v.date[last_days['one']], ma


    

    


