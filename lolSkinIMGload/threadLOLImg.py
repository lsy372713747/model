# -*- coding: utf-8 -*-
import urllib
import os
import time
from functools import wraps
import math
import threading

# TODO： 线程卡死问题

def func_timer(function):
    @wraps(function)
    def function_timer(*args, **kwargs):
        t0 = time.time()
        result = function(*args, **kwargs)
        t1 = time.time()
        print ("Total time running %s: %s seconds" %
               (function.func_name, str(t1-t0))
               )
        return result
    return function_timer

def saveImg(imageURL,fileName, path):
    u = urllib.urlopen(imageURL)
    data = u.read()
    if data.strip() == "The requested URL '/images/lol/appskin/0.jpg' was not found on this server." \
            or data.strip() == "404 page not found":
        return False
    else:
        if not os.path.exists(path):
            os.makedirs(path)
        if not os.path.exists(path + fileName):
            f = open(path + fileName, 'wb')
            f.write(data)
            f.close()
            print u"正在保存图片=>",fileName
        else:
            print u"已存在图片=>",fileName
            return False

def formatNum(strs):
    strs = str(strs)
    s = strs.zfill(3)
    return s

# 保存英雄图片
# for i in range(200):
# 	url = 'http://ossweb-img.qq.com/images/lol/appskin/%s.jpg'%i
# 	saveImg(url, url.split('/')[-1], './img/hero/')

# 获取英雄皮肤
def get_skin(thread_name, hero_count, one_hero_skin_count):
    print 'Run thread %s (%s)...' % (thread_name, os.getpid())
    start = time.time()
    for x in hero_count:
        for i in range(one_hero_skin_count):
            skin = str(x) + formatNum(i)
            url = 'http://ossweb-img.qq.com/images/lol/appskin/{skin}.jpg'.format(skin=skin)
            saveImg(url, url.split('/')[-1], './threadIMG/{hero}/'.format(hero=x))
    end = time.time()
    print 'thread %s runs %0.2f seconds.' % (hero_count, (end - start))

hero_count = 200
skin_count = 20
thread_count = 4

def yield_thread(thread_count, hero_count):
    ''''''
    counts = int(math.ceil(float(hero_count/    thread_count)))
    for x in range(1, thread_count+1):
        list = [i for i in range((counts*x)-counts , x*counts)]
        yield list

@func_timer
def thread_get_skin(skin_count):
    print 'Parent process %s.' % os.getpid()
    threads = []
    c = 0
    createVar = locals()
    for i in yield_thread(thread_count, hero_count):
        c += 1
        createVar['t' + str(c)] = threading.Thread(target=get_skin,args=(c, i, skin_count))
        threads.append(createVar['t' + str(c)])
    print 'Waiting for all done...'
    for t in threads:
        t.setDaemon(True)
        t.start()
    t.join()
    print 'All done.'
if __name__ == '__main__':
    thread_get_skin(skin_count)