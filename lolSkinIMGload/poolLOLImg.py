# -*- coding: utf-8 -*-
import urllib
import os
import time
from functools import wraps
from multiprocessing import Pool

hero_count = 200
skin_count = 20

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
def get_skin(hero_count, one_hero_skin_count):
    print 'Run task %s (%s)...' % (hero_count, os.getpid())
    start = time.time()
    for i in range(one_hero_skin_count):
        skin = str(hero_count) + formatNum(i)
        url = 'http://ossweb-img.qq.com/images/lol/appskin/{skin}.jpg'.format(skin=skin)
        saveImg(url, url.split('/')[-1], './poolIMG/{hero}/'.format(hero=hero_count))
    end = time.time()
    print 'Task %s runs %0.2f seconds.' % (hero_count, (end - start))

@func_timer
def pool_get_skin(hero_count, skin_count):
    p = Pool(8)
    print 'Parent process %s.' % os.getpid()
    for i in range(hero_count):
        p.apply_async(get_skin, args=(i, skin_count))
    print 'Waiting for all subprocesses done...'
    p.close()
    p.join()
    print 'All subprocesses done.'

if __name__ == '__main__':
    pool_get_skin(hero_count, skin_count)