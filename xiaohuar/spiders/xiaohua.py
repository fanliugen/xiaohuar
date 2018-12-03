# -*- coding: utf-8 -*-
import scrapy
from  xiaohuar.items import XiaohuarItem
from copy import deepcopy

class XiaohuaSpider(scrapy.Spider):
    name = 'xiaohua'
    allowed_domains = ['xiaohuar.com']
    start_urls = ['http://www.xiaohuar.com/list-1-0.html']

    def parse(self, response):
        itemList = response.xpath("//div[@class = 'item masonry_brick']")
        for item in itemList:
            itemInfo = XiaohuarItem()
            itemInfo['name'] = item.xpath(".//div[@class='item_t']//span[@class='price']/text()").extract_first(default='')
            itemInfo['school'] = item.xpath(".//div[@class='btns']//a/text()").extract_first(default='')
            itemInfo['title'] = item.xpath(".//div[@class='title']//a/text()").extract_first(default='')
            itemInfo['portrait'] = item.xpath(".//div[@class='img']//img/@src").extract_first(default='')
            if not itemInfo['portrait'].startswith('http'):
                itemInfo['portrait'] = 'http://www.xiaohuar.com' + itemInfo['portrait']

            itemInfo['detailUrl'] = item.xpath(".//div[@class='img']//a/@href").extract_first(default='')


            yield scrapy.Request(itemInfo['detailUrl'],callback=self.parse_detail,meta={'item':deepcopy(itemInfo)})

            next_url = response.xpath("//div[@class='page_num']//a[last()-1]/@href").extract_first(default=None)
            if next_url:
                yield scrapy.Request(next_url, callback= self.parse)



    def parse_detail(self,response):
        itemInfo = response.meta['item']
        itemInfo['xingzuo'] = response.xpath("//div[@class='infodiv']//table//tbody/tr[3]//td[2]/text()").extract_first(default='')
        itemInfo['occupation']=response.xpath("//div[@class='infodiv']//table//tbody/tr[last()-1]//td[2]/text()").extract_first(default='')
        # itemInfo['image_urls']= response.xpath("//div[@class='post_entry']/ul[@class='photo_ul']//li//a/img/@src").extract()
        photourl = response.xpath("//ul[@class='photo_ul']//div[@class='p-tmb']/a/@href").extract_first(default=None)
        if photourl:
            yield scrapy.Request(photourl ,  callback=self.parse_imageurl,meta={'item':deepcopy(itemInfo)})
        # print(itemInfo)
        # yield itemInfo

    def parse_imageurl(self,response):
        itemInfo = response.meta['item']
        image_urlsRaw = response.xpath("//ul[@class='ad-thumb-list']//li//div[@class='inner']//a/@href").extract()
        image_urls = []
        for image_url in image_urlsRaw:
            if not  image_url.startswith('http'):
                image_url = 'http://www.xiaohuar.com' + image_url
                image_urls.append(image_url)
        itemInfo['image_urls'] = image_urls

        yield itemInfo