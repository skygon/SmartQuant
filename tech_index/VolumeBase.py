#coding=utf-8
import os
import sys
from pandas import DataFrame
sys.path.append(os.getcwd())
from utils import *
from RealTimeDataAcq import RTDA

class VolumeBase(object):
    def __init__(self):
        self.code = "000001"
        self.hist_day_path = os.path.join(os.getcwd(), 'hist_data', 'day')
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
        
        return True

    def isNewStock(self):
        if len(self.close) < 200:
            return True
        return False

    def isStartUp(self):
        if self.code.find("300") == 0:
            return True
        return False
    
    def prepareData(self):
        file_name = self.code + '_hist_d.csv'
        full_path = os.path.join(self.hist_day_path, file_name)

        self.df = DataFrame.from_csv(full_path)
        self.close = self.df.close.values
        self.volume = self.df.volume.values
        self.date = self.df.date.values
    
    def canBuy(self):
        raise Exception("Should not call from VolumeBase")
    
    def analysis(self):
        print "You need to define this function in subclass"


if __name__ == "__main__":
    v = VolumeBase()

