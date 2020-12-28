# import scrapy
# from scrapy import Spider, Request#需要构造生成request
# from urllib.parse import urlencode
# import json
# from images360.items import ImageItem
# class ImagesSpider(scrapy.Spider):
# 	name = 'images'
# 	allowed_domains = ['images.so.com']
# 	start_urls = ['http://images.so.com/']
# 	def start_requests(self):
# 		data = {'ch': 'photography','sn':0 ,'listtype': 'new','temp':'1'}#为了构造url=https://image.so.com/z?ch=photography&listtype=new
# 		base_url = 'https://image.so.com/zj?'
# 		for page in range(1,self.settings.get('MAX_PAGE') + 1):
# 			data['sn']=page*30#360摄影是用了ajax方法，主要请求的网址是属于https://image.so.com/zjl?ch=photography&sn=150&listtype=new&temp=1，sn的数值是按照30的一定倍数变化
# 			parms=urlencode(data)
# 			url=base_url+parms
# 			yield Request(url, self.parse)#引入request






# 	def parse(self, response):
# 		result= json.loads(response.text)#因为抓到的格式是json

# 		for image in result.get('list'):#这里的get方法，相当于dict.get（）方法可以直接遍历list的字段，取出一个个图片信息，然后赋值
# 			item = ImageItem()
# 			item['id'] = image.get('imageid')
# 			item['url'] = image.get('qhimg_url')
# 			item['title'] = image.get('group_title')
# 			item['thumb'] = image.get('qhimg_thumb_url')
# 			yield item

# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from urllib.parse import urlencode
import json
from images360.items import ImageItem


class ImagesSpider(Spider):
    name = 'images'
    allowed_domains = ['images.so.com']
    start_urls = ['http://images.so.com/']
    
    def start_requests(self):
        data = {'ch': 'photography', 'listtype': 'new'}
        base_url = 'https://image.so.com/zjl?'
        for page in range(1, self.settings.get('MAX_PAGE') + 1):
            data['sn'] = page * 30
            params = urlencode(data)
            url = base_url + params
            print(url,"url是什么东西呢")
            yield Request(url, self.parse)
    
    def parse(self, response):
        result = json.loads(response.text)
        for image in result.get('list'):
            item = ImageItem()
            item['id'] = image.get('id')
            item['url'] = image.get('qhimg_url')
            item['title'] = image.get('title')
            item['thumb'] = image.get('qhimg_thumb')
            print('item', item)
            yield item
