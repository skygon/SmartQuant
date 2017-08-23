#coding=utf-8
import os
import sys
import json
import urllib2
import threading
import requests
import time
sys.path.append(os.getcwd())
from utils import *


class HotIndustry(threading.Thread):
    def __init__(self):
        super(HotIndustry, self).__init__()
        self.token = "7bc05d0d4c3c22ef9fca8c2a912d779c"
        
        # rest apis BK example: C.BK04741 <- C.{BK0474}1
        self.base_url = "http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=CT&cmd=C._BKHY&sty=FPGBKI&st=c&sr=-1&p=1&ps=5000&cb=&js=var%20BKCache=[(x)]&token=%s&v=0.4666060520101798"
        
        self.industry_url = "http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=CT&cmd=%s&sty=FCOIATA&sortType=C&sortRule=-1&page=1&pageSize=20&js=var%20quote_123%3d{rank:[(x)],pages:(pc)}&token=%s&jsName=quote_123&_g=0.2427368205033993"

    def getCode(self, bk):
        try:
            url = urllib2.unquote(self.industry_url).decode('utf8')
            url = url %(bk, self.token)

            r = self.session.get(url)
            rs = r.text.encode('utf-8').split('=')[1]

            rs = rs.replace('rank', '"rank"')
            rs = rs.replace('pages', '"pages"')
            data = json.loads(rs)
            print data
        except Exception, e:
            print "hot industry get code failed %s" %(str(e))

    def parseLine(self, s):
        try:
            rs = s.split(',"')
            for r in rs[:2]:
                t = r.split(',')
                cat = t[1]
                print cat
                bk = "C." + cat + "1"
                self.getCode(bk)
        except Exception, e:
            print "hot industry parse line failed %s" %(str(e))

    def run(self):
        self.session = requests.Session()
        while True:
            try:
                url = urllib2.unquote(self.base_url).decode('utf8')
                url = url %(self.token)

                r = self.session.get(url)
                rs = r.text.encode('utf-8').split('=')[1]
                self.parseLine(rs)
                break
            except Exception ,e:
                print "hot industry failed : %s" %(str(e))
                time.sleep(5)
                self.session = requests.Session()


if __name__ == "__main__":
    hi = HotIndustry()
    hi.start()
    hi.join()