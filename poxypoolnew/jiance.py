
VALID_STATUS_CODES = [200]
TEST_URL = 'http://www.baidu.com'
BATCH_TEST_SIZE = 100
from db import redisclient
import asyncio
import aiohttp
import time
class Tester(object):
	def __init__(self):
		self.redis = redisclient()
		print('测试初始化')
	async def test_single_proxy(self,proxy):
		conn=aiohttp.TCPConnector(verify_ssl=False)#避免查看网站证书
		async with aiohttp.ClientSession(connector=conn) as session:
			try:
				if isinstance(proxy,bytes):
					proxy=proxy.decode('utf-8')
				real_proxy='http://'+proxy
				print('正在测试',proxy)
				async with session.get(TEST_URL,proxy=real_proxy,timeout=20) as response:
					if response.status in VALID_STATUS_CODES:
						self.redis.max(proxy)
						print('代理可用',proxy)
					else:
						self.redis.decrease(proxy)
						print('请求响应码不合，降低得分', proxy)
			except Exception as e:
				self.redis.decrease(proxy)#也减少得分
				print('请求失败',e)
	def run(self):
		print('测试器开始执行')
		try:
			proxies=self.redis.all()
			loop=asyncio.get_event_loop()#
			#loop=asyncio.new_event_loop()
			
			print('批量测试开始')
			#批量开始测试
			for i in range(0,len(proxies),BATCH_TEST_SIZE):#按照数目来分割
				test_proxies=proxies[i:i+BATCH_TEST_SIZE]
				tasks=[self.test_single_proxy(proxy)for proxy in test_proxies]
				loop.run_until_complete(asyncio.wait(tasks))#多任务等待每个完成用到asyncio.wait
				time.sleep(2)
		except Exception as e:
			print('测试器发生错误', e.args)
			


