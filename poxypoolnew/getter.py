from db import redisclient
from crawler import Crawler

POOL_UPPER_THRESHOLD = 1000#设置一个阈值
class Getter():
	def __init__(self):
		self.redis=redisclient()
		self.crawler = Crawler()#调用其他的函数也得初始化
	def is_over_threshold(self):
		#判断有没有达到代理池的阈值
		if self.redis.count()>=POOL_UPPER_THRESHOLD:
			return True

		else:
			return False

	def run(self):
		print('获取器开始执行')
		if not self.is_over_threshold():#也就是当这个函数返回值是true的时候就停止，false就继续
			for callback_label in range(self.crawler.__CrawlFuncCount__):
				callback=self.crawler.__CrawlFunc__[callback_label]#开始用元类属性__CrawlFunc__中的函数，callback_label是索引，记住这个时候只是把元素拿出来
				proxies = self.crawler.get_proxies(callback)#开始用get_proxies函数调用callback，get_proxy中用了eval函数，直接调用callback获取结果这是个函数
				for proxy in proxies:#每一个ip都取出来加到redis
					self.redis.add(proxy)
