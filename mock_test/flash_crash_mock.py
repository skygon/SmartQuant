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
from TickPrice import TickPrice
import utils
from utils import *


class FlashCrashMock(TickPrice):
    def __init__(self):
        super(FlashCrashMock, self).__init__("")
        self.start_index = -5
        self.days = 5

    def getBestSet(self):
        for i in range(self.days):
            mock_full_queue = g_utils.getFullQueIns()
            utils.start_day = self.start_index - i
            utils.last_days['one'] = utils.start_day + 3
            self.getCurrentDate()
            print self.current_date
            while True:
                try:
                    c = mock_full_queue.get(False)
                    if c.find('300') == 0:
                        continue
                    self.setCode(c)
                    self.prepareDataFromDisk()
                    code, l, tick = self.findCrash()
                    if code is None:
                        continue

                    #print "find some results %s %s" %(code, l)
                    close, high = self.getNextDayInfo()
                    if close is None:
                        continue
                    if l / high < 0.97:
                        print "*** [%s][%s] can buy at price %s -> [%s] ***" %(tick, code, l, high)
                    
                except Queue.Empty:
                    break
                except Exception, e:
                    print "getBestSet failed %s" %(str(e))
        print "==== All Finished ==="

if __name__ == "__main__":
    f = FlashCrashMock()
    f.getBestSet()
    
