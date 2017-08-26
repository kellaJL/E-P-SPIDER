import os
import re
import shutil
import zlib
import time
from datetime import datetime, timedelta
try:
    import cPickle as pickle
except ImportError:
    import pickle
import urllib
class DiskCache:
                                                   #30天前的日期
    def __init__(self, cache_dir='cache', expires=timedelta(days=30), compress=True):
        """
        cache_dir: the root level folder for the cache
        expires: timedelta of amount of time before a cache entry is considered expired
        compress: whether to compress data in the cache
        """
        self.cache_dir = cache_dir
        self.expires = expires
        self.compress = compress
    #从磁盘上检查此url是否已存于其中并返回其内容
    def __getitem__(self, url):#按照索引获取值,__getitem__专有方法
        """Load data from disk for this URL
        """
        path = self.url_to_path(url)
        if os.path.exists(path):
            with open(path, 'rb') as fp:
                data = fp.read()
                if self.compress:
                    data = zlib.decompress(data)
                result, timestamp = pickle.loads(data)
                #if self.has_expired(timestamp):
                 #  print(url + ' has expired')
                return result
        else:
            # URL has not yet been cached
          # print(url + ' does not exist')
            pass
    #将爬取的对象保存在磁盘中
    def __setitem__(self, url, result):#__setitem__按照索引赋值，__setitem__专有方法
        """Save data to disk for this url
        """
        path = self.url_to_path(url)
        folder = os.path.dirname(path)#输出python脚本所在路径
        if not os.path.exists(folder):
            os.makedirs(folder)#创建文件夹

        data = pickle.dumps((result, str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))))
        if self.compress:
            data = zlib.compress(data)
        with open(path, 'wb') as fp:
            fp.write(data)

    def __delitem__(self, url):
        """Remove the value at this key and any empty parent sub-directories
        """
        path = self._key_path(url)
        try:
            os.remove(path)
            os.removedirs(os.path.dirname(path))
        except OSError:
            pass

    def url_to_path(self, url):
        """Create file system path for this URL
        """
        components = urllib.parse.urlsplit(url)
        # when empty path set to /index.html
        path = components.path
        if not path:
            path = '/index.html'
        elif path.endswith('/'):
            path += 'index.html'
        filename = components.netloc + path + components.query
        # replace invalid characters
        filename = re.sub('[^/0-9a-zA-Z\-.,;_ ]', '_', filename)
        # restrict maximum number of characters
        filename = '/'.join(segment[:255] for segment in filename.split('/'))
        return os.path.join(self.cache_dir, filename)


    def has_expired(self, timestamp):
        """Return whether this timestamp has expired
        """
        return str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))) > timestamp + self.expires


    def clear(self):
        """Remove all the cached values
        """
        if os.path.exists(self.cache_dir):
            shutil.rmtree(self.cache_dir)
