# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
from scrapy.pipelines.images import ImagesPipeline
from xiaohuar import settings
from scrapy.exceptions import DropItem
import os

class XiaohuarPipeline(object):
    def process_item(self, item, spider):
        return item

class XiaohuarImagesPipeline(ImagesPipeline):


    def get_media_requests(self, item, info):
        for i, image_url in enumerate(item['image_urls']):
            if not image_url.startswith("http"):
                image_url = 'http://www.xiaohuar.com' + image_url
            yield scrapy.Request(image_url,meta={'item':item,'num':i+1})

    def file_path(self, request, response=None, info=None):
        path = super(XiaohuarImagesPipeline, self).file_path(request,response ,info)
        path = path.replace('full/', '')
        image_format = path.split('.')[-1]
        category = request.meta['item']['title']
        num = request.meta['num']
        image_store = settings.IMAGES_STORE
        category_path = os.path.join(image_store,category )
        #创建文件夹需要用绝对路径
        if not os.path.exists(category_path):
            os.mkdir(category_path)


        image_name = category+ str(num) +'.'+ image_format
        image_path = os.path.join(category , image_name)
        # 注意这里返回的必须是相对路径
        return image_path



    def item_completed(self, results, item, info):
        for ok,x in results:
            if ok:
                url = x['url']
                path = x['path']
                cheksum = x['checksum']
        image_paths = [x['path'] for ok,x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_paths'] = image_paths
        return item