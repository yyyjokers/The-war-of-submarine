import pgzrun
import random

WIDTH=1250
HEIGHT=600
submarine=Actor('1.png')    #我方潜艇
ship=Actor('2.png')         #敌方战船
bullet=Actor('3.png')       #我方鱼雷
mine=Actor('4.png')         #水雷
bomb=Actor('5.png')         #炸弹
enemy=Actor('6.png')        #敌方潜艇
bang=Actor('7.png')         #爆炸效果
e_bullet=Actor('31.png')    #敌方鱼雷
background1=Actor('1234.png')
background2=Actor('4321.png')
x_s=0	                    #我方潜艇的初始位置x
y_s=HEIGHT//2	            #我方潜艇的初始位置y
D_x=10	                    #x轴变化
D_y=5	                    #y轴变化
H=230	                    #水面高度
L=578	                    #海底深度

ship_G=[]                   #敌方战船组
bullet_G=[]                 #我方鱼雷组
mine_G=[]                   #我方水雷组
bomb_G=[]                   #我方炸弹组
enemy_G=[]                  #敌方潜艇组
ebullet_G=[]                #敌方鱼雷组
ebomb_G=[]                  #敌方炸弹组
bang_G=[]                   #爆炸组
D=[]                        #删除组
d=[]                        #碰撞删除组
flag=0	                    #控制键盘帧
Flag=0	                    #控制敌方潜艇的出现频率
Live=0	                    #判断我方潜艇是否存活
F=0	                    #控制敌方的鱼雷频率
x_b=WIDTH//2	            #背景的初始位置x
y_b=HEIGHT//2	            #背景的初始位置y
point=0	                    #得分

