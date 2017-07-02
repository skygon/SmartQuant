import os
import Queue


class Utils(object):
    def __init__(self):
        # config files:
        self.cfg_path = os.path.join(os.getcwd(), 'config')
        self.sh_a = os.path.join(self.cfg_path, 'sh_a.txt')
        self.sz_a = os.path.join(self.cfg_path, 'sz_a.txt')
        # queues
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


g_utils = Utils()