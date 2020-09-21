#2020 6 21y运行成功
import requests
import threading
from lxml import etree
from queue import Queue
import time

class biquge(threading.Thread):#继承多线程
	def __init__(self,q=None,crawl=None):
		threading.Thread.__init__(self)
		self.url=url
		self.base_url=base_url
		self.headers=headers
		self.q=q#队列
		self.crawl=crawl#多线程传入的名称

	def yuanma(self,url,headers):
		response=requests.get(url,headers=headers).text
		html=etree.HTML(response)
		#清洗出小说的链接
		novellinks=html.xpath(r'//*[@id="main"]/div[2]/ul[1]/li[position()>=2 and position()<=20]/a/@href')
		return novellinks
	def novel(self):
		while True:
			if self.q.empty():#
				break
                #从队列中拿出url
			link=q.get()
			print(link)
			res=requests.get(link).text
			res=res.encode('ISO-8859-1').decode(requests.utils.get_encodings_from_content(res)[0])
			result=etree.HTML(res)
			novelname=result.xpath(r'//*[@id="info"]/h1/text()')
			contenttitle=result.xpath(r'//*[@id="list"]/dl/dd[1]/a/text()')
			contentlinks=result.xpath(r'//*[@id="list"]/dl/dd[1]/a/@href')
			self.novelcontent(novelname,contenttitle,contentlinks)
	
	def novelcontent(self,novelname,contenttitle,contentlinks):
		for n in range(len(contentlinks)):
			item={}
			contentlink=base_url+contentlinks[n]
			conres=requests.get(contentlink).text
			conres=conres.encode('ISO-8859-1').decode(requests.utils.get_encodings_from_content(conres)[0])
			conres=etree.HTML(conres)
			conresult=''.join(conres.xpath(r'//*[@id="content"]//text()'))
			item['content']=conresult
			item['title']=contenttitle[n]
			with open(r'C:\Users\Administrator\Desktop\python\python example\python3\data saved\new pen fun\{}.txt'.format(novelname),'a+',encoding='utf-8')as f:
				f.write(item['title'].replace('','\n'))
				f.write(item['content'].strip())

	def run(self):
		self.novel()#从获取图书链接开始
		#novellinks=self.yuanma(self.url,self.headers)

			
if __name__ == '__main__':
	start = time.time()
	url='http://www.xbiquge.la/paihangbang'
	base_url='http://www.xbiquge.la'
	headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}
	b=biquge()
	q=Queue()
	novellinks=b.yuanma(url,headers)#用直接调用类属性函数yuanma
	for link in novellinks:
		q.put(link)

	crawllist=[1, 2, 3, 4, 5]#定义五个线程
	list=[]
	for crawl in crawllist:
		novel=biquge(q,crawl)#有问题不能调用
		novel.start()
		list.append(novel)
		print('%s 正在运行' % threading.current_thread().name)#返回正在运行的线程名称
		print('%s 正在运行线程总数' % threading.active_count())#返回正在运行的线程总数

	for i in list:
		i.join()
	print(time.time()-start)


	

