MAX_SCORE = 100
MIN_SCORE = 0
INITIAL_SCORE = 10
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_PASSWORD = None
REDIS_KEY = 'proxies'
import redis
from random import choice
#使用redis有序集合，和集合区别就是有序集合会多一个分数，可以实现排序，成员唯一，分数可以一样
class redisclient(object):
	def __init__(self,host=REDIS_HOST,port=REDIS_PORT,password=REDIS_PASSWORD):#链接数据库
		self.db=redis.StrictRedis(host=host, port=port, password=password, decode_responses=True)#一般来说官方推荐使用redis.StrictRdis,而redis.Redis操作有些不同主要兼容旧版本

	def add(self,proxy,score=INITIAL_SCORE):#初始的proxy初始分设置为10，后面会检测如果可用直接设置成一百
		if not self.db.zscore(REDIS_KEY,proxy):#如果redis中不存在proxy的分数，那么将之添加
			return self.db.zadd(REDIS_KEY,{proxy:MAX_SCORE})

	def random(self):#随机获取有效代理，首先尝试获取最高分数代理，如果不存在，按照排名获取，否则异常
		result=self.db.zrangebyscore(REDIS_KEY, MAX_SCORE, MAX_SCORE)
		if len(result):
			return choice(result)
		else:
			result=self.db.zrevrange(REDIS_KEY, 0, 100)
			if len(result):
				return choice(result)
			raise POOLEMPTYerror

	def decrease(self,proxy):#设置减分，代理值减一分，小于最小值则删除
		score = self.db.zscore(REDIS_KEY, proxy)

		if score and score>MIN_SCORE:
			print('代理', proxy, '当前分数', score, '减1')
			return self.db.zincrby(REDIS_KEY,-1,proxy)#第三个传入的就是分数，-1表示减1

		else:
			print('代理',proxy)
			return self.db.zrem(REDIS_KEY, proxy)

	def exists(self,proxy):#判断是否存在
		return not self.db.zscore(REDIS_KEY, proxy) == None

	def max(self,proxy):
		print('代理', proxy, '可用，设置为', MAX_SCORE)

		mapping={proxy:MAX_SCORE}
		
		return self.db.zadd(REDIS_KEY, mapping)#

	def count(self):
		return self.db.zcard(REDIS_KEY)#获取数量

	def all(self):
		return self.db.zrangebyscore(REDIS_KEY, MIN_SCORE, MAX_SCORE)#获取全部代理









