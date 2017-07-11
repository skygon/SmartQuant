from VolumeBase import VolumeBase

class VolumeMotivation(VolumeBase):
    def __init__(self):
        super(VolumeBase, self).__init__()
        self.total = 0
        self.exit_invalid_code = 0
        self.exit_motivation_break = 0
        self.exit_big_bill = 0
        self.stock_pool = 0
    
    def getVolumeMA(self, day_index, interval=5):
        try:
            total = 0
            for i in range(interval):
                total += self.volume[day_index - i]
            
            ma = float(total) / interval
            return ma
        except Exception, e:
            print "getVolumeMA failed %s" %(str(e))
    
    def quickIncVolume(self, day_index):
        try:
            ma = self.getVolumeMA(day_index-1)
            if ma == 0:
                return False
            # special stop stock
            if self.volume[day_index-1] == 0:
                return False
            
            if float(self.volume[day_index]) / self.volume[day_index-1] < 2.0:
                return False
            
            if float(self.volume[day_index]) / ma < 2.0:
                return False
            
            return True
        except Exception, e:
            print "quickIncCVolume failed %s" %(str(e))
            return False

    def motivationBreak(self):
        for i in range(4, 20):
            if self.quickIncVolume(last_days['one'] - i):
                if self.close[last_days['one']] > self.close[last_days['one']-i]:
                    return True

        return False
    
    def positiveBigBill(self, day_index):
        try:
            if self.code.find("60") == 0:
                code = "sh" + self.code
            else:
                code = "sz" + self.code
            
            self.rtda.setCode(code)
            self.rtda.setDate(self.date[day_index])
            self.rtda.setParams('bill', amount=200*100*100, type=0)
            data = self.rtda.getBillListSummary()
            if data is None:
                return False
            
            if data[0]['kuvolume'] < data[0]['kdvolume']:
                return False
            #if float(data[0]['kuvolume']) == 0:
            #    return False
            
            #if float(data[0]['kdvolume']) / float(data[0]['kuvolume']) > 1.2:
            #    return False
            
            return True
        except Exception, e:
            print "positiveBigBill failed %s" %(str(e))
            return False
    
    #量能突破后，连续两天外盘大单占多
    def conPositiveBigBill(self):
        if self.positiveBigBill(last_days['one']) is False:
            return False
        
        if self.positiveBigBill(last_days['one'] + 1) is False:
            return False
        
        return True
    
    def canBuy(self):
        try:
            self.total += 1
            self.prepareData()
            if self.invalidCode() or self.isNewStock():
                self.exit_invalid_code += 1
                return False
            
            if self.isStartUp():
                return False
            
            if self.quickIncVolume(last_days['one']) is False:
                return False
            
            if self.motivationBreak() is False:
                self.exit_motivation_break += 1
                return False
            
            if self.conPositiveBigBill() is False:
                self.exit_big_bill += 1
                return False



            self.stock_pool += 1
            return True
        except Exception, e:
            print "canBuy failed %s" %(str(e))
            return False

    def analysis(self):
        print "==== total codes : %s" %(self.total)
        print "==== exit from invalid code : %s" %(self.exit_invalid_code)
        print "==== exit from motivation break : %s" %(self.exit_motivation_break)
        print "==== exit from positive big bill : %s" %(self.exit_big_bill)
        print "==== stock pool size is %s" %(self.stock_pool)


if __name__ == "__main__":
    v = Volume('603993')
    for i in range(10):
        last_days['one'] = -1 - i
        ma = v.getVolumeMA(5)
        print v.date[last_days['one']], ma


    

    


