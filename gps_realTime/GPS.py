import os
import glob
import serial
from types import SimpleNamespace
from lxml import etree
import geopy.distance


class ReadLine:
    def __init__(self, s):
        self.buf = bytearray()
        self.s = s

    def readline(self):
        i = self.buf.find(b"\n")
        if i >= 0:
            r = self.buf[:i+1]
            self.buf = self.buf[i+1:]
            return r
        while True:
            i = max(1, min(2048, self.s.in_waiting))
            data = self.s.read(i)
            i = data.find(b"\n")
            if i >= 0:
                r = self.buf + data[:i+1]
                self.buf[0:] = data[i+1:]
                return r
            else:
                self.buf.extend(data)


class HandsomeHanWen:
    def __init__(self):
        self.COM_PORT = 'COM3'
        self.BAUD_RATES = 921600
        self.s = serial.Serial(self.COM_PORT, self.BAUD_RATES, timeout=None)
        self.ser = ReadLine(self.s)
        self.Hmp = self.getkmpoints() # Hundred-meter pile # 載入百公尺樁資料 
        self.location = SimpleNamespace(lat = 24.3392393, lon = 120.6249646) # 當前位置 # 預設值 KFFF+000
    
    def HanWenIsRealyHandsome(self): # 獲取GPS資料
        while(True):
            data = self.ser.readline()
            data = data.decode()

            # data = data.split(",")
            #print(data.find("$GPRMC"))

            if data.find("$GPRMC") != -1 :
                data = data.split(",")
                if len(data[3][0:2]) > 0 :
                    N = float(data[3][0:2]) + float(data[3][-7:]) / 60
                    E = float(data[5][:-7]) + float(data[5][-7:]) / 60
                    self.location = SimpleNamespace(lat = N, lon = E)
                    kmp = self.kmplush()
                    return kmp
                    # N = '%.6f' % N # toString
                    # E = '%.6f' % E # toString
                    # return N + ', ' + E # 座標
                else :
                    self.location = SimpleNamespace(lat = 24.3392393, lon = 120.6249646)
                    kmp = self.kmplush()
                    return kmp
                    # return 0 # "未定位" 
                
    def HanWenIsVeryHandsome(self): #close the serial port 
        self.s.close()
##########################################        Hmp        ######################################################
    def getkmpoints(self, kmldir="./kmls/"):
        kmlfiles = glob.glob(kmldir + "*.kml")
        points = []
        count = 0
        for kf in kmlfiles:
            try:
                doc = etree.parse(kf)
                rr = doc.xpath('//kml:Placemark/kml:name/text()|//kml:Placemark/kml:Point/kml:coordinates/text()',
                                namespaces={"kml":"http://www.opengis.net/kml/2.2"})
                for i in range(0,len(rr),2):
                    name = rr[i]
                    x,y,z = str(rr[i+1]).split(',')
                    # point = {'name':name,'lon':x,'lat':y,'alt':z, 'index':count}
                    point = SimpleNamespace(name=name, lon=x, lat=y, alt=z, index=count)
                    count = count + 1
                    points.append(point)
            except Exception as err:
                raise err
        return points

    def kmplush(self):
        # print(self.location)
        kmp = self.findclosepoint(self.location)
        if(not hasattr(kmp, 'name')):
            kmp.name = "KFFF+000"
            kmp.meter = 0
        # print("kmp:" + str(kmp))
        kmfo = kmp.name.split("+")
        kmp.kmfo = kmfo[0] + "+" + (str)(round((float)(kmfo[1]) + kmp.meter, 2))
        return kmp

    def findclosepoint(self,targetpoint, thresh=0.1, debug=False):
        lpoint = self.Hmp[0]
        rpoint = self.Hmp[1]
        curdiff = geopy.distance.geodesic((lpoint.lat, lpoint.lon),(self.location.lat,self.location.lon)).km
        nxtdiff = geopy.distance.geodesic((rpoint.lat, rpoint.lon),(self.location.lat,self.location.lon)).km
        kmp = SimpleNamespace()
        if(debug):print("distance thresh = {0}".format(thresh))
        for i in range(2,len(self.Hmp)):
            if(curdiff < nxtdiff and curdiff <= thresh):
                mdiff = geopy.distance.geodesic((lpoint.lat, lpoint.lon),(self.location.lat, self.location.lon)).km*1000
                if(debug):print("mdiff = {0}".format(mdiff))
                if(nxtdiff >= 0.1):
                    kmp.name = self.Hmp[lpoint.index - 1].name
                    kmp.meter = thresh*1000 - mdiff
                else:
                    kmp.name = lpoint.name
                    kmp.meter = mdiff
                break
            else:
                lpoint = rpoint
                rpoint = self.Hmp[i]
                curdiff = nxtdiff
                nxtdiff = geopy.distance.geodesic((rpoint.lat, rpoint.lon),(self.location.lat, self.location.lon)).km
                if(debug):print(lpoint.name,"curdiff",curdiff,rpoint.name,"nxtdiff",nxtdiff)
        if(debug):print("most close point at " + str(lpoint))
        return kmp

"""呼叫方法"""
if __name__ == '__main__':
    a = HandsomeHanWen() #宣告
    print("[test]", a.HanWenIsRealyHandsome()) # 獲取GPS資料/顯示
    a.HanWenIsVeryHandsome() # 關閉serial port //this step is very important, must remember