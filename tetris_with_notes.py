#俄罗斯方块 Tetris
#程序精简巧妙 详细讲解

#其实俄罗斯方块的判断没有想象中的那么难 不需要长篇幅的代码编写
#方块
#旋转
#移动
#物块
#形状
#碰撞检测
#绘制
#就这7个类

#引入必要模块:
import pygame,sys,random,time

#物块的形状是一个二维数组 通俗的讲 就是列表集
#[x,y]定义:[一个列表的第一个值表示行row,第二个值表示列column]
#一个物块的形状由四个方块组成 四个方块对应四个位置
#每个位置(x,y)用一个列表表示 四个位置组成一个物块形状的列表
#7个列表对应7种形状,7种形状组成一个总列表 形状的初始定义位置为0行,0列
#左下角为原点,向上为y正,向右为x正 与背景的原点不同!
#如: 形状Z:[[0,0],[0,-1],[-1,0],[-1,1]]
#Z的定义位置=[第0行第0列,第0行第-1列,第-1行第0列,第-1行第1列]
#如果空间想象能力较差 可以画图理解7种物块形状是如何规定的
#如果至此 仍不能理解二维数组 请百度python二维数组了解更多
#形式不唯一 这里只是7种形状的某一种初始坐标显示方式
all_block=[[[0,0],[0,-1],[0,1],[0,2]],  #物块形状为I
        [[0,0],[0,1],[1,1],[1,0]],    #物块形状为O
        [[0,0],[0,-1],[-1,0],[-1,1]],   #物块形状为Z
        [[0,0],[0,1],[-1,-1],[-1,0]],   #物块形状为S
        [[0,0],[0,1],[1,0],[0,-1]],     #物块形状为T
        [[0,0],[1,0],[-1,0],[1,-1]],    #物块形状为L
        [[0,0],[1,0],[-1,0],[1,1]]]     #物块形状为J

#对于背景: 背景也是一个二维数组 左上角为原点,向下为y正,向右为x正 与形状的原点不同!
#定义:0表示不绘制 1表示绘制 如: [0,0,0,0,0,..]则该行不绘制
#[0,1,0,1,0,...] 则该行第一列不绘制 第二列绘制 第三个列不绘制...
#设置游戏有22行10列 所以每行为[0*10] 即[0,0,0,0,0,0,0,0,0,0]
#游戏窗口显示第1~20行 不绘制 所以窗口每行每列为0
#窗口外的底部为第0行 要作为最初底部的碰撞检测 绘制 所以第0行每列为1
#窗口外的顶部为第21行 用来储存物块初始位置 不绘制 所以第21行每列为0
background=[[0 for column in range(0,10)]for row in range(0,22)]#创造列表集
background[0]=[1 for column in range(0,10)]#把第0层修改为[1*10]

#全局变量:
select_block=list(random.choice(all_block)) #从7个形状里随机挑选一个形状 
block_initial_position=[21,5]   #物块的初始行列位置[第21行,第5列]
times=0 #计时
score=[0]   #得分
gameover=[] #游戏结束
press=False #按键加快下落速度

#游戏设置
pygame.init()   #pygame初始化
screen=pygame.display.set_mode((250,500))   #250*500的窗口大小 如果更改数值 下叙代码也要做相应的更改

#游戏函数: 在while循环里重复调用
def block_move_down():
    y_drop=block_initial_position[0]    #即y_drop=21
    x_move=block_initial_position[1]    #即x_move=5
    y_drop-=1   #物块下落速度 相对于背景原点 y_drop-=1即y_drop=y_drop-1
    for row,column in select_block: #对于选择的物块的形状里的每一方块的行列位置:
        row+=y_drop    #对于当前选择的物块每一方块的行位置加上y_drop
                       #如select_block[0]的行为0+21,0+20,0+19...
        column+=x_move #对于当前选择的物块每一方块的列位置加上x_move
                       #select_block[0]的列为0+2(如果横向移动的距离=2),0+(-1)(如果横向移动的距离=-1)
        #print(background)#有了这行代码 应该更容易理解游戏显示原理
        if background[row][column]==1:  #二维数组检测 对于当前物块的行列
            break   #如果该物块的行列的二维数组值已经等于1就打断该for循环 直接进行下一个环节
    else:   #for循环剩下的工作:如果不满足for中的if条件 就刷新block_initial_position
        block_initial_position.clear()  #即block_initial_position=[]
        block_initial_position.extend([y_drop,x_move])  #即block_initial_position=[y_drop,x_move]
        return  #结束该函数的调用 直接进入下一个环节
    #如果新位置已经被占用 通过break结束上个for循环 再继续向下执行 如果新位置未被占用 通过return结束该函数

    y_drop,x_move=block_initial_position #在上一个环节中更改了block_initial_position 所以重新引入
    for row,column in select_block: #对于选择的物块的形状里的每一方块的行列位置:
        background[y_drop+row][x_move+column]=1
        #把物块所停留的的位置从0改成1 当位置变成1时 屏幕显示停靠的物块

    complete_row=[]   #完成的行
    for row in range(1,21): #1到20行 即窗口范围
        if 0 not in background[row]:    #判断第row行是否为方块全占满 如果占满 就增加到complete_row
            complete_row.append(row)    #增加的是row这行的数字 方便处理
    complete_row.sort(reverse=True) #把background中相应的行pop后 会引起complete_row索引变化
                                    #对其降序排列 倒着删除
    for row in complete_row:    #对于complete_row中的每一个
        background.pop(row)     #background删掉row行
        background.append(list(0 for column in range(0,10)))    #随删随补
    score[0]+=len(complete_row) #得分为完成的行的长度
    pygame.display.set_caption('Tetris,Score:'+str(score[0])+' Tonymot') #直接把得分打在窗口标题上

    select_block.clear()  
    select_block.extend(list(random.choice(all_block))) #至此一个物块的操作结束
    block_initial_position.clear()             #所以select_block,block_initial_position都要重新装填
    block_initial_position.extend([20,5])
    y_drop,x_move=block_initial_position   #在上面的环节中更改了block_initial_position 所以重新引入
    for row,column in select_block:
        if background[y_drop+row][x_move+column]:
            print(ground[row][column]) #如果background的每一行都有方块 就说明方块已经叠加到窗口顶部
            gameover.append(1)   #所以游戏在此结束 给gameover增加任意字节 在后面的gameover检测中用到
    #else:   #如果不满足for中的If条件 就说明方块还未叠加到窗口顶部
    #    return  #所以结束该函数 这两行代码可有可无

