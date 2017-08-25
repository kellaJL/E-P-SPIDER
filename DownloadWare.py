"""
从数据库中取种子下载；
"""
from pymongo import MongoClient
from downloader import downloader
import re
import time
import concurrent.futures
client=MongoClient()
db=client.pythondb

img=db.imgdatabase613


download=downloader()
THREAD_NUMBER=5
class downloaderware:
    def __init__(self):
        self.is_seed_empty=False#判空标志

    def Rem_Repate(self):
            """
            去除数据库中重复的url
            :return:
             """
            global img
            for url1 in img.distinct('seed'):  # 使用distinct方法，获取每一个独特的元素列表
                num = img.count({"seed": url1})  # 统计每一个元素的数量
                print(num)
                for i in range(1, num):  # 根据每一个元素的数量进行删除操作，当前元素只有一个就不再删除
                    print(r"\r删除 %s %d times " % (url1, i))
                    # 注意后面的参数， 很奇怪，在mongo命令行下，它为1时，是删除一个元素，这里却是为0时删除一个
                    img.remove({"seed": url1}, 0)
                for i in img.find({"seed": url1}):  # 打印当前所有元素
                    print(i)

    def downloaderware(self,url):
        print('downloading............')
        self.Rem_Repate()
        global img
        all = img.find()
        if all==None:
            self.is_seed_empty=True
            return self.is_seed_empty
        seeds=[]
        for line in all:
            #print(line)
            seeds.append(line['seed'])

            #print(seed)
        if len(seeds)>50:
            seeds=seeds[:50]
        if seeds:
                start_time = time.time()
                # We can use a with statement to ensure threads are cleaned up promptly
                with concurrent.futures.ThreadPoolExecutor(THREAD_NUMBER) as executor:
                    # Start the load operations and mark each future with its URL
                    future_to_url = {executor.submit(download.downloader,seed,url): seed for seed in seeds}
                    for future in concurrent.futures.as_completed(future_to_url):
                        seed = future_to_url[future]
                        try:
                            data = future.result()
                        except Exception as exc:
                            print('%r generated an exception: %s' % (seed, exc))
                        else:

                            if   not data:
                                continue
                            print('%r page is %d bytes' % (seed, len(data)))
                print('this circle used %d second' % (time.time() - start_time))
                #downloader.downloader(seed,url)
        for used_seed in seeds:
            img.remove({"seed":used_seed})
        return self.is_seed_empty
#url="http://588ku.com/"
#d=downloaderware()
#d.downloaderware(url)
