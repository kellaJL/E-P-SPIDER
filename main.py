"""
主函数
SpiderSchedule
downloader_ware
"""
import ProxyPool
import SpiderSchedule
from DownloadWare import downloaderware
from Spider import Spider
import threading
import time
from pymongo import MongoClient
client = MongoClient()

db = client.pythondb
mongo_base=db.urldatabase618
expired_url=mongo_base.find()
print("正在更新数据库，请稍等...........")
for line in expired_url:
    mongo_base.remove({"url":line["url"]})
print("更新完毕，开始爬取...............")
SLEEP_TIME=5
global start_url
start_url="http://www.xiaohuar.com/"
#start_url=u"http://www.baidu.com/"

sp=Spider()
sp.main(start_url,start_url)
spider_schedule=SpiderSchedule.SpiderSchedule()

downloads = downloaderware()
threads=[]

p_p=ProxyPool.Proxy_Pool()
proxy_counter=1#代理池更新计数器
threads_counter=0#线程计数器
t0 = threading.Thread(target=spider_schedule.SpiderSchedule,args=(start_url,))
t0.start()
threads.append(t0)
while threads and threads_counter<=50:

    # the crawl is still active
    for thread in threads:
        if not thread.is_alive():
            # remove the stopped threads
            threads.remove(thread)

        t2 = threading.Thread(target=downloads.downloaderware, args=(start_url,))
        t2.start()
        threads.append(t2)
        time.sleep(SLEEP_TIME)
        t1 = threading.Thread(target=spider_schedule.SpiderSchedule,args=(start_url,))
        t1.start()
        threads.append(t1)

        # all threads have been processed
        # sleep temporarily so CPU can focus execution on other threads
        proxy_counter=proxy_counter+1
        if proxy_counter%25==0:
           p_p.clean_nonworking()
        time.sleep(SLEEP_TIME)
    threads_counter=threads_counter+1#线程计数器

#爬取结束，清空数据库
for line in expired_url:
    mongo_base.remove({"url":line["url"]})