def draw():
    global Live,x_b,point
    #设置背景移动
    background1.pos=(x_b,y_b)
    background1.draw()
    background2.pos=(x_b+background1.width,y_b)
    background2.draw()
    x_b=x_b-1
    if x_b+background1.width<=WIDTH//2:
        x_b=WIDTH//2
    screen.draw.text("POINT:"+str(point),[WIDTH-100,10],fontsize=30,color="blue")
    #判断潜艇存活和移动
    if Live==0:
        submarine.pos=(x_s,y_s)
        submarine.draw()
    else:
        bang.pos=(x_s,y_s)
        bang.draw()
        #已出屏幕外防止在进行干扰
        submarine.pos=(-300,-300)
        submarine.draw()
        screen.draw.text("GAME OVER",[WIDTH//2-270,HEIGHT//2],fontsize=120,color="black")
    #敌方战舰移动
    for i in range(len(ship_G)):
        ship_G[i][0].pos=ship_G[i][1]
        ship_G[i][1][0]=ship_G[i][1][0]-D_x//4
        ship_G[i][0].draw()
    #删除移动到屏幕外的战舰
    D=[]
    for i in range(len(ship_G)):
        if ship_G[i][1][0]+200<0:
            D.append(i)
    for i in range(len(ship_G)-1,-1,-1):
        if i in D:
            del ship_G[i]
    #判断敌方战舰和我方鱼雷的碰撞
    #并进行删除
    D=[]
    d=[]
    for i in range(len(ship_G)):
        for j in range(len(bullet_G)):
            if ship_G[i][0].colliderect(bullet_G[j][0])==True:
                point=point+1
                D.append(i)
                d.append(j)
                bang_G.append([Actor('7.png'),[ship_G[i][1][0],ship_G[i][1][1]],0])
                break
    for i in range(len(ship_G)-1,-1,-1):
        if i in D:
            del ship_G[i]
    for i in range(len(bullet_G)-1,-1,-1):
        if i in d:
            del bullet_G[i]
    #判断敌方战舰和我方水雷碰撞
    #并进行删除
    D=[]
    d=[]
    for i in range(len(ship_G)):
        for j in range(len(mine_G)):
            if ship_G[i][0].colliderect(mine_G[j][0])==True:
                point=point+1
                D.append(i)
                d.append(j)
                bang_G.append([Actor('7.png'),[ship_G[i][1][0],ship_G[i][1][1]],0])
                break
    for i in range(len(ship_G)-1,-1,-1):
        if i in D:
            del ship_G[i]
    for i in range(len(mine_G)-1,-1,-1):
        if i in d:
            del mine_G[i]
    #我方鱼雷移动
    for i in range(len(bullet_G)):
        bullet_G[i][0].pos=(bullet_G[i][1][0],bullet_G[i][1][1])
        bullet_G[i][1][0]=bullet_G[i][1][0]+D_x
        bullet_G[i][0].draw()
    #删除超出屏幕的鱼雷
    D=[]
    for i in range(len(bullet_G)):
        if bullet_G[i][1][0]>WIDTH:
            D.append(i)
    for i in range(len(bullet_G)-1,-1,-1):
        if i in D:
            del bullet_G[i]
    #我方水雷移动
    for i in range(len(mine_G)):
        mine_G[i][0].pos=(mine_G[i][1][0],mine_G[i][1][1])
        #print(flag)
        if mine_G[i][2]!=0 and flag==1:
            mine_G[i][1][1]=mine_G[i][1][1]+pow(-1,mine_G[i][2])*(D_y//2)
            mine_G[i][2]=mine_G[i][2]+1
            pass
        elif mine_G[i][1][1]>H:
            mine_G[i][1][1]=mine_G[i][1][1]-D_y
        mine_G[i][0].draw()
    #水雷的存在时间
    for i in range(len(mine_G)):
        if mine_G[i][1][1]<=H and mine_G[i][2]==0:
            mine_G[i][2]=1
    #删除存在时间较长的水雷
    D=[]
    for i in range(len(mine_G)):
        if mine_G[i][2]>=20:
            D.append(i)
    for i in range(len(mine_G)-1,-1,-1):
        if i in D:
            del mine_G[i]
    #我方炸弹移动
    for i in range(len(bomb_G)):
        bomb_G[i][0].pos=(bomb_G[i][1][0],bomb_G[i][1][1])
        if bomb_G[i][2]!=0:
            bomb_G[i][2]=bomb_G[i][2]+1
        elif bomb_G[i][1][1]<L:
            bomb_G[i][1][1]=bomb_G[i][1][1]+D_y
        bomb_G[i][0].draw()
    #炸弹的存在时间
    for i in range(len(bomb_G)):
        if bomb_G[i][1][1]>=L and bomb_G[i][2]==0:
            bomb_G[i][2]=1
    #删除存在时间较长的炸弹
    D=[]
    for i in range(len(bomb_G)):
        if bomb_G[i][2]>=10:
            D.append(i)
    for i in range(len(bomb_G)-1,-1,-1):
        if i in D:
            del bomb_G[i]
    #敌方潜艇移动
    for i in range(len(enemy_G)):
        enemy_G[i][0].pos=(enemy_G[i][1][0],enemy_G[i][1][1])
        enemy_G[i][1][0]=enemy_G[i][1][0]-D_x//4
        enemy_G[i][0].draw()
    #删除出屏幕的潜艇
    D=[]
    for i in range(len(enemy_G)):
        if enemy_G[i][1][0]+150<=0:
            D.append(i)
    for i in range(len(enemy_G)-1,-1,-1):
        if i in D:
            del enemy_G[i]
    #判断敌方潜艇和我方鱼雷的碰撞
    #并进行删除
    D=[]
    d=[]
    for i in range(len(enemy_G)):
        for j in range(len(bullet_G)):
            if enemy_G[i][0].colliderect(bullet_G[j][0])==True:
                point=point+1
                D.append(i)
                d.append(j)
                bang_G.append([Actor('7.png'),[enemy_G[i][1][0],enemy_G[i][1][1]],0])
                break
    for i in range(len(enemy_G)-1,-1,-1):
        if i in D:
            del enemy_G[i]
    for i in range(len(bullet_G)):
        if i in d:
            del bullet_G[i]
    #判断敌方潜艇和我方水雷的碰撞
    #并进行删除
    D=[]
    d=[]
    for i in range(len(enemy_G)):
        for j in range(len(mine_G)):
            if enemy_G[i][0].colliderect(mine_G[j][0])==True:
                point=point+1
                D.append(i)
                d.append(j)
                bang_G.append([Actor('7.png'),[enemy_G[i][1][0],enemy_G[i][1][1]],0])
                break
    for i in range(len(enemy_G)-1,-1,-1):
        if i in D:
            del enemy_G[i]
    for i in range(len(mine_G)-1,-1,-1):
        if i in d:
            del mine_G[i]
    #判断敌方潜艇和我方炸弹的碰撞
    #并进行删除
    D=[]
    d=[]
    for i in range(len(enemy_G)):
        for j in range(len(bomb_G)):
            if enemy_G[i][0].colliderect(bomb_G[j][0])==True:
                point=point+1
                D.append(i)
                d.append(j)
                bang_G.append([Actor('7.png'),[enemy_G[i][1][0],enemy_G[i][1][1]],0])
                break
    for i in range(len(enemy_G)-1,-1,-1):
        if i in D:
            del enemy_G[i]
    for i in range(len(bomb_G)-1,-1,-1):
        if i in d:
            del bomb_G[i]
    #爆炸
    for i in range(len(bang_G)):
        bang_G[i][0].pos=(bang_G[i][1][0],bang_G[i][1][1])
        bang_G[i][2]=bang_G[i][2]+1
        bang_G[i][0].draw()
    #爆炸效果存留5帧
    D=[]
    for i in range(len(bang_G)):
        if bang_G[i][2]==5:
            D.append(i)
    for i in range(len(bang_G)-1,-1,-1):
        if i in D:
            del bang_G[i]
    #敌方鱼雷移动
    for i in range(len(ebullet_G)):
        ebullet_G[i][0].pos=ebullet_G[i][1]
        ebullet_G[i][1][0]=ebullet_G[i][1][0]-D_x//2
        ebullet_G[i][0].draw()
    #删除屏幕外的敌方鱼雷
    D=[]
    for i in range(len(ebullet_G)):
        if ebullet_G[i][1][0]<=0:
            D.append(i)
    for i in range(len(ebullet_G)-1,-1,-1):
        if i in D:
            del ebullet_G[i]
    #敌方炸弹移动
    for i in range(len(ebomb_G)):
        ebomb_G[i][0].pos=ebomb_G[i][1]
        if ebomb_G[i][2]!=0:
            ebomb_G[i][2]=ebomb_G[i][2]+1
        elif ebomb_G[i][1][1]<=L:
            ebomb_G[i][1][1]=ebomb_G[i][1][1]+D_y//2
        ebomb_G[i][0].draw()
    #炸弹存在时间
    for i in range(len(ebomb_G)):
        if ebomb_G[i][1][1]>L and ebomb_G[i][2]==0:
            ebomb_G[i][2]=1
    #删除存在时间较长的炸弹
    D=[]
    for i in range(len(ebomb_G)):
        if ebomb_G[i][2]>=20:
            D.append(i)
    for i in range(len(ebomb_G)-1,-1,-1):
        if i in D:
            del ebomb_G[i]
    #判断我方潜艇是否和敌方潜艇相撞
    for i in range(len(enemy_G)):
        if enemy_G[i][0].colliderect(submarine)==True:
            Live=1
            #碰撞后敌方潜艇爆炸
            bang_G.append([Actor('7.png'),[enemy_G[i][1][0],enemy_G[i][1][1]],0])
            del enemy_G[i]
            break
    #判断我方潜艇是否和敌方鱼雷相撞
    for i in range(len(ebullet_G)):
        if ebullet_G[i][0].colliderect(submarine)==True:
            Live=1
            #碰撞后删除敌方鱼雷
            del ebullet_G[i]
            break
    #判断我方潜艇是否和敌方战舰碰撞
    for i in range(len(ship_G)):
        if ship_G[i][0].colliderect(submarine)==True:
            Live=1
            #碰撞后敌方战舰爆炸
            bang_G.append([Actor('7.png'),[ship_G[i][1][0],ship_G[i][1][1]],0])
            del ship_G[i]
            break
    #判断我方潜艇是否和敌方炸弹碰撞
    for i in range(len(ebomb_G)):
        if ebomb_G[i][0].colliderect(submarine)==True:
            Live=1
            del ebomb_G[i]
            break

#鼠标控制潜艇的移动
def on_mouse_move(pos):
    global x_s,y_s,H,Live
    if Live==0:
        x_s=pos[0]
        y_s=pos[1]
        if y_s<=H:
            y_s=H
        if y_s>=L:
            y_s=L
    #print(x_s,y_s)

#鼠标控制发射鱼雷
def on_mouse_down(pos):
    global bullet_G,Live
    if Live==0:
        x,y=pos
        if y<H:
            y=H
    #print(x,y)
        bullet_G.append([Actor('3.png'),[x+100,y+20],0])

#键盘空格控制释放炸弹和水雷
def SPACE_down(P):
    global mine_G,bomb_G
    x=P[0]
    y=P[1]
    mine_G.append([Actor('4.png'),[x,y],0])
    bomb_G.append([Actor('5.png'),[x,y],0])

#出现敌方潜艇
def enemy_append():
    global enemy_G
    y=random.randint(H,L)
    enemy_G.append([Actor('6.png'),[WIDTH+150,y],0])

#出现敌方战船
def ship_append():
    global ship_G
    ship_G.append([Actor('2.png'),[WIDTH+200,H],0])

#敌方潜艇发射鱼雷
def enemy_bullet_append():
    global ebullet_G,enemy_G
    for i in range(len(enemy_G)):
        ebullet_G.append([Actor('31.png'),[enemy_G[i][1][0]-100,enemy_G[i][1][1]+20],0])

#敌方战舰放置炸药
def ship_bomb_append():
    global ebomb_G
    for i in range(len(ship_G)):
        ebomb_G.append([Actor('5.png'),[ship_G[i][1][0],ship_G[i][1][1]],0])

def update():
    global x_s,y_s,H,flag,Flag,Live,F
    flag=flag%10
    Flag=Flag%100
    F=F%60
    if Flag==0:
        if random.randint(0,1)==0:
            enemy_append()
        else:
            ship_append()
    if keyboard[keys.SPACE] and flag==0 and Live==0:
        SPACE_down([x_s,y_s])
    if F==0:
        enemy_bullet_append()
        ship_bomb_append()
    flag=flag+1
    Flag=Flag+1
    F=F+1

pgzrun.go()
