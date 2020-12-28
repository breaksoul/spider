import scrapy
#from lxml import etree
from tutorial.items import TutorialItem



class QuotesSpider(scrapy.Spider):
	name = "quotes"
	allowed_domains = ["quotes.toscrape.com"]
	start_urls = ['http://quotes.toscrape.com/']

	
    	#数据的清洗可以用xpath也可以用css
   		#第一种  用xpath清洗
		# con=etree.HTML(response.text)#can only parse strings
		# cont=con.xpath(r'/html/body/div/div[2]/div[1]//div')
    	
		#在xpath（）后使用extract（）可以返回所有的元素结果。
		# #若xpath（）有问题，那么extract（）会返回一个空列表。
		# #在xpath（）后使用extract_first（）可以返回第一个元素结果。
		# for c in cont:

		# 	item=TutorialItem()
		# 	a=c.xpath(r'//span[1]/text()')
		# 	item['text']=a[-1]
		# 	print(type(item['text']),'-------------------------------------------------------------------------------------------')
		# 	b=c.xpath(r'//span[2]/small/text()')
		# 	item['author']=b[-1]
		# 	print(type(item['author']),'-------------------------------------------------------------------------------------------')
			

		# 	c=c.xpath(r'//html/body/div/div[2]/div[1]/div[1]/div/meta/@content')
		# 	item['tags']=c[-1]
		# 	print(type(item['tags']),'-------------------------------------------------------------------------------------------')

#第二种  用css清洗extract(),获取所有结果组成列表， extract_first ()获取第一个元素即可
	def parse(self, response):
		quotes=response.css('.quote')
		for quote in quotes:
			item=TutorialItem()
			item['text'] = quote.css('.text::text').extract_first()
			#print(item['text'],'---------------------------------------------------------------------------------------------------')
			item['author'] = quote.css('.author::text').extract_first()
			#print(item['author'],'---------------------------------------------------------------------------------------------------')
			item['tags'] = quote.css('.tags .tag::text').extract_first()
			#print(item['tags'],'---------------------------------------------------------------------------------------------------')
			yield item




	   	#网页上面的下一页构造
		#next=con.xpath(r'/html/body/div/div[2]/div[1]/nav/ul/li/a/@href')# 这个是通过xpath构造
		next=response.css('.pager .next a::attr("href")').extract_first()
		#print('next=',next)
     	#构造url,urljoin()方法可以对url进行拼接
		url=response.urljoin(next)#注意这个构造必须是respnse构造
		#print(url)
		yield scrapy.Request(url=url, callback=self.parse)#直接回调，当指定了该回调函数获取到响应，引擎会将该响应作为参数传递给这个回调函数

		

