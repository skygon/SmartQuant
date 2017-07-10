import os
import sys
from pandas import DataFrame
sys.path.append(os.getcwd())
from utils import *


class Volume(object):
    def __init__(self, code):
        self.code = code
        self.hist_day_path = os.path.join(os.getcwd(), 'hist_data', 'day')
        self.total = 0
        self.exit_invalid_code = 0
        self.stock_pool = 0
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
    
    def quickIncVolume(self):
        ma = self.getVolumeMA(last_days['one']-1)
        if float(self.volume[last_days['one']]) / self.volume[last_days['one']-1] < 2.0:
            return False
        
        if float(self.volume[last_days['one']]) / ma < 2.0:
            return False
        
        return True

    def canBuy(self):
        try:
            self.prepareData()
            if self.invalidCode():
                self.exit_invalid_code += 1
                return False
            
            if self.quickIncVolume() is False:
                return False
            
            self.stock_pool += 1
            return True
        except Exception, e:
            print "canBuy failed %s" %(str(e))

    def analysis(self):
        print "==== total codes : %s" %(self.total)
        print "==== exit from invalid code : %s" %(self.exit_invalid_code)
        print "==== stock pool size is %s" %(self.stock_pool)


if __name__ == "__main__":
    v = Volume('603993')
    for i in range(10):
        last_days['one'] = -1 - i
        ma = v.getVolumeMA(5)
        print v.date[last_days['one']], ma


    

    


