import RPi.GPIO as GPIO
import pygame
from pygame.locals import *
import os
import sys
sys.path.append('C:/PiBox')
import time
import shutil

a=os.listdir('/home/pi/PiBox')
files=[]

try:
    b=os.listdir('/media/PIDRIVE')
    c=[]
    for x in b:
        
        if '.py' in x:
            if not x in a:
                shutil.move('/media/PIDRIVE/'+x,'/home/pi/PiBox/'+x)
                files.insert(0,x)
except OSError:
    print 'No External Drive'


for x in a:
    if '.py' in x:
        if '.pyc' in x or 'PiBox.py' in x:
            randomspacefiller=0
        else:
            files.insert(0,x)

GPIO.setmode(GPIO.BCM)

GPIO.setup(18, GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(17, GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(21, GPIO.IN,pull_up_down=GPIO.PUD_UP)

width=500
height=600

pygame.init()
d=pygame.display.set_mode((width,height))
background=pygame.Surface(d.get_size())
background=background.convert()
background.fill((80,80,80))
d.blit(background,(0,0))
pygame.display.flip()

selection=1
var=False
var2=False
var3=False
background.fill((0,250,0))
##Edit Image Name Here##
backer=pygame.image.load('/home/pi/PiBox/PiBoxBackground.jpg')
backer=pygame.transform.scale(backer,(width,height))
background.blit(backer,(0,0))
d.blit(background,(0,0))
pygame.display.flip()
xer=300

def draw_files():
    d.blit(backer,(0,0))
    for (i,x) in enumerate(files):
        if selection==i+1:
            font=pygame.font.Font(None,70)
            s=font.render(x,1,(0,230,0))
        else:
            font=pygame.font.Font(None,40)
            s=font.render(x,1,(220,0,0))
        spos=s.get_rect()
        spos.centerx=width/2
        if selection==i+1:
            spos.centery=xer
        elif selection<i+1:
            spos.centery=xer+((i-selection+1)*60)
        elif selection>i+1:
            spos.centery=xer-((selection-(i+1))*60)
        if selection==i+1:
            pygame.draw.rect(d,(220,0,0),spos)
        else:
            pygame.draw.rect(d,(0,0,0),spos)
        d.blit(s,spos)
    pygame.display.flip()

while True:
    l=GPIO.input(17)
    r=GPIO.input(18)
    f=GPIO.input(21)
    font=pygame.font.Font(None,40)
    draw_files()
    if l==False and var==True:
        var=False
        selection=selection-1
        d.blit(background,(0,0))
    if r==False and var2==True:
        var2=False
        selection=selection+1
        d.blit(background,(0,0))
    if selection<1:
        selection=len(files)
        xer=height/2
    if selection>len(files):
        selection=1
        xer=height/2
    if f==False and var3==True:
        var3=False
        gameit=files[selection-1]
        run=__import__(gameit)
    if var==False and l!=False:
        var=True
    if var2==False and r!=False:
        var2=True
    if var3==False and f!=False:
        var3=True


