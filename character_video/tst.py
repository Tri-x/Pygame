from cv2 import *
video,txt_list=VideoCapture('video.mp4'),[]
active,frame=video.read()
while active:
    txt=''
    frame_video=resize(cvtColor(frame,COLOR_BGR2GRAY),(100,25))
    for line in frame_video:
        for x in line:
            txt+=list('*#$%')[int(x/(256/len(list('*#$%'))))]
        txt+='\n'
    txt_list.append(txt)
    active,frame=video.read()
for frame in txt_list:
    waitKey(25)
    print(frame)