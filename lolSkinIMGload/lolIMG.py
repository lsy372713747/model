# -*- coding: utf-8 -*-
import urllib
import os

hero_count = 200
skin_count = 20

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
for i in range(200):
    url = 'http://ossweb-img.qq.com/images/lol/appskin/%s.jpg'%i
    saveImg(url, url.split('/')[-1], './img/hero/')

# 保存英雄皮肤图片
for x in range(hero_count):
    for y in range(skin_count):
        skin = str(x) + formatNum(y)
        url = 'http://ossweb-img.qq.com/images/lol/appskin/{skin}.jpg'.format(skin=skin)
        saveImg(url, url.split('/')[-1], './poolIMG/{hero}/'.format(hero=x))