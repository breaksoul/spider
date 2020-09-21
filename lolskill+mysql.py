import requests
from lxml import etree
from selenium import webdriver
import json
import threading
from queue import Queue

class lol(threading.Thread):
	def __init__(self,name):
		threading.Thread.init(self)
		self.name=name
		self.url=url
		self.herourl=herourl
		self.driver=driver
		self.headers=headers

	def spiderID(self,html):
		
		#清洗出英雄的link
		herolinks=html.xpath(r'//*[@id="jSearchHeroDiv"]//li/a/@href')
		#heroname=html.xpath(r'//*[@id="jSearchHeroDiv"]//li/a/p/text()')名称可以后面在清洗
		
		return herolinks



	def spiderURL(self,link):
		
		id=link.split('=',-1)[-1]#这一步主要是为了练习split函数不切隔直接用12345代替lol英雄id符合网页
		baseurl=self.herourl+id+'.js'
		
		skillres=requests.get(baseurl,headers=self.headers)
		result=json.loads(skillres.text)
		
		return result

	def spiderNM(self,result):
		item_name={}

		item_name['英雄名称']=result['hero']['name']+''+result['hero']['title']

		return item_name
	
	def spiderSK(self,skill):
		item_skills={}

		item_skills['技能名称']=skill['name']+':'+skill['description']

		return item_skills

	def datasave(self,hero_list):
		print('开始保存数据...')
		hero_list=json.dumps(hero_list)#把数据变为字符串的形式才能保存
		with open(r'C:\Users\Administrator\Desktop\python\python example\python3\data saved\lol英雄技能.txt','w',encoding='utf-8') as f:
			f.write(hero_list.encode('utf-8').decode('unicode_escape'))
		print('保存完成')
	


	def run(self):
		hero_list=[]
		self.driver.get(url)
		html=etree.HTML(driver.page_source)
		print('获取英雄ID...')
		herolinks=self.spiderID(html)
		print('英雄ID获取完成')
		print('开始获取英雄名称以及技能')
		count=0
		for link in herolinks:
			heroname=[]
			
			result=self.spiderURL(link)

			#将结果接入到一个heroname中
			heroname.append(self.spiderNM(result))
			count+=1
			print('已经获取'+str(count)+'个英雄')
			for skill in result['spells']:
				heroname.append(self.spiderSK(skill))
				
				
			#注意每放一个英雄的技能和名称到heroname中必须要再推送到hero_list中一次性保存，方便查看
			hero_list.append(heroname)
		self.datasave(hero_list)

if __name__ == '__main__':
	url='http://lol.qq.com/data/info-heros.shtml'
	herourl='http://game.gtimg.cn/images/lol/act/img/js/hero/'
	driver=webdriver.Chrome(executable_path=r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
	headers={'Accept': 'application/json, text/javascript, */*; q=0.01',
	'Origin': 'http://lol.qq.com',
	'Referer': 'http://lol.qq.com/data/info-defail.shtml?id='+str(id),
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}
	#创建一个队列
	q=Queue()
	#初始化任务队列，把
	lol=lol()
	lol.run()
			
			
			
			




		
