#Python:静音视频转字符
#任意字符任意静音视频均可
#如果效果不理想 多半是视频分辨率过小 分辨率越大效果越好 但程序运行也会越慢 用视频转换工具转换分辨率即可 推荐狸窝

#需要安装Module cv2
#安装方法: Win+R>打开>cmd>输入 pip install opencv-python
#出现successfully字样即安装成功

from cv2 import *

character_list=list('*¿$#')#字符列表 可任意更改 但注意不要把不同类别的字符组合(即字母,汉字,数字等组合) 因为字符宽度不同
video=VideoCapture('video.mp4')#视频初始化
active,frame=video.read()#read()返回每一帧的布尔值(True/False)和三维数组
txt_list=[]#初始化输出列表
n=0#视频越长程序处理时间越长,判断程序是否在正常运行

while active:#循环读取视频帧  
    txt=''#文本初始化
    gray_frame=cvtColor(frame,COLOR_BGR2GRAY)#COLOR_BGR2GRAY是cvtColor()的一个参数 详细请百度python cvtColor()
    #把每一帧转换成灰度图 灰度图没有色彩 RGB色彩分量全部相等 例如:灰度为100就表示RGB(100,100,100)
    frame_video=resize(gray_frame,(100,25))#resize灰度图 (100,25)数值适应控制台大小 video是该视频的三维数组

    for gray_pixel_line in frame_video:#对于视频中的每行像素 根据灰度值对应字符
        for gray_pixel in gray_pixel_line:#对于每一行中的每个像素 
            txt+=character_list[int(gray_pixel/(256/len(character_list)))]
            #256表示灰阶(0~256) 浮点算法：∵Gray=0.3*R+0.6*G+0.1*B ∴(0.3+0.6+0.1)=1
        txt+="\n"
        n+=1

    txt_list.append(txt)
    print(n)

    active,frame=video.read()#视频处理完后结束循环

for frame in txt_list: 
    waitKey(25)#控制播放速度
    print(frame)#打印每一帧

#源码在主页公告地址中的chartacter_video文件夹
#By Tonymot