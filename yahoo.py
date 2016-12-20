#-*-encoding:utf-8-*-
from urllib2 import urlopen
from bs4 import BeautifulSoup
import re
import os
import Queue
import time
import random
import threading

mainUrl = 'https://www.yahoo.com/'
lock = threading.Lock()
count = 0

UserAgent = { 
    'User-Agent':
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36',
    'Accept':
    'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
}

def getLinks(pageUrl):
    global pages
    bsObj = None
    try:
        request = mainUrl + pageUrl
        html = urlopen(request, timeout = 20)
        bsObj = BeautifulSoup(html, 'lxml')
    except :
        print 'Error with open', pageUrl
        return
    
    if bsObj:
        if pageUrl == '':
            pageUrl = 'mainPage.html'
        savePath = os.path.join('urls', pageUrl.split('/')[-1])
        lock.acquire()
        global count
        count += 1
        print '%s downloading %d %s'%(
            threading.currentThread().getName(), 
            count, 
            pageUrl)
        lock.release()
        with open(savePath, 'w') as fout:
            fout.write(pageUrl + '\n')
            fout.write(bsObj.encode('utf8'))

        for link in bsObj.findAll('a', href = re.compile('.+\.html')):
            if 'href' in link.attrs:
                if link.attrs['href'] not in pages:
                    newPage = link.attrs['href']
                    # print 'find newPage:', newPage
                    pages.add(newPage)
                    global q
                    q.put(newPage)
        time.sleep(3 + 2*random.random())

def worker():
    while True:
        item = q.get()
        # print 'item:',item
        getLinks(item)
        q.task_done()
        htmlList = os.listdir('urls')
        if len(htmlList) > 1000:
            break

if __name__ == '__main__':
    if not os.path.exists('urls'):
        os.mkdir('urls')
    pages = set()
    pages.add(mainUrl)
    q = Queue.Queue()
    getLinks('')
    
    num_worker_threads = 3
    for i in range(num_worker_threads):
         t = threading.Thread(target=worker) #, args = None, name = None
         t.daemon = True
         t.start()

    q.join() 
    htmlList = os.listdir('urls')
    print 'Download completed'
    print 'Number of HTMLs:', len(htmlList)
    