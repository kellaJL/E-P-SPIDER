import bs4
import requests


class PR:
    def __init__(self):
        self.url=''
        self.html=''
        self.PR_VALUE=-1.1
    def getHTMLText(self, url,code="utf-8",):
        self.url='http://tool.chinaz.com/ExportPR/?q='+url

        try:
            ua = { 'user-agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36'}
            r = requests.get(self.url, headers=ua,timeout=30)
            r.raise_for_status()
            r.encoding = code
            self.html = r.text
        except:
            pass

    def GetPR(self,url):
        self.getHTMLText(url)

        soup=bs4.BeautifulSoup(self.html,'html.parser')
        PR_class=soup.find('ul',attrs={'class':'ResultListWrap'})
        #print(PR_class)
        #PR_INVALID=PR_class.find('')
        if PR_class==None:
            return self.PR_VALUE
        PR_C=PR_class.find_all('div',attrs={'class':'w24-0'})
        #print(type(PR_C[-1].text))
        self.PR_VALUE=float(PR_C[-1].text)
        """
       col-red lh30 fz14   无法解析域名的class名
       """
        #print(self.PR_VALUE)
        return self.PR_VALUE
#url='www.baidu.com'
#p=PR()
#p.GetPR(url)

