#coding:utf-8
'''
多线程加队列实现 生产者和消费者模型
'''

import threading, time
import Queue
import random
q = Queue.Queue()
def Producer(name):
    '''生产者'''
    for i in range(10):
        q.put(i)
        print '肯德基%s: 炸好 %s 包薯条' % (name, i)
        time.sleep(random.randrange(3))  # 3s内炸好一包薯条
def Consumer(name):
    '''消费者'''
    count = 0
    while count < 10:
        data = q.get()
        print '消费者:%s 购买 %s 包薯条' % (name, data)
        count += 1
        time.sleep(random.randrange(4))  # 4s内有人购买薯条
p = threading.Thread(target=Producer, args=('producer',))
c = threading.Thread(target=Consumer, args=('customer',))
p.start()
c.start()