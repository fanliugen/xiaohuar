# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class XiaohuarItem(scrapy.Item):
    name = scrapy.Field()
    school = scrapy.Field()
    title = scrapy.Field()
    portrait = scrapy.Field()
    detailUrl = scrapy.Field()
    xingzuo = scrapy.Field()
    occupation = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    image_paths = scrapy.Field()