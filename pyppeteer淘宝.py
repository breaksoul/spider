import asyncio
from pyppeteer import launch
import time, random

width, height = 1366, 768

browser = None#设置一个浏览器变量为了在多任务时只创建一个浏览器
async def main():
	global browser
	if browser is None:#为了在多任务时只创建一个浏览器
		browser=await launch(executablePath='D:\\sublime\\chrome\\chrome.exe',headless=False,args=[f'--window-size={width},{height}'],autoClose=False)#设置浏览器的大小,'headless': False如果想要浏览器隐藏更改False为True，executablePath=''可以修改浏览器路径
	page=await browser.newPage()
	#设置useragent
	await page.setUserAgent(
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36')
	await page.setViewport({'width': width, 'height': height})#设置浏览器大小
	await page.goto('https://login.taobao.com/member/login.jhtml?')
	#通过设置webdriver、检测为false绕过
	await page.evaluate('''() =>{ Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) }''')
	await asyncio.sleep(3)
	await page.type('#fm-login-id',username,{'delay':input_time_random() - 50})#防止tb输入数据速度检测
	await asyncio.sleep(2)
	await page.type('#fm-login-password',pwd,{'delay':input_time_random() - 50})
	await page.keyboard.press('Enter')
	# pages = await browser.pages()#当点击后，pypeteer的页面内容还是停留在原页面，可以通过这种方式获取新的页面内容
	# page = pages[-1]
def input_time_random():#定义一个随机数
	return random.randint(100, 151)
if __name__ == '__main__':
	username='15121001990'
	pwd='123456'
	asyncio.get_event_loop().run_until_complete(main())
# 今日头条点击后新开一个页面, 通过打印url可以看出page还停留在原页面
    # # 以下用于切换至新页面
    # pages = await browser.pages()
    # page = pages[-1]
    # print(page.url)