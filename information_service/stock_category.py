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
        self.category = {}
        
    def getPage(self, category_code, page):
        try:
            print "base url %s" %(industry_base_url)
            url = urllib2.unquote(industry_base_url).decode('utf8') 
            url = url %(category_code, str(page), self.token)
            
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
            data = json.loads(text)
            
        except Exception, e:
            print "Category getPages failed %s" %(str(e))

    def getFullCategory(self):
        try:
            full_path = os.path.join(os.getcwd(), "information_service", "industry_map_dfcfw.list")
            with open(full_path, 'r') as f:
                imap = json.load(f, encoding='utf-8')
                #print imap['total']
                iarray = imap['total']
                for i in range(len(iarray)):
                    s = iarray[i].encode('utf-8')
                    sa = s.split(',')
                    icode = sa[1] + "1"
                    print icode
        except Exception, e:
            print "get full category failed %s" %(str(e))
            
    
    def run(self):
        while True:
            try:
                self.getPages("C.BK04211")
            except Exception, e:
                print "market information fetch failed [%s]" %(str(e))

if __name__ == "__main__":
    ca = Category()
    ca.getFullCategory()
