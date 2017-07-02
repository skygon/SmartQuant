import threading
import Queue
from ts_wrapper import TsWrapper
from utils import *

thread_poll_num = 300

class DataCollector(threading.Thread):
    def __init__(self, t='hist_day'):
        threading.Thread.__init__(self)
        self.type = t
        self.ts = TsWrapper('000001')
        self.start()

    
    def processOneCode(self, code):
        self.ts.setCode(code)
        if self.type == 'hist_day':
            self.ts.get_hist_day_data()
        elif self.type == 'hist_day_2':
            self.ts.get_hist_day_data_2()
    

    def run(self):
        while True:
            try:
                code = g_utils.full_queue.get(False)
                print "I get code %s" %(code)
                self.processOneCode(code)
            except Queue.Empty:
                print "All works of DataCollection have been done \n"
                break
            except Exception, e:
                print "DataCollection Error : %s \n" %(str(e))


def getHistDay_2(t):
    threads = []
    for i in range(thread_poll_num):
        dc = DataCollector(t)
        threads.append(dc)
    
    for t in threads:
        if t.isAlive():
            t.join()

if __name__ == "__main__":
    getHistDay_2('hist_day')