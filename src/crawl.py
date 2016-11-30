#coding:utf-8

import time
import urllib2
import os,random
import conf.config as cf
from lxml import etree

#给定一些topics
def getUrls(url_original):
    response = urllib2.urlopen(url_original)
    html = response.read()
    tree = etree.HTML(html)
    nodes = tree.xpath("//a[@target='_blank']")
    result = []
    for ele in nodes:
        try:
            title, url = ele.text, ele.get('href')
            title = title.strip()
        except:
            title = ''
        if url.endswith('.html'):
            result.append((title,url))
    return result

def getNew(url):
    response = urllib2.urlopen(url)
    html = response.read()
    tree = etree.HTML(html)
    return ''.join(tree.xpath("//div[@class='text']/p/text()"))


def run_crawl(topics):
    #topics:[(topic,url_original),...]
    for topic in topics:
        topic,url_original = topic
        urls = getUrls(url_original)
        try:
            os.mkdir(os.path.join(cf.TRAIN_ROOT,topic))
        except:
            pass
        for ind,url in enumerate(urls):
            title,url = url
            time.sleep(random.random())
            try:
                content = getNew(url)
            except:
                continue
            if content.strip() == '':
                continue
            print 'crawling: %s has been downloaded...'%title
            f = file(os.path.join(cf.TRAIN_ROOT,topic+'/new_'+str(ind)+'.txt'),'w')
            f.write(content.encode('utf-8'))
            f.close()
    
if __name__=='__main__':
    #
    topics = [('finance','http://finance.huanqiu.com/'),
              ('technology','http://tech.huanqiu.com/'),
              ('entertainment','http://ent.huanqiu.com/'),
              ('fashion','http://fashion.huanqiu.com/'),
              ('world','http://world.huanqiu.com/'),
              ('military','http://mil.huanqiu.com/')]
    run_crawl(topics)