import json
import urllib2
from utils import *

BILL_LIST = "http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_Bill.GetBillList?"
BILL_LIST_COUNT = "http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_Bill.GetBillListCount?"
BILL_LIST_SUMMARY = "http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_Bill.GetBillSum?"

STOCKS_INDEX = "http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?"
g_pages = 5 # We think the first five pages are most useful

DEFAULT_PAGE_SIZE = 80
# Bill example url:
#http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_Bill.GetBillList?symbol=sh603993&num=60&page=1&sort=ticktime&asc=0&volume=0&amount=200000&type=0&day=2017-05-26

# Index example list
#http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page=1&num=20&sort=changepercent&asc=0&node=hs_a&symbol=&_s_r_a=page

'''
Used for both real time strategy data fetching and machine learning data collection. 
'''
# param_type : bill, summary
# api_type : bill_list, bill_list_count, bill_list_summary, STOCKS_INDEX

class RTDA(object):
    def __init__(self, date_string):
        self.day = date_string
        # params day must as the last item
        self.params_list = {}
        self.params_list['bill'] = {}
        self.params_list['index'] = {}
        self.initParamsList()
        
    def initParamsList(self):
        # bill param type
        self.params_list['bill']['num'] = DEFAULT_PAGE_SIZE
        self.params_list['bill']['page'] = 1 #first page
        self.params_list['bill']['sort'] = "ticktime"
        self.params_list['bill']['asc'] = 0
        self.params_list['bill']['volume'] = 0 # By default, use amount mode
        self.params_list['bill']['type'] = 0
        # change the following params
        self.params_list['bill']['amount'] = 50 * 100 * 100
        #self.params_list['day'] = "1970-01-01"

        # summary param type
        self.params_list['index']['page'] = 1 # page starts from 1. We only interst at the first 500 stocks.
        self.params_list['index']['num'] = DEFAULT_PAGE_SIZE # num can be any integer. 
        self.params_list['index']['sort'] = "changepercent"
        self.params_list['index']['asc'] = 0
        self.params_list['index']['node'] = "hs_a"
        self.params_list['index']['symbol'] = ""
        self.params_list['index']['_s_r_a'] = "page"

    
    def setCode(self, code):
        self.code = code

    def setParams(self, param_type, **kwargs):
        for k, v in kwargs.items():
            self.params_list[param_type][k] = v
    
    def composeURL(self, api_type):
        url = ""
        param_type = ""
        if api_type == "bill_list":
            url = BILL_LIST + "symbol=" + self.code
            param_type = 'bill'
        elif api_type == "bill_list_count":
            url = BILL_LIST_COUNT + "symbol=" + self.code
            param_type = 'bill'
        elif api_type == "bill_list_summary":
            url = BILL_LIST_SUMMARY + "symbol=" + self.code
            param_type = 'bill'
        elif api_type == "stocks_index":
            url = STOCKS_INDEX
            param_type = 'index'
        else:
            raise Exception("composeURL error. Unsupported bill type")
        for k, v in self.params_list[param_type].items():
            url = url + "&" + k + "=" + str(v)
        
        if api_type != "stocks_index":
            url = url + "&day=" + self.day
        print "url is %s" %(url)
        return url

    def getRawData(self, api_type):
        url = self.composeURL(api_type)
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        ret = response.getcode()
        if (ret != 200):
            raise Exception("response error")
        
        raw = response.read()
        text = raw.decode('gb2312') #codec is from response.info()
        return text

    def getBillListCount(self):
        try:
            text = self.getRawData("bill_list_count")
            return int(text[13:-3]) # (new String("10"))
        except Exception, e:
            print "getBillListCount error: %s \n" %(str(e))

    def getBillList(self):
        try:
            text = self.getRawData("bill_list")
            data = self.handleResponseBillList(text)
            return json.loads(data)
        except Exception, e:
            print "getBillList error: %s \n" %(str(e))

    def getBillListSummary(self):
        try:
            text = self.getRawData("bill_list_summary")
            data = self.handleResponseSummary(text)
            return json.loads(data)
        except Exception, e:
            print "getBillListSummary error : %s \n" %(str(e))

    def getStocksIndex(self):
        try:
            text = self.getRawData('stocks_index')
            data = self.handleResponseStocksIndex(text)
            #return json.loads(data)
            jd = json.loads(data)
            print type(jd[3])
            print jd[3]['symbol']
            return jd
        except Exception, e:
            print "getStocksIndex error: %s \n" %(str(e))

    def handleResponseBillList(self, data):
        data = data.replace('symbol', '"symbol"')
        data = data.replace('name', '"name"')
        data = data.replace('ticktime', '"ticktime"')
        #z = y.replace('price', '"price"')
        data = data.replace('volume', '"volume"')
        data = data.replace('prev_price', '"prev"')
        data = data.replace('kind', '"kind"')
        data = data.replace('price', '"price"')
        #print "data is: \n"
        #print data
        return data
    
    
    def handleResponseSummary(self, data):
        data = data.replace('symbol', '"symbol"')
        data = data.replace('name', '"name"')
        data = data.replace('opendate', '"opendate"')
        data = data.replace('minvol', '"minvol"')
        data = data.replace('voltype', '"voltype"')
        
        #Be careful here. totalvolpct actually will be "totalvol"pct
        data = data.replace('totalvol', '"totalvol"')
        data = data.replace('"totalvol"pct', '"totalvolpct"')
        
        data = data.replace('totalamt', '"totalamt"')
        data = data.replace('"totalamt"pct', '"totalamtpct"')
        
        data = data.replace('avgprice', '"avgprice"')
        data = data.replace('kuvolume', '"kuvolume"')
        data = data.replace('kuamount', '"kuamount"')
        data = data.replace('kevolume', '"kevolume"')
        data = data.replace('keamount', '"keamount"')
        data = data.replace('kdvolume', '"kdvolume"')
        data = data.replace('kdamount', '"kdamount"')
        data = data.replace('stockvol', '"stockvol"')
        data = data.replace('stockamt', '"stockamt"')
        #print data
        return data

    def handleResponseStocksIndex(self, data):
        data = data.replace('symbol', '"symbol"')
        data = data.replace('code', '"code"')
        data = data.replace('name', '"name"')
        data = data.replace('trade', '"trade"')
        data = data.replace('pricechange', '"pricechange"')
        #side affect
        data = data.replace('per', '"per"')
        data = data.replace('change"per"cent', '"changepercent"')
        data = data.replace('buy', '"buy"')
        data = data.replace('sell', '"sell"')
        data = data.replace('settlement', '"settlement"')
        data = data.replace('open', '"open"')
        data = data.replace('high', '"high"')
        data = data.replace('low', '"low"')
        data = data.replace('volume', '"volume"')
        data = data.replace('amount', '"amount"')
        data = data.replace('ticktime', '"ticktime"')
        data = data.replace('pb', '"pb"')
        data = data.replace('mktcap', '"mktcap"')
        data = data.replace('nmc', '"nmc"')
        data = data.replace('turnoverratio', '"turnoverratio"')
        return data



if __name__ == "__main__":
    rtda = RTDA("2017-07-07")
    rtda.setCode("sh603993")
    rtda.setParams('bill', amount=200*100*100, type=0)
    data = rtda.getBillListSummary()

    # test summary api
    #rtda.setParams('index', num=20)
    #data = rtda.getStocksIndex()
    print type(data[0]) # should be dict
    print data[0]['kuvolume']



