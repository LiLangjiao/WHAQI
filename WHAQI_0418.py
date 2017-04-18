# _*_ coding:utf-8 _*_
# author: LJ299

import requests
import bs4
from bs4 import BeautifulSoup
import re
import time
from datetime import datetime,date,timedelta



def getHTML(url,fpath=r'E:\WHAQI\html'):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        dt = datetime.now().strftime("%Y-%m-%d %H")
        with open(fpath + dt + '.txt','w') as f:
            f.write(r.text.encode('utf-8'))
        return r.text
    except Exception as e:
        dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(fpath + 'log.txt','a') as log:
            log.writelines(dt+'\n'+str(e)+'\n')
        return ""

def getAQI(aqilist,html):
    soup = BeautifulSoup(html,"html.parser")
    soup.prettify()
    for tr in soup.find_all('tr'):
        if tr('td'):
             tds = tr('td')
             date = tds[0].string
             station = tds[1].string
             so2 = tds[2].string
             no2 = tds[3].string
             pm10 = tds[4].string
             co = tds[5].string
             o3_1 = tds[6].string
             o3_8 = tds[7].string
             pm25 = tds[8].string
             aqi = tds[9].string
             pollution = tds[10].string
             class_AQI = tds[11].string
             #print date,station,so2,no2,pm10,co,o3_1,o3_8,pm25,aqi,pollution,class_AQI
             aqilist.append((',').join((date,station,so2,no2,pm10,co,o3_1,o3_8,pm25,aqi,pollution,class_AQI)))

def outputAQI(aqilist):
    workspace = r"D:\workspace\WHAQI"
##    year = str(datetime.now().year)
##    month = str(datetime.now().month)
##    day = str(datetime.now().day)
##    hour = str(datetime.now().hour)
##    dt = ("_").join((year,month,day,hour))
    with open(workspace +"\\"+"aqi_wh.txt",'a') as f:
        #f.write("时间,监测点位,二氧化硫,二氧化氮,PM10,一氧化碳,臭氧_1h,臭氧_8h,PM2.5,AQI指数,首要污染物,AQI指数类别\n")
        for station in aqilist:
            aqi = station.encode("utf-8")
            f.write(aqi + "\n")

            
def printAQI(aqilist):
    tpl = "{:^18}\t{:^14}\t{:^6}\t{:^6}\t{:^6}\t{:^6}\t{:^6}\t{:^6}\t{:^6}\t{:^6}"
    print tpl.format("时间","监测点位","二氧化硫","二氧化氮",\
                     "PM10","一氧化氮","臭氧_1h","臭氧_8h",\
                         "PM2.5","AQI指数","首要污染物","AQI指数类别")
    

    for i in range(len(aqilist)):
        st_data = aqilist[i] # 站点aqi描述信息
        st = str(st_data.encode('utf-8'))
        station = st.split(',')
        
        print tpl.format(station[0],station[1],station[2],station[3],\
                        station[4],station[5],station[6],station[7],\
                        station[8],station[9])


def main():
    url = "http://www.whepb.gov.cn/airSubair_water_lake_infoView.jspx?type=1"
    aqi = []
    html = getHTML(url)
    count = 0

    while not html and count < 10:
        time.sleep(20)
        html = getHTML(url)
        count = count + 1
    else:
        if html:
            getAQI(aqi,html)
            #printAQI(aqi)
            outputAQI(aqi)
        else:
            dt = datetime.now().strftime("%Y-%m-%d %H")
            with open(r'E:\WHAQI\html' + 'httplog.txt','a') as log:
                log.writelines(dt+'\n'+"访问失败！"+'\n')
        
        
    

def repeat():
    for i in range(25):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print "第{0}次执行，时间：{1}".format(i+1,now)
        main()
        time.sleep(3600)

repeat()





