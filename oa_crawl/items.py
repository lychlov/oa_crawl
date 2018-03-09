# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class OaCrawlItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # pass
    # 我们要爬取的字段：姓名、ID、性别、职位等等
    name = scrapy.Field()
    user_id = scrapy.Field()
    gender = scrapy.Field()
    title = scrapy.Field()
    department = scrapy.Field()
    mobile_phone = scrapy.Field()
    email_add = scrapy.Field()
    image_url = scrapy.Field()
