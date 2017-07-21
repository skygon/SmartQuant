import os
import sys
import json
import urllib2
import threading
sys.path.append(os.getcwd())
from utils import *
import itchat
from itchat.content import *

# xueqiu
quick_info_url = "https://xueqiu.com/v4/statuses/public_timeline_by_category.json?since_id=-1&max_id=-1&count=5&category=6"

class QuickInfo(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)


    def getFirstPage(self):
        try:
            # httpHandler = urllib2.HTTPHandler(debuglevel=1)
            # httpsHandler = urllib2.HTTPSHandler(debuglevel=1)
            # opener = urllib2.build_opener(httpHandler, httpsHandler)
            # urllib2.install_opener(opener)
            
            headers = {}
            headers['Accept'] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"
            headers['User-Agent'] = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
            headers['Connection'] = 'keep-alive'
            headers['Cookie'] = "s=fc11ltk6v8; xq_a_token=0a52c567442f1fdd8b09c27e0abb26438e274a7e; xq_r_token=43c6fed2d6b5cc8bc38cc9694c6c1cf121d38471; u=271499737713720; webp=0; device_id=6c5436a0262a061e605957ee42fac936; Hm_lvt_1db88642e346389874251b5a1eded6e3=1499737714,1500528293; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1500613451"
            
            request = urllib2.Request(quick_info_url, headers=headers)
            response = urllib2.urlopen(request)
            ret = response.getcode()
            if (ret != 200):
                raise Exception("response error")
            
            print response.info()
            raw = response.read()
            #text = raw.decode('utf-8') #codec is from response.info()
            #with open("quick_info", 'w') as f:
            #  f.write(raw)
            data = json.loads(raw)
            print type(data)
            ticket = json.loads(data['list'][0]['data'].encode('utf-8'))
            print ticket['mark']
            print type(ticket['text'])
            
            itchat.auto_login(True)
            itchat.send_msg(ticket['text'], "filehelper")
        except Exception, e:
            print "get first page failed [%s]" %(str(e))
        
    def run(self):
        pass

if __name__ == "__main__":
    qi = QuickInfo()
    qi.getFirstPage()
