import os
import sys
import json
sys.path.append(os.getcwd())
from realtime_index import RealtimeIndex
from message_pusher import Pusher
from utils import *
import time


class MessageService(object):
    def __init__(self):
        self.config_file = os.path.join(os.getcwd(), "information_service", "myshares.json")
        self.stock_pool = []
        self.stock_conf = {}
        self.worker = []
        self.parseStockConf()

    def parseStockConf(self):
        try:
            f = open(self.config_file, 'r')
            data = json.load(f)
            
            for k, v in data.items():
                self.stock_pool.append(k)
                self.stock_conf[k] = v
        except Exception, e:
            print "parseStockConf failed [%s]" %(str(e))
        finally:
            f.close()

    def start(self):
        # start message pusher service
        self.pusher = Pusher()
        self.pusher.start()

        # query realtime index
        for i in range(len(self.stock_pool)):
            r = RealtimeIndex()
            r.setCode(self.stock_pool[i])
            r.start()
        
        # empty loop
        while True:
            print "....................."
            time.sleep(5)

if __name__ == "__main__":
    m = MessageService()
    m.start()

        