def new_draw():
    y_drop,x_move=block_initial_position    #即y_drop=21,x_move=5
    for row,column in select_block: #对于选择的物块的形状里的每一方块的行列位置:
        row+=y_drop     #对于当前选择的物块每一方块的行位置加上y_drop
        column+=x_move  #对于当前选择的物块每一方块的列位置加上x_move
        pygame.draw.rect(screen,(255,165,0),(column*25,500-row*25,23,23))#窗口动态方块绘制
        #(255,165,0)表示橙色 column*25,500-row*25表示一个方块的位置 23,23表示一个方块的长宽

    for row in range(0,20): #创建20行
        for column in range(0,10):  #创建10列
            bottom_block=background[row][column]
            #第row行第column列#500表示窗口的高 前两个表示绘制的位置 后两个表示长宽
            if bottom_block:#窗口底部的静态方块绘制
                pygame.draw.rect(screen,(0,0,255),(column*25,500-row*25,23,23))
                #(0,0,255)表示蓝色 column*25,500-row*25表示一个方块的位置 23,23表示一个方块的长宽

def move_left_right(n):
    #n=-1表示向左 n=1表示向右
    y_drop,x_move=block_initial_position #同上面 不赘述
    x_move+=n
    for row,column in select_block:
        row+=y_drop
        column+=x_move
        if column<0 or column>9 or background[row][column]: #前两个防止物块移出窗口
                                                            #后一个检测动态与静态的碰撞
            break
    else:   #更新位置
        block_initial_position.clear()
        block_initial_position.extend([y_drop,x_move])
def rotate():
    y_drop,x_move=block_initial_position
    rotating_position=[(-column,row)for row,column in select_block]
    #旋转90° 方块的每个坐标位置都要改变 如果空间想象能力较差 可以画图理解坐标位置的变换
    for row,column in rotating_position:
        row+=y_drop
        column+=x_move
        if column<0 or column>9 or background[row][column]: #检测原理和左右移动一样 不赘述
            break
    else:   #更新位置
        select_block.clear()
        select_block.extend(rotating_position)
while True:
    screen.fill((255,255,255))  #窗口背景为白色
    for event in pygame.event.get():    #处理游戏事件
        if event.type==pygame.QUIT: #点X退出
            sys.exit()
        elif event.type==pygame.KEYDOWN and event.key==pygame.K_LEFT:   #←键左移
            move_left_right(-1)
        elif event.type==pygame.KEYDOWN and event.key==pygame.K_RIGHT:  #→键右移
            move_left_right(1)
        elif event.type==pygame.KEYDOWN and event.key==pygame.K_UP: #↑键旋转
            rotate()
        elif event.type==pygame.KEYDOWN and event.key==pygame.K_DOWN:   #↓键加速下落
            press=True
        elif event.type==pygame.KEYUP and event.key==pygame.K_DOWN:
            press=False
    if press:   #按键时
        times+=10   #加快物块下落速度
    if times>=50:   #50为时间间隔
        block_move_down()   #物块下落
        times=0 #重置时间
    else:   #未按键时
        times+=1    #默认下落速度
    if gameover:    #如果gameover有了任意字节 游戏结束
        sys.exit()  #退出游戏
    new_draw()  #窗口整体重新绘制
    pygame.time.Clock().tick(200)   #控制游戏整体绘制速度
    pygame.display.flip()   #屏幕更新


#Python Pygame 俄罗斯方块(Tetris)
#运行需要安装pygame模块
#OK 完整代码教程到这里就结束了 演示视频可以参照AV55272839
#如何将代码一步一步的简化到85行 就不进行演示了
#把本文件的代码注释和不必要的空格和缩进去掉,不必要的重复代码删掉,冗长的代码简写
#剩下的代码就是AV55272839所示的85行 或者更少 如course.py所示 最新纪录已经简化到75行!
#本视频涉及到的代码,注释 仅用于学习 未经授权 禁止转载
#完整代码zip包在评论区
#如果还有任何不懂的地方 欢迎弹幕 评论 私聊
#如果觉得本视频对你的python学习有帮助 别忘了素质三连哦~
#By Tonymot
#演示Print