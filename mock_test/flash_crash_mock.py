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
from utils import *


class FlashCrashMock(object):
    def __init__(self):
        pass
    
    