TESTER_CYCLE = 20
GETTER_CYCLE = 20
TESTER_ENABLED = False
GETTER_ENABLED = False
API_ENABLED = True

#x这个模块其实就是调用以上所定义的三个模块，将以上三个模块通过多进程的形式运行起来

from api import app
from getter import Getter
from jiance import Tester
from multiprocessing import Process
import time
#import threading

class Scheduler():
	def schedule_tester(self, cycle=TESTER_CYCLE):
		#定时测试代理
		tester = Tester()
		count=0
		while True:
			count+=1
			print('测试器开始运行',count)
			tester.run()

			time.sleep(cycle)


	def schedule_getter(self, cycle=GETTER_CYCLE):
		#定时获取代理
		getter = Getter()
		count=0
		while True:
			count+=1
			print('获取器开始运行',count)
			getter.run()
			
			time.sleep(cycle)

	def schedule_api(self):#20207/13 接口正常开启，正常提取ip
		#开启api接口
		app.run()#在默认端口运行

	def run(self):
		print('代理池开始运行')
		if TESTER_ENABLED:
			tester_process = Process(target=self.schedule_tester)
			tester_process.start()
			print('测试器进程开启')

		if GETTER_ENABLED:
			getter_process = Process(target=self.schedule_getter)
			getter_process.start()
			print('获取器进程开启')

		if API_ENABLED:
			api_process = Process(target=self.schedule_api)
			api_process.start()
			print('api接口开启')

if __name__ == '__main__':
    scheduler = Scheduler()
    scheduler.run()
# if __name__=='__main__':
#         Scheduler=Scheduler()
#         #Scheduler.run()
#         t=[]
#         t1 = threading.Thread(target=Scheduler.schedule_tester)
#         t.append(t1)
#         t2 = threading.Thread(target=Scheduler.schedule_getter)
#         t.append(t1)
#         t3 = threading.Thread(target=Scheduler.schedule_api)
#         t.append(t1)

#         for i in t:
#         	i.start()


#         for i in t:
#         	i.join()

#         print('主程序结束')