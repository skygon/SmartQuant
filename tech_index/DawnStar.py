#coding=utf-8
import os
import sys
from pandas import DataFrame
sys.path.append(os.getcwd())
from utils import *
from RealTimeDataAcq import RTDA
from VolumeBase import VolumeBase



class DawnStar(VolumeBase):
    def __init__(self):
        super(Kick, self).__init__()


    def kDawnStar(self):
        if self.checkDay_1() is False:
            return False

        if self.checkDay_2() is False:
            return False
        
        if self.checkDay_3() is False:
            return False
        
        return True
