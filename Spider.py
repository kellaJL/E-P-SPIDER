#Spider.py
"""
框架爬取爬虫
"""

import requests
import re
import bs4
import DiskCache
import ProxyPool
import ProxyGetter
import PR
from pymongo import MongoClient

client = MongoClient()

db = client.pythondb

class Spider:
    def __init__(self,url=''):
        self.url=url
        self.url_queue=list()#url队列
        self.img_queue=list()#图片种子队列
        self.cache=DiskCache.DiskCache()#磁盘缓存页面到当前目录
        self.html=str()#存储页面内容
        self.posts = db.urldatabase619
        self.post = db.imgdatabase619
        #self.PR_WEIGHT=-1#网页pr值
    #获取html页面内容

    #检测url合法性
    def parseURL(self):
        if len(self.url)>100:
            print('The url is too long!\n')
            return False
        parse_regex=r'https?://'
        parse_pat=re.compile(parse_regex)
        if not parse_pat.search(self.url):
            print('URL is illegal!\n')
            return False
        return True
    #获取PR值
    def Get_PR(self):
        PR_url = 'http://tool.chinaz.com/ExportPR/?q=' + self.url

        p = PR(PR_url)
        p.GetPR()
        self.PR_WEIGHT = PR.PR()
        return self.PR_WEIGHT

#缓存机制爬去页面
    def getHTMLText(self,code="utf-8"):
        if not self.parseURL():
            return
        if self.cache:
            self.html = self.cache[self.url]
            if not self.html:
               p_p=ProxyPool.Proxy_Pool()
               proxy = db.proxy
               tag=True
               while tag:
                  proxies=proxy.find_one()
                  if proxies==None:
                     ProxyGetter.get_ip()
                  one_p=str(proxies['类型'])
                  two_p=str(proxies['IP'])
                  three_p=str(proxies['PORT'])
              #print(one_p)
              #print(type(one_p))
                  flag=p_p.test_connection(one_p,two_p,three_p)##########################
                  if flag==False:
                     p_p.del_record(proxies['IP'])
                  #proxies = proxy.find_one()
                  else:
                    tag=False
               proxy_ip = {str(proxies['类型']):str(proxies['IP']) + ":" + str(proxies['PORT'])}
               try:

                   ua = {'user-agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36'}
                   r = requests.get(self.url,headers=ua,proxies=proxy_ip)
                   r.raise_for_status()
                   r.encoding = code
                   self.html=r.text
                   self.cache[self.url] = self.html
            #p_p.clean_nonworking()
               except:
            #p_p.clean_nonworking()
                  pass

 

    #删除页面内的js和style代码段，提高搜索效率
    def replaceJS(self):
        js_list=[]#存储js
        style_list=[]#存储style
        js_regex=r'<script.*?>[\s\S]+?<\/script>'
        style_regex=r'<style.*?>[\s\S]+?<\/style>|\s|&nbsp'
        js_pat=re.compile(js_regex,re.IGNORECASE)
        style_pat=re.compile(style_regex,re.IGNORECASE)#bug................................................
        js_list=js_pat.findall(self.html)
        style_list=style_pat.findall(self.html)
        js_len=len(js_list)
        style_len=len(style_list)
        for i in range(js_len):
            self.html.replace(js_list[i],' ')
        for i in range(style_len):
            self.html.replace(style_list[i],' ')



    #获取页面上的所有url连接
    def getURL(self,start_url):

        self.replaceJS()
        url_regex = start_url+'.*?\"'
        #url_regex=r'\"https?://[a-zA-z/]*?.scann.com\/[a-zA-z/]*?.[hH]tml\"'
        url_pat=re.compile(url_regex,re.IGNORECASE)
        for line in url_pat.findall(self.html):
            self.url_queue.append(line[:-1])
        """
        将url队列d导入数据库
        mongodb
       """


        #PR_g=PR.PR()


        url_queue=list(set(self.url_queue))
        for i in range(len(url_queue)):

            if url_queue[i][-3:]=='jpg' or url_queue[i][-3:]=='gif' or url_queue[i][-3:]=='png':
                continue
            infoDict = {}

            infoDict['url']=url_queue[i]
            #infoDict['weight']=PR_g.GetPR(self.url_queue[i])
            infoDict['is_traveled']=-1#判断是否url已被探索过
            #if infoDict['weight']!=-1.1:
            print(infoDict)
            self.posts.insert(infoDict)#
        #all=posts.find()
    #获取页面内的图片种子
    """
    正则表达式
    """
    def getImgSeed(self):

        img_seed_regex=r'\"[a_zA-Z./:]*?.jpg\"'

        img_seed_pat=re.compile(img_seed_regex,re.IGNORECASE)
        #img_seed_pat1 = re.compile(img_seed_regex1, re.IGNORECASE)
        for line in img_seed_pat.findall(self.html):
            line1=line[1:-1]
            self.img_queue.append(line1)
        #for line in img_seed_pat1.findall(self.html):
         #   self.img_queue.append(line)

        #存放img seed的集合
        self.img_queue=list(set(self.img_queue))
        for i in self.img_queue:
            infoDict={}
            infoDict['seed']=i
            print('seed:'+i)
            self.post.insert(infoDict)

    """
    获取图片种子
    beautifulsoup
    """
    def GetImgSeed(self):
        soup=bs4.BeautifulSoup(self.html,'html.parser')
        seed=soup.find_all('img')
        if not seed:
            #print('ts')
            self.getImgSeed()
            return
        else:
          for line in seed:
              p=line.attrs
              dict(p)
              if 'src' in p:
                  src=str(line['src'])
                  self.img_queue.append(src)
              else:
                  self.getImgSeed()
                  return

          self.img_queue=list(set(self.img_queue))
          for i in self.img_queue:
              infoDict={}
              infoDict['seed']=i
              print('seed:'+i)
              self.post.insert(infoDict)

    #更新数据库
    def updateDatabase(self):

        print("正在更新数据库，请稍等...........")
        expired_url=self.posts.find()
        url_fields=0#数据库中url字段计数器
        processing_counter=0#进度指示器
        for line in expired_url:
            url_fields=url_fields+1
        print(url_fields)
        if url_fields>0:
            expired_url_d = self.posts.find()
            for line in expired_url_d:

                processing_counter=processing_counter+1
                self.posts.remove({"url": line["url"]})
                print("\r当前进度: {:.2f}%".format(float(processing_counter/url_fields)*100),end="")
        print("\n更新完毕，开始爬取...............")

    def deleteDatabase(self):
        print("爬取完毕，开始清除数据库，请稍等...........")
        expired_url = self.posts.find()
        url_fields = 0  # 数据库中url字段计数器
        processing_counter = 0  # 进度指示器
        for line in expired_url:
            url_fields = url_fields + 1
            print(line)
        if url_fields >0:
            expired_url_d = self.posts.find()
            for line in expired_url_d:
                processing_counter = processing_counter + 1
                self.posts.remove({"url": line["url"]})
                print("\r当前进度: {:.2f}%".format(float(processing_counter / url_fields) * 100), end="")
            print("\n删除完毕...............")
    #主函数
    def main(self,url,start_url):
        self.url=url
        self.getHTMLText()
        self.getURL(start_url)
        self.GetImgSeed()

#url='http://588ku.com/'
#url='http://www.sccnn.com/'
#url="http://www.baidu.com/"
#sp=Spider(url)
#print(sp.getPage())
#s=Spider()
#s.main(url,url)


