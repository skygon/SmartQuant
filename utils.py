import os
import Queue
from pandas import DataFrame


class Utils(object):
    cfg_path = os.path.join(os.getcwd(), 'config')
   
    def __init__(self):
        # config files:
        self.sh_a = os.path.join(self.cfg_path, 'sh_a.txt')
        self.sz_a = os.path.join(self.cfg_path, 'sz_a.txt')
        # queues. full_queue is used for multithreading workers to process code sets.
        # Thus it's should be a singlton queue. Used from g_utils
        self.full_queue = Queue.Queue()
        self.read_to_queue(self.sh_a, self.full_queue)
        self.read_to_queue(self.sz_a, self.full_queue)
    
    @staticmethod
    def save2CSVFile(df, full_path, enc='utf-8'):
        df.to_csv(full_path, encoding=enc)

    def read_to_queue(self, file_name, que):
        with open(file_name, 'r') as f:
            line = f.readline()
            while line:
                code = line.strip('\n')
                self.full_queue.put(code)
                line = f.readline()
    @staticmethod
    def getHS300Queue():
        que = Queue.Queue()
        full_path = os.path.join(Utils.cfg_path, 'hs300.csv')
        df = DataFrame.from_csv(full_path)
        codes = df.code.values
        for c in codes:
            que.put(c)
        
        return que

    @staticmethod
    def getZZ500Queue():
        que = Queue.Queue()
        full_path = os.path.join(Utils.cfg_path, 'zz500.csv')
        df = DataFrame.from_csv(full_path)
        codes = df.code.values
        for c in codes:
            que.put(c)
        
        return que
    
    @staticmethod
    def getHS300AndZZ500():
        que1 = Utils.getHS300Queue()
        que2 = Utils.getZZ500Queue()
        while True:
            try:
                code = que2.get(False)
                que1.put(code)
            except Queue.Empty:
                break
        
        return que1

g_utils = Utils()


if __name__ == "__main__":
    que = Utils.getHS300AndZZ500()
    print que.qsize()