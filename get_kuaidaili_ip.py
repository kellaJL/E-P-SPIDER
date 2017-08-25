import bs4
import requests
import csv
import re
from pymongo import MongoClient
#import ProxyPool
client = MongoClient()

db = client.pythondb
class GetKuaiDaiLiIp:


    def GetHTMLText(self,url,code='utf-8'):
        html = ''
        ua={'user-agent':'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36'}

        r = requests.get(url,headers=ua,timeout=3)
        if 500 <= r.status_code < 600:
            return self.GetHTMLText(url)
        r.raise_for_status()
        r.encoding = code
        html = r.text
              # self.cache[url] = html
        return html

    def ParseAndGetInfo(self,url):
        #p_p=ProxyPool.Proxy_Pool()
        proxy_pool2=db.proxy
        html=self.GetHTMLText(url)
        #print(html[:200])
        count=0
        if html==None:
            return
        soup=bs4.BeautifulSoup(html,'html.parser')
        ip_info=soup.find('table',attrs={'class':'table table-bordered table-striped'})
        key_list=ip_info.find_all('th')
        value_list=ip_info.find_all('td')
        len_list=ip_info.find_all('tr')
        len_list_length=len(len_list)
        #print(len_list_length)
        key_len=len(key_list)
        #print(len(value_list))
        #proxies_pools=db.proxy
        for k in range(len_list_length-1):
           infoDict={}
           for i in range(key_len):
              key=key_list[i].text
              value=str(value_list[i+k*(key_len)].text)
              pat=re.compile(':')
              value1=pat.sub('-',value)
              #value.replace(':','-')
              #print(value)
              infoDict[key]=value1
           if infoDict['匿名度']=='高匿名':
               #is_working=p_p.test_connection(infoDict['类型'],infoDict['IP'],infoDict['PORT'])
               #if is_working:
                #   p_p.add_proxy(infoDict)
              print('proxies:'+infoDict)
              proxy_pool2.insert(infoDict)




#s=GetKuaiDaiLiIp()
#url='http://www.kuaidaili.com/free/'
#fpath='D:/s219.txt'
#s.ParseAndGetInfo(url)
