from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from urllib import parse
from lxml import etree
import json



class Douban(object):
	def __init__(self):
		self.driver=webdriver.Chrome(executable_path=r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
		self.url='https://search.douban.com/book/subject_search?'
		#https://search.douban.com/book/subject_search?   search_text=%E8%92%99%E5%A4%AA%E5%A5%87&cat=1001&start=15
		#self.parse()
		print('initial varities succed')
	def spider(self,url,xpath):
		response=self.driver.get(url)
		waitelement=WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH,xpath)))#报错_init__() takes 2 positional arguments but 3 were given_需要在locator在嵌套一层括号变成一个元祖成为一个整体
		#print (response)
		return self.driver.page_source

		print('gain pagesource...')
		print(response,self.driver.page_source)

	def dataclean(self,data):
		item={}
		results=[]
		#bookname，score,comments,detailslinks,price
		#网页上有一个div是从div【2】开始的，如果知己额匹配所有会把第一个匹配上，可以用到position（）函数//li[position()<=3]/a/text()'
		bookname=r'//*[@id="root"]/div/div[2]/div[1]/div[1]//div[position()>=2]/div/div/div[1]/a/text()'
					#
                                        #//*[@id="root"]/div/div[2]/div[1]/div[1]/div[2]/div/div/div[1]/a
					#//*[@id="root"]/div/div[2]/div[1]/div[1]/div[3]/div/div/div[1]/a

		sore=r'//*[@id="root"]/div/div[2]/div[1]/div[1]//div[position()>=2]/div/div/div[2]/span[2]/text()'

		#//*[@id="root"]/div/div[2]/div[1]/div[1]//div[position()>=2]/div/div/div[2]/span[2]
	

		comments=r'//*[@id="root"]/div/div[2]/div[1]/div[1]//div[position()>=2]/div/div/div[2]/span[3]/text()'

		detailslinks=r'//*[@id="root"]/div/div[2]/div[1]/div[1]//div[position()>=2]/div/div/div[1]/a/@href'

		price=r'//*[@id="root"]/div/div[2]/div[1]/div[1]//div[position()>=2]/div/div/div[3]/text()'
				#//*[@id="root"]/div/div[2]/div[1]/div[1]/div[3]/div/div/div[3]
		print('dataclean start...')

		result=etree.HTML(data)#书名和评分有问题

		name=result.xpath(bookname)
		scores=result.xpath(sore)
		comment=result.xpath(comments)
		links=result.xpath(detailslinks)
		price=result.xpath(price)

		print(len(name),len(scores),len(comment),len(links),len(price),end='\n')
		print(name,scores,comment,links,price)

		for i in range(len(name)):#要注意range函数中（）默认从0到结尾，例如（0,14），实际上i取到了13，但不包含结束，索引是从0开始所以限制让个范围为0到len（bookname-1）
			item['书名']=name[i]
			item['得分']=scores[i]
			item['评论']=comment[i]
			item['链接']=links[i]
			item['价格']=price[i]
			results.append(item)

		return results
		print('dataclean finished')
	def savedata(self,results):
		print('savedata start...')
		try:
			with open(r'C:\Users\Administrator\Desktop\python\python example\python3\data saved\豆瓣读书.txt','a',encoding='utf-8')as f:

				f.write(json.dumps(results))
				print('succeed')

		except Exception as e:
			print('write error',e)

	def run(self):#search_text=python&cat=1001&start=%s
		#page=input('please enter the page number:')
		#kw=input('please enter the content you want to search:')
		page='1'
		kw='python'
		for n in range(int(page)):
			params={'search_text':kw,
			'cat':'1001',
			'start':page}

			url=self.url+parse.urlencode(params)
			print(url)
			result=self.spider(url,r'//*[@id="root"]/div/div[2]/div[1]/div[1]/div[2]/div/div')
			results=self.dataclean(result)
			self.savedata(results)


if __name__=='__main__':
	douban=Douban()
	douban.run()
