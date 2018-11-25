from selenium import webdriver
import time
from lxml import etree
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import requests
class LagouSpider(object):
    driver_path = r'D:\python\Scripts\chromedriver.exe'
    def __init__(self):
        self.driver = webdriver.Chrome(executable_path=LagouSpider.driver_path)
        self.url ='https://www.qidian.com/free/all?action=1&orderId=&page=1&vip=hidden&style=1&pageSize=20&siteid=1&pubflag=0&hiddenField=1'
        self.positions =[]

    def run(self):
        self.driver.get(self.url)
        i = 5
        while i > 0:

            source = self.driver.page_source
            #用于等待下一页的按钮出现后再进行点击
            WebDriverWait(driver=self.driver,timeout = 15).until(
                EC.presence_of_element_located((By.XPATH,'//li[@class="lbf-pagination-item"][last()]')))
            #页面加载完毕后 解析页面
            self.parse_list_page(source)
            next_bt = self.driver.find_element_by_xpath('//li[@class="lbf-pagination-item"][last()]')
            #判断是否到了最后一页
            i -= i
            next_bt.click()
            time.sleep(2)


    def parse_list_page(self,source):
        html = etree.HTML(source)
        links =html.xpath('//div[@class="book-img-box"]//a/@href')
        for link in links:
            self.request_detail_page(link)
            time.sleep(1)

    def request_detail_page(self,url):
        #用新窗口打开页面
        url = 'https:' + url + "#Catalog"
        self.driver.execute_script("window.open('%s')" %url)
        #切换到新窗口
        self.driver.switch_to.window(self.driver.window_handles[1])
        #等待页面加载完成
        WebDriverWait(driver=self.driver, timeout=10).until(
           EC.presence_of_element_located((By.XPATH, '//div[@class="volume"]//li[last()]')))
        source = self.driver.page_source
        #开始爬取页面
        self.parse_detail_page(source)
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])
    def parse_detail_page(self,source):
        html = etree.HTML(source)
        charpters = html.xpath('//div[@class="volume"]//li/a')
        book_name = html.xpath('//div[@class="book-info "]//h1//em//text()')[0]
        for charpter in charpters:
            charpter_url =charpter.get('href')

            self.download(charpter_url,book_name)

    def download(self,url,book_name):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
        }
        text_url = 'https:' + url
        response3 = requests.get(text_url, headers=headers)
        res = response3.text
        html3 = etree.HTML(res)
        text = html3.xpath('//div[@class="read-content j_readContent"]//p/text()')
        name = html3.xpath('//h3[@class="j_chapterName"]/text()')[0]
        print(name)
        with open(str(book_name) + '.txt', 'a', encoding='utf-8') as f:
            f.write(name + '\n')
            for i in text:
                f.write(i)





if __name__ == '__main__':
    spider = LagouSpider()
    spider.run()