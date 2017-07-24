#coding=utf-8
import os
import sys
import json
import urllib2
import threading

# dongfang caifu 
# example C.BK04211
# token = "7bc05d0d4c3c22ef9fca8c2a912d779c"
industry_base_url = "http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=CT&cmd=%s&sty=FCOIATA&sortType=C&sortRule=-1&page=%s&pageSize=20&js=var%20quote_123%3d{rank:[(x)],pages:(pc)}&token=%s&jsName=quote_123&_g=0.1923871021689061"


class Category(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.token = "7bc05d0d4c3c22ef9fca8c2a912d779c"
        
    def getPages(self, category_code):
        try:
            print "base url %s" %(industry_base_url)
            url = urllib2.unquote(industry_base_url).decode('utf8') 
            url = url %(category_code, str(1), self.token)
            
            print "url: %s" %(url)
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            ret = response.getcode()
            if (ret != 200):
                raise Exception("response error")
        
            
            raw = response.read()
            text = raw.split('=')[1]
            text = text.replace('rank', '"rank"')
            text = text.replace('pages', '"pages"')
            print text
            data = json.loads(text)
            print type(data)
            print data
        except Exception, e:
            print "Category getPages failed %s" %(str(e))


    def run(self):
        while True:
            try:
                self.getPages("C.BK04211")
            except Exception, e:
                print "market information fetch failed [%s]" %(str(e))

if __name__ == "__main__":
    ca = Category()
    ca.getPages("C.BK04211")
