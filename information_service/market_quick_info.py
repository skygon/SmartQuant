import os
import sys
import json
import urllib2
sys.path.append(os.getcwd())
from utils import *

# xueqiu
quick_info_url = "https://xueqiu.com/v4/statuses/public_timeline_by_category.json?since_id=-1&max_id=-1&count=5&category=6"

class QuickInfo(object):
    def __init__(self):
        pass


    def getFirstPage()
