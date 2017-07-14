import os
import threading
import Queue
from ts_wrapper import TsWrapper
import pandas
from utils import *

thread_poll_num = 300

class DataCollector(threading.Thread):
    def __init__(self, t='hist_day'):
        threading.Thread.__init__(self)
        self.type = t
        self.hist_day_path = os.path.join(os.getcwd(), 'hist_data', 'day')
        self.ts = TsWrapper('000001')
        #self.start()

    
    def processOneCode(self, code):
        self.ts.setCode(code)
        if self.type == 'hist_day':
            self.ts.get_hist_day_data()
        elif self.type == 'hist_day_2':
            self.ts.get_hist_day_data_2()
        elif self.type == 'update_hist_day':
            self.ts.update_hist_day_data()
        elif self.type == 'upadte_hist_day_2':
            self.ts.update_hist_day_data_2()
    

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
        t.start()
        if t.isAlive():
            t.join()


def updateToday(date_str):
    dc = DataCollector()
    df = dc.ts.get_today_all()
    df.to_csv('today_all.csv', encoding='utf-8')

    df = DataFrame.from_csv('today_all.csv', encoding='utf-8')
    code = df.code.values
    close = df.trade.values
    open = df.open.values
    high = df.high.values
    low = df.low.values
    volume = df.volume.values
    for i in range(len(code)):
        try:
            c = str(code[i])
            if len(c) < 6:
                c = "0" * (6 - len(c)) + c
            file_name = c + '_hist_d.csv'
            full_path = os.path.join(dc.hist_day_path, file_name)
            df = DataFrame.from_csv(full_path)
            last_frame = df.tail(1)
            offset = df.shape[0]

            date_string = last_frame.iloc[0,0] # date is the first cell of on row
            if (date_string == date_str):
                continue
            
            print "offset is %s" %(offset)
            data = {}
            data['date'] = [date_str]
            data['open'] = [open[i]]
            data['close'] = [close[i]]
            data['high'] = [high[i]]
            data['low'] = [low[i]]
            data['volume'] = [float(volume[i]) / 100]
            data['code'] = [c]

            delta_df = DataFrame.from_dict(data)
            delta_df = delta_df[['date', 'open', 'close', 'high', 'low', 'volume', 'code']]
            delta_df = delta_df.set_index([[offset]])
            delta_df.to_csv(full_path, mode='a', header=None)
            
        except Exception, e:
            print "updateHistDayRealTime error: %s" %(str(e))


def updateTodayRealTime(date_str):
    dc = DataCollector()
    #df = dc.ts.get_today_all()
    #df.to_csv('today_all.csv', encoding='utf-8')

    df = DataFrame.from_csv('today_all.csv', encoding='utf-8')
    code = df.code.values
    close = df.trade.values
    open = df.open.values
    high = df.high.values
    low = df.low.values
    volume = df.volume.values
    for i in range(len(code)):
        try:
            c = str(code[i])
            if len(c) < 6:
                c = "0" * (6 - len(c)) + c
            file_name = c + '_hist_d.csv'
            full_path = os.path.join(dc.hist_day_path, file_name)
            df = DataFrame.from_csv(full_path)
            last_frame = df.tail(1)
            offset = df.shape[0]

            data = {}
            data['date'] = [date_str]
            data['open'] = [open[i]]
            data['close'] = [close[i]]
            data['high'] = [high[i]]
            data['low'] = [low[i]]
            data['volume'] = [float(volume[i]) / 100]
            data['code'] = [c]

            delta_df = DataFrame.from_dict(data)
            delta_df = delta_df[['date', 'open', 'close', 'high', 'low', 'volume', 'code']]

            date_string = last_frame.iloc[0,0] # date is the first cell of on row
            if (date_string == date_str):
                # update today's data
                delta_df = delta_df.set_index([[offset-1]], inplace=True)
                df.update(delta_df)
                df.to_csv(full_path)
            
            else:
                # first time update, just append to the origin file
                delta_df = delta_df.set_index([[offset]])
                delta_df.to_csv(full_path, mode='a', header=None)
            
        except Exception, e:
            print "updateHistDayRealTime error: %s" %(str(e))


if __name__ == "__main__":
    #getHistDay_2('update_hist_day')
    #updateToday('2017-07-14')
    updateTodayRealTime('2017-07-14')