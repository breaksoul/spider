from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
from selenium.webdriver import ActionChains

driver=webdriver.Chrome(executable_path=r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')

name='10322bbb@qq.com'
password='wb1ddd789'
url='https://account.geetest.com/login'
driver.get(url)
driver.find_element_by_xpath(r'//*[@id="base"]/div[2]/div/div[2]/div[3]/div/form/div[1]/div/div/input').send_keys(name)
driver.find_element_by_xpath(r'//*[@id="base"]/div[2]/div/div[2]/div[3]/div/form/div[2]/div/div[1]/input').send_keys(password)
WebDriverWait(driver,15).until(EC.presence_of_element_located((By.CLASS_NAME,'geetest_radar_tip')))
driver.find_element_by_xpath(r'//*[@id="captchaIdLogin"]/div/div[2]/div[1]/div[3]').click()

#如果出现图片验证
#先找到图片位置，然后依次添加style="display: none; opacity: 1;"之后可以看出消失的分别是哪些图片可以查看到 那个是原图哪些是缺口图片
#而在这个网站中第三个canpas是隐藏的完整的图片所以只需要截图这个就好
#工作顺序：隐藏滑块
# 对canvas对象截图，获得缺口图片
# 隐藏缺口图片
# 显示完整图片
# 对canvas对象截图，获得完整图片
# 隐藏完整图片
# 显示缺口图片
# 显示滑块
#这里就需要用到javascript更改页面元素了


#js1="geetest_canvas_bg geetest_absolute"
#js2="document.getElementsByClassName('geetest_canvas_slice geetest_absolute').style.display: none; opacity: 1;"
js = "document.getElementsByClassName('geetest_canvas_fullbg geetest_fade geetest_absolute').style.display='block';"

driver.execute_script(js)


报错：执行不了了，验证码已经升级为点击，毫无办法，以下的代码就作为思路方法吧


button=WebDriverWait(driver,15).until(EC.element_to_be_clickable((By.CLASS_NAME,'geetest_slider_button'))

img=WebDriverWait(driver,15).until(EC.presence_of_element_located((By.CLASS_NAME,'.......'))#找到图片

location=img.location(img)#这一步主要是为了定位在浏览器中的位置，为后面的截图以及裁剪出图片做准备
size=img.size#size函数可以取矩阵点位，将图片按照长宽分布例如size[0]就位原点，所以图片额长宽就可以表示为
top,bottom,left,right=location(y),location(y)+size('height'),location(x),location(x)+size('width')#图片的位置就可以表示出来

screenshot=driver.get_screenshot()#截图
captcha=screenshot.crop()#截图之后按照上面定好的点位可以直接裁剪出完整的图片
#一般来说，需要截图出缺口和非缺口的图片，共两张
#假设已经截图好了两张图片
#接下来需要对图片的缺口进行比对

#oad（）方法主要返回一个用于读取和修改像素的像素访问对象。
#这个访问对象像一个二维队列，每个点位的像素都由三个值组成色彩即（r,g,b）类似于每个点位都是一个元祖
#开始比对两张图片的点位de RGB值，设定一个阈值，超过这个范围的就证明色彩明显不对那么就是缺口图片（元组索引访问对应点位的对应值，也就是r对r g对g）
threshold = 60
left=30#一般缺口在图片右边，所以设置个left
#开始遍历各个点位
for i in range(0,image1.size[0]):
	for j in range(image1.size[1]):
		pixel1=image1.load()[i,j]#将两张图片遍历像素点位
		pixel2=image2.load()[i,j]


		if not bs(pixel1[0] - pixel2[0]) < threshold and abs(pixel1[1] - pixel2[1]) < threshold and abs(pixel1[2] - pixel2[2]) < threshold:#这一步就可以判断出缺口的位置
				left=i#拿到了缺口位置的横坐标


#确定了缺口位置之后可以开始移动滑块
track=[]#记录了固定时间移动的距离
current=0#记录当前位移
distance#可以这顶不超过图片的长度即可
mid=distance*4/5#设定好需要做减速的区域
t=0.2
v=0#设置个初速度
#第一种，设定运动轨迹的方法，相对麻烦
while current<distant:#当前位置只要小于总距离
		if current<mid:
			a=2
		else:
			a=-3


		v0 = v
		v = v0 + a * t#计算速度
		#x = v0t + 1/2 * a * t^2 # 移动距离
		move = v0 * t + 1 / 2 * a * t * t
		current += move 
		track.append(move)#移动距离


#tracklist中已经哟了各个距离ActionChains模拟鼠标点击拖动
ActionChains(driver).click_and_hold(buttom).perform()
#在模拟拖动
for x in track:
		ActionChains(driver).move_by_offset(xoffset=x, yoffset=0).perform()
time.sleep(0.5)#模拟停顿
ActionChains(self.browser).release().perform()#松开鼠标

#因为网站改变，提供一个思路，为后面作参考








































