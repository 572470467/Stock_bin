#coding = utf-8 
import time
from tkinter import*
import threading
import json
import os
import sys
import socket
import csv ,sys,operator
import tkinter.filedialog
import pygame
import pandas as pd
from pygame.locals import *
import urllib.request
from pygame.color import THECOLORS
pygame.init()
os.environ['SDL_VIDEO_WINDOW_POS']= "%d,%d" % (67,27)
Brack=[0,0,0]
White=[255,255,255]
Red=[255,0,0]
Green=[0,255,0]
Gray=[169,169,169]
width=1360
height=768
size=(width-67)/3
default_dir = r"C:\Users\lenovo\Desktop" # 设置默认打开目录
name=[" 选择配方","  开    始"]
number_a=["A0","A1","A2","A3"]
icon={'11':'kz.jpg','01':'bz.jpg','00':'mz.jpg','10':'gz.jpg'}
csd_icon={'0':'csd0.jpg','1':'csd1.jpg'}
zd_icon={'0':'zd0.jpg','1':'zd1.jpg'}
qg_icon={'0':'qg0.jpg','1':'qg1.jpg'}
xzt_icon={'0':'xzt0.jpg','1':'xzt1.jpg'}
screen = pygame.display.set_mode((int(size),height))
text=pygame.font.Font("fonts/wqy-zenhei.ttc",24)
text0=pygame.font.Font("fonts/wqy-zenhei.ttc",18)
screen.fill(Brack)
def stock_bin(num,x,y,a):#料仓图标
    text_fmt0=text.render(number_a[num],3,White)
    screen.blit(text_fmt0,(x-30,y+15))
    img=pygame.image.load(icon[a])
    img=pygame.transform.smoothscale(img,(60,60))
    screen.blit(img,(x,y)) 
    pygame.display.update()
def transmit(x,y,a):#传输带图标
    img=pygame.image.load(csd_icon['{}'.format(a)])
    img=pygame.transform.smoothscale(img,(60,60))
    screen.blit(img,(x,y))
    pygame.display.update()
def distributor(x,y,a):#振动给料器图标
    img=pygame.image.load(zd_icon['{}'.format(a)])
    img=pygame.transform.smoothscale(img,(60,60))
    screen.blit(img,(x,y))
    pygame.display.update()
def weight(x,y,m):#称重图标
    img=pygame.image.load('cz.jpg')
    img=pygame.transform.smoothscale(img,(60,60))
    screen.blit(img,(x,y))
    text_fmt0=text0.render('{}'.format(m),3,White)
    screen.blit(text_fmt0,(x+22,y+70))
    pygame.display.update()
def slip(x,y,a):#气缸图标
    img=pygame.image.load(qg_icon['{}'.format(a)])
    img=pygame.transform.smoothscale(img,(70,70))
    screen.blit(img,(x,y))
    pygame.display.update()
def turn_table(x,y,a):#旋转台图标
    img=pygame.image.load(xzt_icon['{}'.format(a)])
    img=pygame.transform.smoothscale(img,(100,100))
    screen.blit(img,(x,y))
    pygame.display.update()
def AN(x,y,a):#按钮
    pygame.draw.rect(screen,Green,[x,y,82,35],0)
    text_fmt0=text0.render(a,3,Brack)
    screen.blit(text_fmt0,(x+2,y+4))
    pygame.display.update()
def PF():#选择配方并另存为recipe.csv
    root=tkinter.Tk()
    root.withdraw()
    fname= tkinter.filedialog.askopenfilename(title=u"Select formula",initialdir=(os.path.expanduser(default_dir)))
    g=open(fname)
    next(g)
    f=open('recipe.csv','w')
    for line in g:
        f.write(line)
    g.close()
    f.close()
if __name__ == '__main__':
    while True:
        time.sleep(1/3)
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    exit()
            elif event.type == QUIT:
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pressed_array = pygame.mouse.get_pressed()
                pos = pygame.mouse.get_pos()
                for index in range(len(pressed_array)):
                    if pressed_array[index]:
                        if 75<=pos[0]<=167 and 670<=pos[1]<=705:
                            PF()
                        elif (size/2)+75<=pos[0]<=(size/2)+167 and 670<=pos[1]<=705:
                            f=open('recipe.csv','r')
                            reader=csv.reader(f)
                            lt=[]
                            for a in reader:
                                lt.append(a)
                            for t in lt:
                                #response=urllib.request.urlopen('http://localhost:5000/measure/{0}/{1}'.format(t[0],round(float(t[1])-float(t[2]),2)))
                                print('http://localhost:5000/measure/{0}/{1}'.format(t[0],round(float(t[1])-float(t[2]),2)))
        response0=urllib.request.urlopen("http://localhost:5000/level")
        html=response0.read().decode()
        a=(html[2:-3].split('],['))[0].split(',')
        b=(html[2:-3].split('],['))[1].split(',')
        response1=urllib.request.urlopen("http://localhost:5000/scale/a")
        html1=response1.read()
        text1=json.loads(html1)
        response2=urllib.request.urlopen("http://localhost:5000/scale/b")
        html2=response2.read()
        text2=json.loads(html2)
        response3=urllib.request.urlopen("http://localhost:5000/scale/c")
        html3=response3.read()
        text3=json.loads(html3)
        response4=urllib.request.urlopen("http://localhost:5000/scale/d")
        html4=response4.read()
        text4=json.loads(html4)
        response5=urllib.request.urlopen("http://localhost:5000/icon")
        html5=response5.read()
        text5=json.loads(html5)
        Weight=[text1,text2,text3,text4]
        for i in range(4):
            stock_bin(i,(size/4)*i+30,40,a[i]+b[i])
            transmit((size/4)*i+30,130,text5['CSD'][i])
            distributor((size/4)*i+30,230,text5['ZD'][i])
            weight((size/4)*i+30,350,Weight[i]['reading'])
        for v in range(2):
            slip((size/2)*v+75,470,text5['QG'][v])
            turn_table((size/2)*v+75,550,text5['XZT'][v])
            AN((size/2)*v+75,670,name[v])
