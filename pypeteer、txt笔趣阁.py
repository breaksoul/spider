import asyncio
from pyppeteer import launch
import time,random
import os


width, height = 1366, 768
browser = None
async def main():
	global browser
	if browser is None:
		browser=await launch(executablePath='D:\\sublime\\chrome\\chrome.exe',headless=False,args=[f'--window-size={width},{height}'],autoclose=False)
	page=await browser.newPage()
	await page.setUserAgent(
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36')
	await page.setViewport({'width': width, 'height': height})
	await page.goto(url)
	await asyncio.sleep(3)
	await page.content()
	# Pyppeteer 三种解析方式
    # Page.querySelector()  # 选择器
    # Page.querySelectorAll()
    # Page.xpath()  # xpath  表达式
    # 简写方式为：
    # Page.J(), Page.JJ(), and Page.Jx()
            # 获取表格文本        
    # 获取文本：方法一，通过getProperty方法获取
    # title_str1 = await (await item.getProperty('textContent')).jsonValue()
    # 获取文本：方法二，通过evaluate方法获取
    # title_str2 = await page.evaluate('item => item.textContent', item)
    # 获取链接：通过getProperty方法获取
        # title_link = await (await item.getProperty('href')).jsonValue()


     #注意解析方法之后成了elementhandle,再通过获取文本等方法转化为str
	links=await page.querySelectorAll('#main > div:nth-child(2) > ul:nth-child(2) > li:nth-child(n+2) > a')#返回结果是一个domlist的集合,选择器中的选择直接选取的是从第二个到最后
	#print(links)
	#之后通过执行js获取内容
	for i in links:
		link=await (await i.getProperty('href')).jsonValue()
		name=await page.evaluate('i => i.textContent',i)
		print(name)
		name=name.strip()#去除首位空格
		print(link)
		page2=await browser.newPage()
		await page2.goto(link)
		l=await page2.querySelectorAll('#list > dl > dd:nth-child(n+1) > a')
		#文件不存在就创建
		if not os.path.exists(r'D:\新建文件夹\pythontext\data\%s'%name):#尝试了formate但是报错
			os.makedirs(r'D:\新建文件夹\pythontext\data\%s'%name)
		for n in l:
			
			mulu=await(await n.getProperty('href')).jsonValue()
			zhangjie=await (await n.getProperty('textContent')).jsonValue()
			page3=await browser.newPage()
			await page3.goto(mulu)
			#content=await page3.xpath(r'//*[@id="content"]//text()')#xpath清理出来的文件是elementhandle对象，xpath获取文本可以通过//text()获取所有子标签，也可以通过string（）获取所有文本并同通过无缝连续的方式拼接得到一起page3.xpath(string(r'//*[@id="content"]')
			content=await page3.querySelectorAll('#content')
			print(len(content))

			for i in content:
				content=await (await i.getProperty('textContent')).jsonValue()
				print(len(content))
				with open(r'D:\新建文件夹\pythontext\data\%s\%s.txt'%(name,zhangjie),'w',encoding='utf8')as f:
					f.write(content)#保存的时候必须为str,当前为'ElementHandle'
			print('保存',zhangjie)
	


if __name__ == '__main__':
	url='http://www.xbiquge.la/paihangbang/'
	#asyncio.get_event_loop().run_until_complete(main())
	asyncio.get_event_loop().run_until_complete(main())
	print('完成')

