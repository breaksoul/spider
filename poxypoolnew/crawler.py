import requests
import json
from pyquery import PyQuery as pq
from lxml import etree


class ProxyMetaclass(type):
	def __new__(cls,name,bases,attrs):
		count=0
		attrs['__CrawlFunc__']=[]#创建一个dict
		for k,v in attrs.items():
			if 'crawl_' in k:
				attrs['__CrawlFunc__'].append(k)
				count+=1
		attrs['__CrawlFuncCount__'] = count
		return type.__new__(cls,name,bases,attrs)
#从元类继承
class Crawler(object,metaclass=ProxyMetaclass):
	def get_proxies(self,callback):
		proxies=[]
		for proxy in eval("self.{}()".format(callback)):#eval函数是直接执行传入的表达式或函数等，并返回值
			print('成功获取到代理', proxy)
			proxies.append(proxy)

		return proxies

	# def crawl_xicidaili(self,page_count=2):#网站已经关闭了

	# 	start_url='https://www.xicidaili.com/nn/{}'
	# 	urls = [start_url.format(page) for page in range(1, page_count + 1)]#用formate构造一个完整的url
	# 	for url in urls:
	# 		req=requests.get(url)
	# 		if req:
	# 			doc= pq(req)
	# 			its=doc("tr").items()#pyquery清洗出tr节点，生成之后是一个生成器需要用for循环取出来，对比xpath等pyquery取出的内容还能二次继续筛选
	# 			for tr in its:
	# 				ip=tr.find('td:nth-child(2)').text()#在tr中找出。。。
	# 				port=tr.find('td:nth-child(3)').text()
	# 				yield ':'.join([ip, port])#在两者间加入：就变成了一个完整的ip
	# def crawl_goubanjia(self):#网站已经关闭了
	# 	start_url = 'http://www.goubanjia.com/free/gngn/index.shtml'
	# 	html = get_page(start_url)
	# 	if html:
	# 		doc = pq(html)
	# 		tds = doc('td.ip').items()
	# 		for td in tds:
	# 			td.find('p').remove()
	# 			yield td.text().replace(' ', '')
	def crawl_89daili(self, page_count=4):
		start_url='http://www.89ip.cn/index_{}.html'
		urls=[start_url.format(page) for page in range(1, page_count + 1)]
		for url in urls:
			req=requests.get(url).text
			if req:
				#print(req.text)

				# html=etree.HTML(req)
				# ips=html.xpath(r'/html/body/meta"utf-8"/div[3]/div[1]/div/div[1]/table/tbody//tr/td[1]/text()')

				# ports=html.xpath(r'/html/body/meta"utf-8"/div[3]/div[1]/div/div[1]/table/tbody//tr/td[2]/text()')
				# for i in range(len(ips)):
				# 	yield ':'.join([ips[i], port[i]])

				doc= pq(req)#用pyquery清洗
				#print(doc)
				its=doc('tr').items()
				for tr in its:
					ip=tr.find('td:nth-child(1)').text()
					port=tr.find('td:nth-child(2)').text()
					
					yield ':'.join([ip, port])



	def crawl_dieniao(self,page_count=4):
		start_url='https://www.dieniao.com/FreeProxy/{}.html'
		urls=[start_url.format(page) for page in range(1, page_count + 1)]
		for url in urls:
			req=requests.get(url).text
			if req:

				doc= pq(req)
				its=doc('li.f-list col-lg-12 col-md-12 col-sm-12 col-xs-12').items()#找到class=。。的li标签

				for tr in its:
					ip=tr.find('span.f-address').text()	
					port=tr.find('span:nth-child(2)')
					yield ':'.join([ip, port])

	# def crawl_proxy360(self):#已经不能用了

	# 		"""
	# 		获取Proxy360
	# 		:return: 代理
	# 		"""
	# 	start_url = 'http://www.proxy360.cn/Region/China'
	# 	print('Crawling', start_url)
	# 	html = get_page(start_url)
	# 	if html:
	# 		doc = pq(html)
	# 		lines = doc('div[name="list_proxy_ip"]').items()
	# 		for line in lines:
	# 			ip = line.find('.tbBottomLine:nth-child(1)').text()
	# 			port = line.find('.tbBottomLine:nth-child(2)').text()
	# 			yield ':'.join([ip, port])
