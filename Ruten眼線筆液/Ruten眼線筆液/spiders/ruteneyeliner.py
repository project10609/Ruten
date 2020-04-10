import scrapy
from selenium import webdriver
from ..items import RutenItem
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from scrapy.http import Request
import os


class RuteneyelinerSpider(scrapy.Spider):
    name = 'ruteneyeliner'

    start_urls = ['https://find.ruten.com.tw/c/0012000500020003']

    page = 2

    def __init__(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.action = webdriver.ActionChains(self.driver)

    def parse(self, response):
        self.driver.get(response.url)
        res = self.driver.execute_script("return document.documentElement.outerHTML")
        soup = BeautifulSoup(res,'html.parser')

        for href in soup.find_all('h5',{'class':'prod_name'}):
            url = href.find('a').attrs['href']
            yield Request(url,callback=self.parse_item)

        next_page = 'https://find.ruten.com.tw/c/0012000500020003?p=' + str(RuteneyelinerSpider.page)
        if  RuteneyelinerSpider.page <= 10:
                # self.action.pause(1)
                # self.action.perform()
             RuteneyelinerSpider.page += 1
            url = next_page
            yield response.follow(url, callback=self.parse)

    def parse_item(self,response):
        self.driver.get(response.url)
        res = self.driver.execute_script("return document.documentElement.outerHTML")
        item = RutenItem()
        soup = BeautifulSoup(res, 'html.parser')

        img = []
        item['product_url'] = str(response.request.url)
        for image in soup.find_all('div',{'class':'item-image-wrap'}):
            url = image.find('img').attrs['src']
            img.append(url)
        item['product_images'] = img[0]
        item['product_name'] = soup.find('span',{'class':'vmiddle'}).text
        item['product_price'] = soup.find('strong', {'class': 'rt-text-xx-large'}).text.replace('$','').replace(',','')
        item['product_category'] = 'EyeLiner'
        item['product_source'] = 'Ruten'
        yield item
