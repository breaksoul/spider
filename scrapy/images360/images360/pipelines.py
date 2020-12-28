# # Define your item pipelines here
# #
# # Don't forget to add your pipeline to the ITEM_PIPELINES setting
# # See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# # useful for handling different item types with a single interface
# from itemadapter import ItemAdapter
# import pymysql
# from scrapy.pipelines.images import ImagesPipeline
# from scrapy.exceptions import DropItem
# from scrapy import Request


# class ImagesPipeline(ImagesPipeline):# ImagePipeline，继承 Scrapy 内置的 ImagesPipeline，重写下面几个方法
# 	def file_path(self,request,response=None,info=None):
# 		url=request.url
# 		file_name=url.split('/')[-1]
# 		return file_name#的第一个参数 request 就是当前下载对应的 Request 对象。这个方法用来返回保存的文件名，直接将图片链接的最后一部分当作文件名即可


# 	def item_completed(self,results,item,info):
# 		image_paths=[x['path'] for ok,x in results if ok]
# 		if not image_paths:
# 			raise DropItem('Image Downloaded Failed')
# 		return item
# 	def get_media_requests(self,item,info):
# 		yield Request(item['url'])#它的第一个参数 item 是爬取生成的 Item 对象。我们将它的 url 字段取出来，然后直接生成 Request 对象。此 Request 加入到调度队列，等待被调度，执行下载。

# class MysqlPipeline():
# 	def __init__(self,host,database,user,password,port):
# 		self.host=host
# 		self.database=database
# 		self.user=user
# 		self.password=password
# 		self.port=port

# 	@classmethod
# 	def from_crawler(cls,crawler):
# 		return cls(host=crawler.settings.get('MYSQL_HOST'),
#             database=crawler.settings.get('MYSQL_DATABASE'),
#             user=crawler.settings.get('MYSQL_USER'),
#             password=crawler.settings.get('MYSQL_PASSWORD'),
#             port=crawler.settings.get('MYSQL_PORT'),)#这一步主要获得定义在settings中的
# 	def open_spider(self,spider):
# 		self.db=pymysql.connect(self.host, self.user, self.password, self.database, charset='utf8', port=self.port)
# 		self.cursor = self.db.cursor()


# 	def close_spider(self,spider):
# 		self.db.close()


# 	def process_item(self, item, spider):
# 		data=dict(item)
# 		keys=','.join(data.keys())#在字典keys中加入逗号
# 		values = ', '.join(['% s'] * len(data))
# 		sql='insert into %s(%s)values (% s)'% (item.table, keys, values)
# 		self.cursor.execute(sql, tuple(data.values()))
# 		self.db.commit()
# 		return item

#Scrapy 提供了专门处理下载的 Pipeline，包括文件下载和图片下载。下载文件和图片的原理与抓取页面的原理一样，因此下载过程支持异步和多线程，下载十分高效

import pymysql
from scrapy import Request
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline


# class MongoPipeline(object):
#     def __init__(self, mongo_uri, mongo_db):
#         self.mongo_uri = mongo_uri
#         self.mongo_db = mongo_db
    
#     @classmethod
#     def from_crawler(cls, crawler):
#         return cls(
#             mongo_uri=crawler.settings.get('MONGO_URI'),
#             mongo_db=crawler.settings.get('MONGO_DB')
#         )
    
#     def open_spider(self, spider):
#         self.client = pymongo.MongoClient(self.mongo_uri)
#         self.db = self.client[self.mongo_db]
    
#     def process_item(self, item, spider):
#         name = item.collection
#         self.db[name].insert(dict(item))
#         return item
    
#     def close_spider(self, spider):
#         self.client.close()


class MysqlPipeline():
    def __init__(self, host, database, user, password, port):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port
    
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('MYSQL_HOST'),
            database=crawler.settings.get('MYSQL_DATABASE'),
            user=crawler.settings.get('MYSQL_USER'),
            password=crawler.settings.get('MYSQL_PASSWORD'),
            port=crawler.settings.get('MYSQL_PORT'),
        )
    
    def open_spider(self, spider):
        self.db = pymysql.connect(self.host, self.user, self.password, self.database, charset='utf8',
                                  port=self.port)
        self.cursor = self.db.cursor()
    
    def close_spider(self, spider):
        self.db.close()
    
    def process_item(self, item, spider):
        print(item['title'])
        data = dict(item)
        keys = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        sql = 'insert into %s (%s) values (%s)' % (item.table, keys, values)
        self.cursor.execute(sql, tuple(data.values()))
        self.db.commit()
        return item


class ImagePipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        url = request.url
        file_name = url.split('/')[-1]
        return file_name
    
    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem('Image Downloaded Failed')
        return item
    
    def get_media_requests(self, item, info):
        yield Request(item['url'])