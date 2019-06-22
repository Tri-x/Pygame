#Python:静态图片转字符
#任意字符任意静态图片均可
#若提示格式不支持 或者字符转换后效果不理想 用其他软件转换格式或图像大小即可 推荐Honeyview(蜂蜜图像浏览器)

#需要安装Module PIL 
#安装方法: Win+R>打开>cmd>输入 pip install pillow
#出现successfully字样即安装成功

from PIL import Image

character_list=list('NM$L')#字符列表 可任意更改 但注意不要把不同类别的字符组合(即字母,汉字,数字等组合) 因为字符宽度不同
color_character_unit=256/len(character_list)#规定颜色字符单位

#定义转换处理函数
def get_character(R,G,B):#RGB 颜色处理 
	gray_level=0.3*R+0.6*G+0.1*B#灰度浮点算法 通过灰度来区分颜色代表的字符 数值大小取舍略微影响最后的字符图像效果
	return character_list[int(gray_level/color_character_unit)]
	#不同的灰度对应着列表中不同的位置 不同的位置储存着不同的字符 颜色处理后返回列表中对应的一个字符

#图像和文本初始化
emperor=Image.open('nmsl_small.png')
txt=''

#对于图像中的每一个像素点
for height_pixel in range(0,200):
	for width_pixel in range(0,168):
		pixel_rgb=emperor.getpixel((width_pixel,height_pixel))
		#getpixel((x,y))得到的是该像素点的RGB值的元祖 例如(12,46,76)
		txt+=get_character(*pixel_rgb)#*表示解包 即去掉括号 例如12,46,76
	txt+='\n'#每一行字符打印完了换行

with open('nmsl_small.txt','w') as file:#文件写入
	file.write(txt)

#源码在主页公告地址中的chartacter_image文件夹
#By Tonymot