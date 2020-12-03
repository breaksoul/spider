import asyncio
import time
#隐藏浏览器特征，主要是去除浏览器自动化参数，以及去除window.navigator.webdr检测
#必须在导入pyppeteer之前就去除(你自己的Python安装路径)\Python37_64\Lib\site-packages\pyppeteer\launcher.py注释掉  --enable-automation 参数
from lxml import etree
import time,random
from pyppeteer.launcher import launch
from pyquery import PyQuery as pq

#from retrying import retry #设置重试次数用的


async def main(username,pwd,url):

	start_parm = {
        # 启动chrome的路径
        "executablePath": r"D:\Downloads\chrome\chrome-win\chrome.exe",
        # 关闭无头浏览器
        "headless": True,

        "args": [
            '--disable-infobars',  # 关闭自动化提示框
            # '--window-size=1920,1080',  # 窗口大小
            '--log-level=30',  # 日志保存等级， 建议设置越好越好，要不然生成的日志占用的空间会很大 30为warning级别
            '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',  # UA
            #'--no-sandbox',  # 关闭沙盒模式
            '--start-maximized',  # 窗口最大化模式
            '--proxy-server=http://118.113.247.65:9999'  # 代理
            r'userDataDir=C:\Users\Administrator\Desktop\python\python example\python3\data saved'  # 用户文件地址有效解决Unable to remove Temporary User Data
        ],
    }
	browser=await launch({'headless': False, **start_parm, })
	page=await browser.newPage()#启动新的浏览器页面
	await page.setUserAgent( 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36')
	await page.goto(url)#访问登录页面
	#pyppeteer很强大的地方在于page.evaluate(pageFunction, ...args可以向页面注入我们的函数
	# navigator是windiw对象的一个属性，同时修改plugins，languages，navigator 且让
    #个网站，检测都不一样，这是比较通用的。
	await page.evaluate('''() =>{ Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) }''') #以下为插入中间js，将淘宝会为了检测浏览器而调用的js修改其结果。
	await page.evaluate('''() =>{ window.navigator.chrome = { runtime: {},  }; }''')
	await page.evaluate('''() =>{ Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] }); }''')
	await page.evaluate('''() =>{ Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5,6], }); }''')


	#输入账号密码
	await page.type('#fm-login-id', username, {'delay': input_time_random() - 30})
	await page.type('#fm-login-password', pwd, {'delay': input_time_random()})
	await page.keyboard.press('Enter')
	await asyncio.sleep(3)
	#await page.screenshot(path=r'C:\Users\Administrator\Desktop\python\python example\python3\data saved\example.jpg')#截图存放路径
	#print('截图存放完成')

	# js="documnet.getElementById('q').value=''"#将默认的搜索框内容改为空，tb数据更改失败，尝试用鼠标控制清除默认数据
	# await page.evaluate(js)
	await page.hover('#q')
	await asyncio.sleep(1)
	await page.mouse.down()
	await page.mouse.up()

	await page.keyboard.press('Backspace')#笨办法，但确实是可以的
	await page.keyboard.press('Backspace')
	await page.keyboard.press('Backspace')
	await page.keyboard.press('Backspace')
	await page.keyboard.press('Backspace')
	await page.keyboard.press('Backspace')

	await asyncio.sleep(1)
	await page.type('#q','pingguo',{'delay': input_time_random()-30})#有个bug在于如何清除搜索框内的原本内容
	await page.keyboard.press('Enter')
	await asyncio.sleep(3)
	#pypeteer的页面依然停留在原来的页面，可以通过以下访问新的页面
	 #pages = await browser.pages()
	 #page = pages[-1]
	await page.content()
	#link=await page.xpath(r"//*[@id='mainsrp-itemlist']/div/div/div[1]//div/div[2]/div[2]/a/@href")
							# //*[@id="mainsrp-itemlist"]/div/div/div[1]/div[1]/div[2]/div[2]/
	      #                   //*[@id="mainsrp-itemlist"]/div/div/div[1]/div[3]/div[2]/div[2]
	      #                   //*[@id="mainsrp-itemlist"]/div/div/div[1]/div[4]/div[2]/div[2]
	      #                   //*[@id="mainsrp-itemlist"]/div/div/div[1]/div[5]/div[2]/div[2]
	      					#//*[@id="mainsrp-itemlist"]/div/div/div[1]/div[2]/div[2]/div[2]
	      					#//*[@id="mainsrp-itemlist"]/div/div/div[1]/div[2]/div[2]/div[2]

	link=await page.querySelectorAll("#mainsrp-itemlist > div > div > div:nth-child(1) > div > div.ctx-box.J_MouseEneterLeave.J_IconMoreNew > div.row.row-2.title > a.J_ClickStat")
	#这个选择只能选出一个还得更改


	

	#link=await page.querySelectorAll(".J_ItemPic.img")#除此之外还可以用page.xpath()清洗
	print(len(link))

	count=0

	# Pyppeteer 三种解析方式
    # Page.querySelector()  # 选择器
    # Page.querySelectorAll()
    # Page.xpath()  # xpath  表达式
    # # 简写方式为：
    # Page.J(), Page.JJ(), and Page.Jx()
	item_list = []
	for i in link:
		i=await (await i.getProperty("href")).jsonValue()
		print(i)
		await page.waitForNavigation()#，导航超时#为了解决报错问题Protocol error (Runtime.evaluate): Cannot find context with specified id

		#i=await i.attrs('href')
		#t=await i.click()#z这个位置有问题，并没有点进去，导致后面的内容还是搜索主页的内容
		await page.goto(i)#访问详情页面
		#a=await page.content()
		#print('分割线------------------------------------------------------------------------------------',a)
		# 打印当前页标题
		# print(await page.title())

		# # 获取所有的文本信息, 执行js代码
  #   	content = await page.querySelectorAll('(element) => element.textContent', element)
  #   	print(content)
    # for item in elements:
    #     print(await item.getProperty("textContent"))
    #     # 获取文本信息
    #     title = await (await item.getProperty("textContent")).jsonValue()
    #     # 获取连接
    #     link = await (await item.getProperty("href")).jsonValue()
    #     print(title)   
    #     print(link)



    	#清洗出 详情页标签
		a1=await page.xpath(r'//*[@id="J_DetailMeta"]/div[1]/div[1]/div/div[1]/h1/a')#清洗出a标签，这一步的标签为空

		#ab=await page.xpath(r'//*[@id="J_DetailMeta"]/div[1]/div[1]/div/div[1]/h1/a/text')
		#print('a标签爬取的内容结果：',a)
		#name1=await (await a[-1].getProperty("textContent")).jsonValue()#直接抓取content内容

		a = await (await a1[-1].getProperty("textContent")).jsonValue()
		item={'商品名称':a}
		item_list.append(item)

		await asyncio.sleep(1)
		



		


	print('通过getProperty爬取的内容结果：',item_list)

	await browser.close()#可以等待浏览器关闭，答道手动关闭的目的


# def content(page):
# 	link=page.querySelectorAll("div.row.row-2.title")#querySelector只选择一个，querySelectorAll则选择所有符合条件的，返回一个nodelist
# 	print(len(link))
# 	# for i in link:
# 	# 	i.click()





	time.sleep(10)








	#page.waitForNavigation({'timeout':50000})
	#content=await page.querySelector("#J_SiteNavLogin > div.site-nav-menu-hd > div.site-nav-user > a text()")#获取登录到的各人信息
##J_SiteNavLogin > div.site-nav-menu-hd > div.site-nav-user > a text
# 	if content=='tb1001990_33':
# 		print("登录成功")
# 	else:
# 		time.sleep(2)
# 		 #看看是否有滑块
# 		slider=await page.querySelector("#nc_lang_cnt")#获取元素document.querySelector("#nc_1_n1z")

# 		if slider:
# 			print("页面出现滑块")
# 			#flag,page=await mouse_slide(page=page)

# 			await asyncio.sleep(2)
# 			try:
# 			#鼠标移动到滑块，按下，滑动到头（然后延时处理），松开按键
# 				await page.hover("#nc_1_n1z")#找到滑块.hover选择器，将指针浮在元素上

# 				await page.mouse.down()
# 				await page.mouse.move(2000, 0, {'delay': random.randint(1000, 2000)})
# 				await page.mouse.up()
# 			except Exception as e:
# 				print(e, ':验证失败')
# 				#return None,page



# 			# if flag:
# 			# 	await page.keyboard.press('Enter')
# 			# 	print("print enter",flag)
# 			# 	await page.evaluate('''document.getElementById("J_SubmitStatic").click()''') # 如果无法通过回车键完成点击，就调用js模拟点击登录按钮。
# 			# 	await get_cookie(page)


# 		else:
# 			await page.keyboard.press('Enter')#没有的haul就直接点击回车，直接模拟了点击键盘
# 			print("点击了回车")
# 			await page.evaluate('''document.getElementById("J_SubmitStatic").click()''')#同理直接模拟js知找到登录按钮，点击



#    # 获取登录后cookie
def input_time_random():
	return random.randint(100,151)
	#清洗出路径












# async def ge_cookie(page):
# 	res = await page.content()
# 	cookies_list = await page.cookies()
# 	cookies = ''#用的是js语法
# 	for cookie in cookies_list:
# 		str_cookie = '{0}={1};'
# 		str_cookie = str_cookie.format(cookie.get('name'), cookie.get('value'))#格式化一下
# 		cookies += str_cookie#放入字符串中
# 	print(cookies)
# 	return cookies



if __name__ == '__main__':
	username='15121001990'
	pwd = 'wb962422' #密码
	url='https://login.taobao.com/member/login.jhtml?redirectURL=http%3A%2F%2Fs.taobao.com%2Fsearch%3Fq%3Diphone%26imgfile%3D%26commend%3Dall%26ssid%3Ds5-e%26search_type%3Ditem%26sourceId%3Dtb.index%26spm%3Da21bo.2017.201856-taobao-item.1%26ie%3Dutf8%26initiative_id%3Dtbindexz_20170306&uuid=9b631e2152cdd7be53cdd829a9c84a3e'
	loop = asyncio.get_event_loop()  #协程，开启个无限循环的程序流程，把一些函数注册到事件循环上。当满足事件发生的时候，调用相应的协程函数。

	loop.run_until_complete(main(username, pwd, url))  #将协程注册到事件循环，并启动事件循环




