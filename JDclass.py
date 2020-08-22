import requests
import json
import time
import random
import requests
import pymysql
from urllib import parse#parse可以实现解析url，unparse构造url,quote可以实现把中文转化成url编码格式，urlencode实现字典添加到url
from pyquery import PyQuery as pq
from lxml import etree
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class JD(object):
	def __init__(self):
		self.t=round(random.uniform(1,2),1)
		self.headers={'user-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}
		#self.url="http://www.jd.com"
		#获取到得+self.getproxy.为了方便直接添加了可用ip
		self.chrome_options=webdriver.ChromeOptions().add_argument(r'--proxy_server=http://118.113.247.65:9999')
		self.url="https://search.jd.com/Search?"
		#keyword=%E8%8B%B9%E6%9E%9C&wq=%E8%8B%B9%E6%9E%9C&page=1&s=1&click=0"
		self.driver=webdriver.Chrome(executable_path=r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe',chrome_options=self.chrome_options)
		self.ipurl='http://localhost:5000/random'
		self.keyword=keyword
	

	# def getproxy(self):
	# 	try:
	# 		proxy=requests.get(self.ipurl)
	# 		if proxy.status_code==200:
	# 			print('获取成功',proxy.text)
	# 			return proxy.text
	# 		except ConnectionError:
	# 			print('获取失败')
	# 			return None


	def getJD(self,keyword,p,q):


		parms={
		'keyword':keyword,
		'wq':keyword,
		'page':p,
		's':q,
		'click':'0'}
		parmsstr=parse.urlencode(parms)
		
		url=self.url+parmsstr
		print(url)
		
		
		page=self.driver.get(url)
		print('设置窗口大小')
		self.driver.set_window_size(600,800)

		#这段代码可以访问主页，并在搜阔框内输入需要搜索的内容进行爬取
		# xpath=r'//*[@id="shSafetyPV"]'
		# WebDriverWait(driver,15).until(EC.presence_of_element_located((By.XPATH,xpath)))
		# time.sleep(self.t)
		# self.driver.find_element_by_id('key').send_keys(content)
		# self.driver.find_element_by_class_name('button').click()


		xpath2=r'//*[@id="J_filter"]/div[1]/div[1]/a[2]'
		time.sleep(self.t)
		self.driver.find_element_by_xpath(xpath2).click()#排序按照销量

		res=self.driver.page_source
		self.clearpage(res)

	def clearpage(self,res):
		resp=pq(res)
		link=resp("#J_goodsList > ul > li > div > div.p-name.p-name-type-2 > a").items()
		#list=[]
		c=0
		data=[]
		for l in link:
			c+=1
			href=l.attr('href')
			#list.append(href)
			#开始清洗出link中各个产品的信息，放入data
			#for d in list:
			deturl='https:'+href
			self.driver.get(deturl)
			response=self.driver.page_source
			re=etree.HTML(response)
			name=re.xpath(r'/html/body/div[6]/div/div[2]/div[1]/text()')[0].strip()
			price=re.xpath(r'/html/body/div[6]/div/div[2]/div[3]/div/div[1]/div[2]/span[1]/span[2]/text()')
			cnum=re.xpath(r'//*[@id="comment-count"]/a/text()')
			#print(price)
			dict={}
			dict['name']=name
			dict['price']=price
			dict['commentsnum']=cnum
			data.append(dict)
			time.sleep(self.t)
			print('保存产品量',c)


		self.save(data)



	def save(self,data):
		#写入方式一
		print('开始写入')
		with open(r'C:\Users\Administrator\Desktop\python\python example\python3\data saved\JDdata.txt','w') as f:#写入文件
			for a in range(len(data)):
				aa=json.dumps(data[a],ensure_ascii=False)#吧字典类型数据变成字符才能写入
				f.write(aa+'\n')


		#写入方式二
		# sql_1="create table if not exists %s(num int primary key auto_increment,name varchar(45),price char(10),cnum char(10));"%(content)

		# sql_2="insert ignore into iphone(name,price,cnum) values(%s,%s,%s);"%(name,price,cnum)#insert ignore 如果字符过长直接截断不报错，但是insert会报错
	
		# cursor.execute(sql_1)
		# cursor.execute(sql_2)
		print('写入完成')
	def run(self):
		
		count=1

		for i in range(1,3,2):
			p=i
			q=count*50+1
			self.getJD(keyword,p,q)
			print('开始抓取',count)
			count+=1




if __name__ == '__main__':
	#keyword=input('请输入需要查询的内容：')#sublimeinput函数之后好像有问题，以后再测试改成固定值
	keyword='iphone'
	JD=JD()
	JD.run()












