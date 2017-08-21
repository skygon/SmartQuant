#encoding=utf-8
import os
import sys
import threading
import Queue
import requests
import time
from pandas import DataFrame
sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), 'tech_index'))
sys.path.append(os.path.join(os.getcwd(), 'information_service'))


from TickPrice import TickPrice
from WatchDog import WatchDog
from shake import Shake
from box import Box
from message_pusher import Pusher
import utils

class LowOpen(threading.Thread):
    def __init__(self):
        super(LowOpen, self).__init__()
        self.start_day = -1
        self.mock_code = ""
        self.hist_data_path = os.path.join(os.getcwd(), 'hist_data', 'day')

    def isLowOpenTest(self):
        file_name = self.mock_code + "_hist_d.csv"
        f = os.path.join(self.hist_data_path, file_name)
        if os.path.isfile(f) is False:
            return
        else:
            df = DataFrame.from_csv(f)
        
        c = df.close.values
        o = df.open.values
        date = df.date.values

        if len(date) <= 100:
            return

        if o[self.start_day] == 0 or c[self.start_day-1] == 0:
            return

        if o[self.start_day] / c[self.start_day-1] <= 0.96:
            print "[%s] -> [%s] open at low price: %s" %(date[self.start_day], self.mock_code, o[-1])


    def run(self):
        while True:
            try:
                c = utils.g_utils2.full_queue.get(False)
                self.mock_code = c
                if c.find("300") == 0:
                    continue
                if c.find("60") == 0:
                    c = "sh" + c
                else:
                    c = "sz" + c
                
                self.isLowOpenTest()
            except Queue.Empty:
                print "queue empty"
                break
            except Exception, e:
                print "low open watcher failed %s" %(str(e))


if __name__ == "__main__":
    lp = LowOpen()
    lp.start()
    lp.join()