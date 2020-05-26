from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
import scrapy
import os
import mysql.connector
from scrapy.http import Request


class RutenPipeline(object):

    def __init__(self):
        self.create_connection()
        # self.create_table()

    def create_connection(self):
        self.conn = mysql.connector.connect(
            host='projectdatabase.ccew5rh7vbmj.us-east-1.rds.amazonaws.com',
            user='michael',
            password='Baesuzy1',
            database='Project',
            auth_plugin='mysql_native_password'
        )
        self.curr = self.conn.cursor()

    def create_table(self):
        self.curr.execute(
            """CREATE TABLE Product(product_images text, product_name text, product_price text, product_url text, product_category text, product_subcategory text, product_source text)""")

    def process_item(self, item, spider):
        self.store_db(item)
        return item

    def store_db(self, item):
        self.curr.execute("INSERT INTO Product(product_images, product_name, product_price, product_url, product_category, product_subcategory, product_source) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                          (item['product_images'], item['product_name'], item['product_price'], item['product_url'], item['product_category'], item['product_subcategory'], item['product_source']))
        self.conn.commit()

# class ProjectPipeline(ImagesPipeline):
#
#     def file_path(self, request, response=None, info=None):
#         image_guid = request.url.split('/')[-1]
#         return 'full/%s' % (image_guid)
#
#     # Name thumbnail version
#     def thumb_path(self, request, thumb_id, response=None, info=None):
#         image_guid = thumb_id + request.url.split('/')[-1]
#         return 'thumbs/%s/%s.jpg' % (thumb_id, image_guid)
#
#     def get_media_requests(self, item, info):
#         yield Request(item['image_urls'][0], meta=item)
