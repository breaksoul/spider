# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#注意在设置了新的pipeline、之后需要在setting里面更改配置，如果有新的类引入也需要加入到大括号里面
import pymysql
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class TutorialPipeline:
	def __init__(self):
		self.conn=pymysql.Connect(host='localhost',port=3306,user='root',passwd='wb123456789',db='scrapyq',charset='utf8')
		self.cursor=self.conn.cursor()
		self.limit = 30
	def process_item(self, item, spider):
		if item['text']:

			if len(item['text'])>self.limit:
				item['text']= item['text'][0:self.limit].rstrip() + '...'

				# if len(item['tags'])>self.limit:
				# 	item['tags']=item['tags'][0:self.limit].rstrip() + '...'

				sql="insert into quotes(text,author,tags) Values(%s,%s,%s)"

				self.cursor.execute(sql,(item['text'],item['author'],item['tags']))#mysqlOperand should contain 1 column(s)，就是需要再多一列， 原因是因为tags中的数据十多个 写入mysql就报错更改之后就ok了
				self.conn.commit()
			return item

		else:
			return DropItem('Missing Text')
