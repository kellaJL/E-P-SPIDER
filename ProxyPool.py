import requests
from pymongo import MongoClient
import proxy_getter
client=MongoClient()
db=client.pythondb
REQ_TIMEOUT=5
class Proxy_Pool:
    def __init__(self):
        self.url = db.proxy


    def add_proxy(self,infoDict):
        """
        向数据库中插入记录
        :param infoDict:
        :return:
        """
        self.url.insert(infoDict)

    def del_record(self,ip):
        """
        删除数据库中制定记录
        :param ip:
        :return:
        """
        self.url.remove({'IP':ip})

    def test_connection(self,protocol,ip,port):
        """
        检测代理的有效性
        :param protocol:
        :param ip:
        :param port:
        :return:
        """
        proxies = {protocol: ip + ":" + port}
        try:
           # OrigionalIP = requests.get("http://icanhazip.com", timeout=REQ_TIMEOUT).content
            MaskedIP = requests.get("http://icanhazip.com", timeout=3, proxies=proxies).content
            if MaskedIP!=None:
                return True
            else:
                return False
        except:
            return False

    def Is_Empty(self):
        all=self.url.find()
        if all==None:
            return True
        else:
            return False

    def Re_CrawProxy(self):
        if self.Is_Empty():
            proxy_getter.get_ip()

    def clean_nonworking(self):
        """
        循环代理池，逐行测试IP地址端口协议是否可用
        :return:
        """
        all=self.url.find()
        if not all==None:
          for line in all:
            protocol=line['类型']
            ip=line['IP']
            port=line['PORT']
            isAnonymous=self.test_connection(protocol,ip,port)
            if isAnonymous==False:
                print('delete outdate proxy:'+ip)
                self.del_record(ip)

        self.Re_CrawProxy()

