import scrapy
from selenium import webdriver
from ..items import RutenItem
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from scrapy.http import Request
import os


class RutenremoverSpider(scrapy.Spider):
    name = 'rutenremover'

    start_urls = ['https://find.ruten.com.tw/c/001200070011']

    page = 2

    def __init__(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.action = webdriver.ActionChains(self.driver)

    def parse(self, response):
        self.driver.get(response.url)
        res = self.driver.execute_script(
            "return document.documentElement.outerHTML")
        soup = BeautifulSoup(res, 'html.parser')

        main = soup.find_all('h5', {'class': 'prod_name'})
        oversea = soup.find_all('h5', {'class': 'prod_oversea'})

        for href in main:
            url = href.find('a').attrs['href']
            yield Request(url, callback=self.parse_item)

        for href in oversea:
            url2 = href.find('a').attrs['href']
            yield Request(url2, callback=self.parse_item)

        next_page = 'https://find.ruten.com.tw/c/001200070011?p=' + \
            str(RutenremoverSpider.page)
        if RutenremoverSpider.page <= 4:
            # self.action.pause(1)
            # self.action.perform()
            RutenremoverSpider.page += 1
            url = next_page
            yield response.follow(url, callback=self.parse)

    def parse_item(self, response):
        self.driver.get(response.url)
        res = self.driver.execute_script(
            "return document.documentElement.outerHTML")
        item = RutenItem()
        soup = BeautifulSoup(res, 'html.parser')

        img = []
        item['product_url'] = str(response.request.url)
        for image in soup.find_all('div', {'class': 'item-image-wrap'}):
            url = image.find('img').attrs['src']
            img.append(url)
        item['product_images'] = img[0]
        item['product_name'] = soup.find('span', {'class': 'vmiddle'}).text
        item['product_price'] = soup.find(
            'strong', {'class': 'rt-text-xx-large'}).text.replace('$', '').replace(',', '')
        item['product_category'] = 'Remover'
        item['product_subcategory'] = 'remover'
        item['product_source'] = 'Ruten'
        yield item
