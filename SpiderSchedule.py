#SpiderSchedule.py
from Spider import Spider
#import threadpool
from pymongo import MongoClient
import time
import concurrent.futures

client=MongoClient()
db=client.pythondb
spider=Spider()

class SpiderSchedule:
    def __init__(self):
        self.is_empty=False#判空标志
        self.url = db.urldatabase619
    def Rem_Repate(self):
            """
            去除数据库中重复的url
            :return:
             """

            for url1 in self.url.distinct('url'):  # 使用distinct方法，获取每一个独特的元素列表
                num = self.url.count({"url": url1})  # 统计每一个元素的数量
                print(num)
                for i in range(1, num):  # 根据每一个元素的数量进行删除操作，当前元素只有一个就不再删除
                    print('\r删除 %s %d times ' % (url1, i),end="")

                    # 注意后面的参数， 很奇怪，在mongo命令行下，它为1时，是删除一个元素，这里却是为0时删除一个
                    self.url.remove({"url": url1}, 0)
                for i in self.url.find({"url": url1}):  # 打印当前所有元素
                    print(i)

    def SpiderSchedule(self,start_url):
        self.Rem_Repate()
        THREAD_NUMBER = 5
      
        url_list=[]

        all=self.url.find({"is_traveled":-1},{'url':1,'is_traveled':1})#在此处筛选未被探索过的url，使用bool标志
      

        if all==None:
            self.is_empty=True
            return self.is_empty
      
        url_counter=0
        for line in all:
            if url_counter<THREAD_NUMBER:
               self.url.update({"url": line['url']}, {'$set': {"is_traveled": 1}})  # 修改traveled字段值
               url_list.append(line['url'])
               url_counter=url_counter+1
            else:
                break

        """
            #if line['is_traveled']==-1:
            w_list.append(line['weight'])
            #print(line)
        w_list=list(set(w_list))#去重
        #for i in w_list:
         #   print('qz:'+str(i))
        if len(w_list)==0:
            print('None URL!')
            return
        """
        """
        if len(w_list) < THREAD_NUMBER:  # 确定一次投放线程数
            THREAD_NUMBER = len(w_list)
        for i in range(THREAD_NUMBER):
            t=max(w_list)#获取权值最大的url
            url_weight_list=url.find({"weight":t},{'url':1,'weight':1,"_id":0})
            for line in url_weight_list[:1]:
                url.update({"url":line['url']}, {'$set': {"is_traveled": 1}})#修改traveled字段值
                url_list.append(line['url'])
            w_list.remove(t)

        #print("tests")
        """
        for line in url_list[:THREAD_NUMBER]:
             print('Ready to crawl:'+line)

         #多线程
        start_time = time.time()
        """
        pool = threadpool.ThreadPool(THREAD_NUMBER)
        requests = threadpool.makeRequests(spider.main,zip(url_list,start_list))
       # print('test')
        [pool.putRequest(req) for req in requests]
        pool.wait()
        """
        # We can use a with statement to ensure threads are cleaned up promptly
        with concurrent.futures.ThreadPoolExecutor(THREAD_NUMBER) as executor:
            # Start the load operations and mark each future with its URL
            future_to_url = {executor.submit(spider.main, url, start_url): url for url in url_list}
            for future in concurrent.futures.as_completed(future_to_url):
                url = future_to_url[future]

                try:
                    data = future.result()
                    #print(data)
                except Exception as exc:
                    print('%r generated an exception: %s' % (url, exc))
                #print('sur:'+url)
                if not data:
                    continue
                print('%r page is %d bytes' % (url, len(data.content)))
        print('this circle used %d second' % (time.time() - start_time))
        time.sleep(3)
        return self.is_empty
#start_url="http://www.xiaohuar.com/"
#sp=SpiderSchedule()
#sp.SpiderSchedule(start_url)
