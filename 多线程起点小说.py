import threading
import requests
from lxml import etree
from urllib import request
import os
import re
from queue import Queue
class Producer(threading.Thread):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
    }
    def __init__(self,page_queue,img_queue,*args,**kwargs):
        super(Producer, self).__init__(*args,**kwargs)
        self.page_queue = page_queue
        self.img_queue = img_queue


    def run(self):
        while True:
            if self.page_queue.empty():
                break
            url = self.page_queue.get()
            self.parse_page(url)

    def parse_page(self,url):

        response = requests.get(url,headers=self.headers)
        text = response.text
        html = etree.HTML(text)
        books = html.xpath('//div[@class="book-img-box"]//a/@href')
        for book in books:
             self.img_queue.put(book)

class Consumer(threading.Thread):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
    }
    def __init__(self,page_queue,img_queue,*args,**kwargs):
        super(Consumer, self).__init__(*args,**kwargs)
        self.page_queue = page_queue
        self.img_queue = img_queue

    def run(self):
        while True:
            if self.img_queue.empty():
                if self.page_queue.empty():
                    return
                    # print(book)
            img = self.img_queue.get(block=True)
            book = img
            book_url = 'https:' + book + "#Catalog"
            response2 = requests.get(book_url, headers=self.headers)
            text = response2.text
            html2 = etree.HTML(text)
            book2s = html2.xpath('//ul[@class="cf"][1]//li//a/@href')
            book_name = html2.xpath('//div[@class="book-info "]//h1//em//text()')[0]

            print(book_name)
            for book2 in book2s:
                print(book2)
                text_url = 'https:' + book2
                response3 = requests.get(text_url, headers=self.headers)
                res = response3.text

                html3 = etree.HTML(res)
                text = html3.xpath('//div[@class="read-content j_readContent"]//p/text()')
                title = html3.xpath('//h3[@class="j_chapterName"]/text()')[0]
                print(title)
                with open(str(book_name) + '.txt', 'a', encoding='utf-8') as f:
                    f.write(title + '\n')
                    for i in text:
                        f.write(i)



def main():
    page_queue = Queue(10)
    img_queue = Queue(50)
    for x in range(1,9):
        url = "https://www.qidian.com/free/all?orderId=&vip=hidden&style=1&pageSize=20&siteid=1&pubflag=0&hiddenField=1&page=%d" % x
        page_queue.put(url)

    for x in range(5):
        t = Producer(page_queue,img_queue)
        t.start()

    for x in range(5):
        t = Consumer(page_queue,img_queue)
        t.start()

if __name__ == '__main__':
    main()

