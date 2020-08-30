import tesserocr#第三方图片识别库，识别能力比较基础
from PIL import Image
image=Image.open(r'C:\Users\Administrator\Desktop\车牌.jpg').convert('L')#导入图片并转化为灰度图像
#image=image.convert('1')#将图像进行二值化处理，同事还可以指定二值化的阈值（也就是把图像灰度之后，将图像变为0-255的黑海图，只要高于某个值，可以认定为有效的，低于的就可以抛弃））
threshold=80#0表示黑，255表示白高于80都定位白色
able = []
for i in range(256):#遍历到255选出以80位分割的数
	if i<threshold:
		able.append(0)

	else:
		able.append(1)

#图片二值化处理
ph=image.point(able,'1')#二值化处理，拿出高于80的点位变为黑色
result=tesserocr.image_to_text(ph)#识别会提高辨识度
print(result)

