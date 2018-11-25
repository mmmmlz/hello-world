from selenium import webdriver
import time
from lxml import etree
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
class LagouSpider(object):
    driver_path = r'D:\python\Scripts\chromedriver.exe'
    def __init__(self):
        self.driver = webdriver.Chrome(executable_path=LagouSpider.driver_path)
        self.url ='https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput='
        self.positions =[]

    def run(self):
        self.driver.get(self.url)
        while True:

            source = self.driver.page_source
            #用于等待下一页的按钮出现后再进行点击
            WebDriverWait(driver=self.driver,timeout = 15).until(
                EC.presence_of_element_located((By.XPATH,'//div[@class="pager_container"]/span[last()]')))
            #页面加载完毕后 解析页面
            self.parse_list_page(source)
            next_bt = self.driver.find_element_by_xpath('//div[@class="pager_container"]/span[last()]')
            #判断是否到了最后一页
            if "pager_next_disabled" in next_bt.get_attribute('class'):
                break
            else:
                next_bt.click()
            time.sleep(2)


    def parse_list_page(self,source):
        html = etree.HTML(source)
        links =html.xpath('//a[@class="position_link"]/@href')
        for link in links:
            self.request_detail_page(link)
            time.sleep(1)

    def request_detail_page(self,url):
        #用新窗口打开页面
        self.driver.execute_script("window.open('%s')" %url)
        #切换到新窗口
        self.driver.switch_to.window(self.driver.window_handles[1])
        #等待页面加载完成
        WebDriverWait(driver=self.driver, timeout=10).until(
           EC.presence_of_element_located((By.XPATH, "//div[@class='job-name']/span[@class='name']")))
        source = self.driver.page_source
        #开始爬取页面
        self.parse_detail_page(source)
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])
    def parse_detail_page(self,source):
        html = etree.HTML(source)
        position_name = html.xpath("//span[@class='name']/text()")[0]
        job_request_spans = html.xpath("//dd[@class='job_request']//span")
        salary = job_request_spans[0].xpath(".//text()")[0].strip()
        city = job_request_spans[1].xpath(".//text()")[0].strip()
        city = re.sub(r"[\s/]","",city)
        work_years = job_request_spans[2].xpath(".//text()")[0].strip()
        work_years = re.sub(r"[\s/]","",work_years)
        education = job_request_spans[3].xpath(".//text()")[0].strip()
        education = re.sub(r"[\s/]","",education)
        desc = "".join(html.xpath("//dd[@class='job_bt']//text()")).strip()
        #desc = re.sub(r"[\\n]", "", desc)
        company = html.xpath("//h2[@class='fl']/text()")[0].strip()
        position = {
                'name':position_name,
                'campany':company,
                'salary':salary,
                'city':city,
                'work_years':work_years,
                'education':education,
                'desc': desc

        }
        self.positions.append(position)
        print(position)





if __name__ == '__main__':
    spider = LagouSpider()
    spider.run()