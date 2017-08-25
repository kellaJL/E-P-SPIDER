import os
import re
import requests
class downloader:
   def __init__(self):
        self.seed=''
   def parseSeed(self, seed,url):
        if len(seed) > 2000:
            print('The url is too long!\n')
            return False
        parse_regex = r'https?://'
        parse_www=r'www.'
        parse_pat = re.compile(parse_regex)
        parse_wwwp = re.compile(parse_www)
        if not parse_pat.search(seed):
            #print('URL is illegal!\n')
            if not parse_wwwp.search(seed):
                if seed[0]=='/':
                   self.seed=url[:-1]+seed
                else:
                    self.seed=url+seed
                return True
        self.seed=seed
        return True

   def downloader(self,img_q,url):
     #print('test')
     if img_q==None:
         return
     else:
       if self.parseSeed(img_q,url)==False:

            return
       root="D:/Spider/"


       if not os.path.exists(root):
                os.mkdir(root)
       try:
          r = requests.get(self.seed)
       except:

          return
       p=img_q.split('/')[-1]
       #n = p.find('.jpg')
       path1=root+p#jpg格式下载保存路径

       if not os.path.exists(path1):

            try:
                with open(path1, 'wb') as f:
                         f.write(r.content)
                         f.close()
                print(path1+' SAVE SUCCESSFULLY! '+'size:'+str(os.path.getsize(path1))+'Byte')

            except:
                print(path1+'SAVE FAILURE')
                pass
       else:
           print("this img:"+path1+" has been saved!")
#img_url='http://icon.qiantucdn.com/img/lazypic.jpg'
#d=downloader()
#d.downloader(img_url)
