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

    # 筛选涨幅大于1%的个股，目前只拿第一页的数据
    def getCode(self, bk):
        try:
            url = urllib2.unquote(self.industry_url).decode('utf8')
            url = url %(bk, self.token)

            r = self.session.get(url)
            rs = r.text.encode('utf-8').split('=')[1]

            rs = rs.replace('rank', '"rank"')
            rs = rs.replace('pages', '"pages"')
            data = json.loads(rs)
            #print data
            lines = data['rank']
            for l in lines:
                s = l.encode('utf-8')
                s_arr = s.split(',')
                code = s_arr[1]
                if code.find("60") == 0:
                    code = "sh" + code
                else:
                    code = "sz" + code
                
                settlement = float(s_arr[9])
                if settlement == 0 or float(s_arr[10]) == 0:
                    continue

                change = float(s_arr[4])
                per_change = s_arr[5]


                if change / settlement > 0.01:
                    print "%s -> %s | %s -> %s" %(code, settlement, change, per_change)
                    self.hot_codes.append(code)

        except Exception, e:
            print "hot industry get code failed %s for %s" %(str(e))

    # 取前10个热门行业。涨幅小于0时返回
    def parseLine(self, s):
        try:
            rs = s.split(',"')
            for r in rs[:10]:
                t = r.split(',')
                cat = t[1]
                change = float(t[3])
                if change < 0:
                    return
                print cat
                bk = "C." + cat + "1"
                self.getCode(bk)
        except Exception, e:
            print "hot industry parse line failed %s" %(str(e))

    def oneTimeRun(self):
        self.session = requests.Session()
        while True:
            try:
                self.hot_codes = []
                url = urllib2.unquote(self.base_url).decode('utf8')
                url = url %(self.token)

                r = self.session.get(url)
                rs = r.text.encode('utf-8').split('=')[1]
                self.parseLine(rs)
                g_utils.hot_codes = self.hot_codes
                print "hot codes: %s" %(g_utils.hot_codes)
                break # !!! change to time sleep for real
                #time.sleep(5) # refresh every 10 min
            except Exception ,e:
                print "hot industry failed : %s" %(str(e))
                time.sleep(30)
                self.session = requests.Session()

    def run(self):
        self.session = requests.Session()
        while True:
            try:
                self.hot_codes = []
                url = urllib2.unquote(self.base_url).decode('utf8')
                url = url %(self.token)

                r = self.session.get(url)
                rs = r.text.encode('utf-8').split('=')[1]
                self.parseLine(rs)
                g_utils.hot_codes = self.hot_codes
                print "hot codes: %s" %(g_utils.hot_codes)
                #break # !!! change to time sleep for real
                time.sleep(5) # refresh every 10 min
            except Exception ,e:
                print "hot industry failed : %s" %(str(e))
                time.sleep(30)
                self.session = requests.Session()


if __name__ == "__main__":
    hi = HotIndustry()
    hi.start()
    hi.join()