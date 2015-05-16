##Requires PiBox 3 button controller connected to terminals 17, 18, and 21
import RPi.GPIO as GPIO
import time
import pygame
from pygame.locals import *
import random

width=1200
height=600
global difficulty
difficulty='MEDIUM'
global diff
diff=5
global shipcolor
shipcolor=(220,0,0)
global easyscores
global medscores
global hardscores
try:
    f=open('scores.txt')
    s=f.read()
    f.close()
    easyscores=s.split(',')
    easyscores.pop()
except IOError:
    easyscores=[0,0,0,0,0]
try:
    f=open('scores2.txt')
    s=f.read()
    f.close()
    medscores=s.split(',')
    medscores.pop()
except IOError:
    medscores=[0,0,0,0,0]
try:
    f=open('scores3.txt')
    s=f.read()
    f.close()
    hardscores=s.split(',')
    hardscores.pop()
except IOError:
    hardscores=[0,0,0,0,0]
    

GPIO.setmode(GPIO.BCM)

GPIO.setup(18, GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(17, GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(21, GPIO.IN,pull_up_down=GPIO.PUD_UP)

pygame.init()
screen=pygame.display.set_mode((width, height))
background=pygame.Surface(screen.get_size())
background=background.convert()
background.fill((0,75,150))
screen.blit(background, (0,0))
pygame.display.flip()

def main_menu():
    font=pygame.font.Font(None,55)
    selection=1
    texcol=(210,0,0)
    var=True
    var2=True
    var3=True
    background.fill((0,0,0))
    screen.blit(background, (0,0))
    display_scores()
    while True:
        r=GPIO.input(18)
        l=GPIO.input(17)
        f=GPIO.input(21)
        tp=font.render('PLAY',1,(0,200,0))
        ts=font.render('SETTINGS',1,(0,200,0))
        th=font.render('HELP',1,(0,200,0))
        tq=font.render('QUIT',1,(0,200,0))
        tppos=tp.get_rect()
        tppos.centerx=(width)/5
        tppos.centery=(background.get_rect().centery)-150
        tspos=ts.get_rect()
        tspos.centerx=width*2/5
        tspos.centery=background.get_rect().centery-150
        thpos=th.get_rect()
        thpos.centerx=(width)*3/5
        thpos.centery=(background.get_rect().centery)-150
        tqpos=tq.get_rect()
        tqpos.centerx=(width)*4/5
        tqpos.centery=(background.get_rect().centery)-150
        if selection==1:
            pygame.draw.rect(screen,texcol,(tppos))
            pygame.draw.rect(screen,(0,0,0),(tspos))
            pygame.draw.rect(screen,(0,0,0),(tqpos))
        elif selection==2:
            pygame.draw.rect(screen,texcol,(tspos))
            pygame.draw.rect(screen,(0,0,0),(tppos))
            pygame.draw.rect(screen,(0,0,0),(thpos))
        elif selection==3:
            pygame.draw.rect(screen,texcol,(thpos))
            pygame.draw.rect(screen,(0,0,0),(tspos))
            pygame.draw.rect(screen,(0,0,0),(tqpos))
        elif selection==4:
            pygame.draw.rect(screen,texcol,(tqpos))
            pygame.draw.rect(screen,(0,0,0),(tppos))
            pygame.draw.rect(screen,(0,0,0),(thpos))
        screen.blit(th,thpos)
        screen.blit(ts,tspos)
        screen.blit(tp,tppos)
        screen.blit(tq,tqpos)
        pygame.display.flip()
        if l==False and r != False and f != False and var==True:
            selection=selection-1
            var=False
        if l != False and r == False and f != False and var2==True:
            selection=selection+1
            var2=False
        if selection<1:
            selection=4
        elif selection>4:
            selection=1
        if l != False and r != False and f == False and var3==True:
            if selection==1:
                time.sleep(.5)
                Play()
                var=False
                var2=False
                var3=False
            if selection==2:
                Settings()
            if selection==3:
                background.fill((250,250,250))
                Help()
            elif selection==4:
                save()
                pygame.quit()
                quit()
            var3=False
        if l != False and var==False:
            var=True
        if r != False and var2==False:
            var2=True
        if f != False and var3==False:
            var3=True

def save():
    s=''
    for i in easyscores:
        s=s+str(i)+','
    f=open('scores.txt','w')
    f.write(s)
    f.close()
    s=''
    for i in medscores:
        s=s+str(i)+','
    f=open('scores2.txt','w')
    f.write(s)
    f.close()
    s=''
    for i in hardscores:
        s=s+str(i)+','
    f=open('scores3.txt','w')
    f.write(s)
    f.close()
    

def display_scores():
    ys=[height/2+40,height/2+80,height/2+120,height/2+160,height/2+200]
    font=pygame.font.Font(None,40)
    t=font.render('HIGH SCORES',1,(250,0,0))
    tp=t.get_rect()
    tp.centerx=background.get_rect().centerx
    tp.centery=height/2-50
    screen.blit(t,tp)
    t=font.render('EASY',1,(0,240,0))
    tp=t.get_rect()
    tp.centerx=width/4
    tp.centery=height/2
    screen.blit(t,tp)
    t=font.render('MEDIUM',1,(0,240,0))
    tp=t.get_rect()
    tp.centerx=width/2
    tp.centery=height/2
    screen.blit(t,tp)
    t=font.render('HARD',1,(0,240,0))
    tp=t.get_rect()
    tp.centerx=width*3/4
    tp.centery=height/2
    screen.blit(t,tp)
    pygame.display.flip()
    xer=0
    for i in easyscores:
        t=font.render(str(i),1,(150,150,250))
        tp=t.get_rect()
        tp.centerx=width/4
        tp.centery=ys[xer]
        screen.blit(t,tp)
        pygame.display.flip()
        xer=xer+1
    xer=0
    for i in medscores:
        t=font.render(str(i),1,(150,150,250))
        tp=t.get_rect()
        tp.centerx=width/2
        tp.centery=ys[xer]
        screen.blit(t,tp)
        pygame.display.flip()
        xer=xer+1
    xer=0
    for i in hardscores:
        t=font.render(str(i),1,(150,150,250))
        tp=t.get_rect()
        tp.centerx=width*3/4
        tp.centery=ys[xer]
        screen.blit(t,tp)
        pygame.display.flip()
        xer=xer+1
    

def Settings():
    global diff
    global difficulty
    global shipcolor
    font=pygame.font.Font(None,45)
    selection=1
    black=(0,0,0)
    red=(200,0,0)
    green=(0,210,0)
    var=False
    var2=False
    var3=False
    tc=font.render('COLOR',1,green)
    tcpos=tc.get_rect()
    tcpos.centerx=width/3
    tcpos.centery=200
    tsd=font.render('DIFFICULTY',1,green)
    tsdpos=tsd.get_rect()
    tsdpos.centerx=width/3
    tsdpos.centery=height/2
    tdif=font.render(str(difficulty),1,red)
    tdpos=tdif.get_rect()
    tdpos.centerx=width*2/3
    tdpos.centery=height/2
    ba=font.render('BACK',1,red)
    bapos=ba.get_rect()
    bapos.centerx=background.get_rect().centerx
    bapos.centery=height-60
    background.fill((0,0,0))
    screen.blit(background,(0,0))
    screen.blit(tsd,tsdpos)
    screen.blit(tdif,tdpos)
    screen.blit(ba,bapos)
    pygame.display.flip()
    while True:
        l=GPIO.input(17)
        r=GPIO.input(18)
        f=GPIO.input(21)
        background.fill((0,0,0))
        screen.blit(background, (0,0))
        tdif=font.render(difficulty,1,green)
        if selection==1:
            pygame.draw.rect(screen,red,tcpos)
        if selection==2:
            pygame.draw.rect(screen,red,tsdpos)
        if selection==3:
            pygame.draw.rect(screen,green,bapos)
        if f != False and var==False:
            var=True
        if l!=False and var2==False:
            var2=True
        if r!=False and var3==False:
            var3=True
        if l==False and var2==True:
            selection=selection-1
            var2=False 
        if r==False and var3==True:
            selection=selection+1
            var3=False
        if selection<1:
            selection=3
        if selection>3:
            selection=1
        if f==False and var==True:
            var=False
            if selection==1:
                if shipcolor==(220,0,0):
                    shipcolor=(0,220,0)
                elif shipcolor==(0,220,0):
                    shipcolor=(0,0,220)
                elif shipcolor==(0,0,220):
                    shipcolor=(250,250,250)
                elif shipcolor==(250,250,250):
                    shipcolor=(250,235,0)
                elif shipcolor==(250,235,0):
                    shipcolor=(220,0,220)
                elif shipcolor==(220,0,220):
                    shipcolor=(220,0,0)
            if selection==2:
                if diff==3:
                    diff=5
                    difficulty='MEDIUM'
                elif diff==5:
                    diff=7
                    difficulty='HARD'
                elif diff==7:
                    diff=3
                    difficulty='EASY'
            if selection==3:
                break
        screen.blit(tc,tcpos)
        pygame.draw.rect(screen,shipcolor,(width*2/3-40,180,80,40))
        screen.blit(tsd,tsdpos)
        screen.blit(tdif,tdpos)
        screen.blit(ba,bapos)
        pygame.display.flip()
    background.fill((0,0,0))
    screen.blit(background,(0,0))
    display_scores()
        

def Help():
    font=pygame.font.Font(None,40)
    line1=font.render('Press left and right buttons to move your character to either side',1,(120,120,120))
    onepos=line1.get_rect()
    onepos.centerx=background.get_rect().centerx
    onepos.centery=100
    line2=font.render('Press the middle button to fire at the green enemies',1,(120,120,120))
    twopos=line2.get_rect()
    twopos.centerx=background.get_rect().centerx
    twopos.centery=150
    line3=font.render('You can only shoot 5 bullets at a time',1,(120,120,120))
    threepos=line3.get_rect()
    threepos.centerx=background.get_rect().centerx
    threepos.centery=200
    line4=font.render('You can pause the game by pressing all three buttons at once',1,(120,120,120))
    fourpos=line4.get_rect()
    fourpos.centerx=background.get_rect().centerx
    fourpos.centery=250
    line5=font.render('press any button to return to the main menu',1,(250,0,0))
    fivepos=line5.get_rect()
    fivepos.centerx=background.get_rect().centerx
    fivepos.centery=400
    screen.blit(background,(0,0))
    screen.blit(line1,onepos)
    screen.blit(line2,twopos)
    screen.blit(line3,threepos)
    screen.blit(line4,fourpos)
    screen.blit(line5,fivepos)
    pygame.display.flip()
    time.sleep(1)
    while True:
        l=GPIO.input(17)
        r=GPIO.input(18)
        f=GPIO.input(21)
        if l==False or r==False or f==False:
            break
    background.fill((0,0,0))
    screen.blit(background,(0,0))
    display_scores()


def Play():
    global diff
    global difficulty
    global shipcolor
    count=0
    hits=0
    lives=10
    breakout=False
    var=True
    var2=True
    var3=True
    width=1200
    height=600
    bulletcolor=(200,100,100)
    enemycolor=(0,150,0)
    x=(width/2-40)
    y=(height*3/4)
    bulletx=[]
    bullety=[]
    enemyx=[-100,-50,-75,-90]
    enemyy=[200,150,50,300]
    poplistb=[]
    popliste=[]
    #initializes quit text
    font=pygame.font.Font(None,45)
    text=font.render('Are you sure you want to quit?',1,(250,250,250))
    text2=font.render('press LEFT for yes, RIGHT for no',1,(250,250,250))
    t3=font.render('Center to return to main menu',1,(250,250,250))
    tpos=text.get_rect()
    tpos.centerx=background.get_rect().centerx
    tpos.centery=background.get_rect().centery
    tpos.centery=tpos.centery-60
    t2pos=text2.get_rect()
    t2pos.centerx=background.get_rect().centerx
    t2pos.centery=background.get_rect().centery
    t3pos=t3.get_rect()
    t3pos.centerx=background.get_rect().centerx
    t3pos.centery=background.get_rect().centery
    t3pos.centery=t3pos.centery+60
    while True:
    # initializes the three button variables
        input_state = GPIO.input(18)
        input_state2= GPIO.input(17)
        input_state3= GPIO.input(21)
    # Tests for whether the buttons are pressed individually and runs accordingly
        if input_state==False:
            x=x+8
        if input_state2==False:
            x=x-8
        if input_state3==False and var3==True and len(bulletx)<5:
            bulletx.insert(0,x+35)
            bullety.insert(0,y)
            count=count+1
            var3=False
    # prevents you from going off the screen
        if x<0:
            x=0
        elif x>width-80:
            x=width-80

    # tests whether all three buttons are pressed at once and if so, quits        
        if input_state==False and input_state2==False and input_state3==False:
            pygame.draw.rect(screen,(0,0,0),(width/4,height/4+40,width/2,height/2))
            screen.blit(text,tpos)
            screen.blit(text2,t2pos)
            screen.blit(t3,t3pos)
            pygame.display.flip()
            time.sleep(1)
            while True:
                input_state = GPIO.input(18)
                input_state2= GPIO.input(17)
                input_state3= GPIO.input(21)
                screen.blit(text,tpos)
                screen.blit(text2,t2pos)
                screen.blit(t3,t3pos)
                pygame.display.flip()
                if input_state2==False and input_state != False and input_state3 != False:
                    save()
                    pygame.quit()
                    quit()
                elif input_state==False and input_state2 != False and input_state3 != False:
                    break
                elif input_state !=False and input_state2 !=False and input_state3 ==False:
                    breakout=True
                    break
            
        if breakout==True:
            break
        
    #sets the single touch variable for the fire button
        if input_state3 != False and var3==False:
            var3=True

    ##Draws all objects, including the background
        screen.blit(background, (0,0))
        
        sd=font.render('lives: '+str(lives),1,(200,250,250))
        sdp=sd.get_rect()
        sdp.centerx=width/3
        sdp.centery=height-75
        hd=font.render('hits: '+str(hits),1,(200,250,250))
        hdp=hd.get_rect()
        hdp.centerx=width*2/3
        hdp.centery=height-75
        screen.blit(sd,sdp)
        screen.blit(hd,hdp)
        
        #player
        pygame.draw.rect(screen,shipcolor,(x,y,80,40))
        #enemies
        if len(enemyx)>0:
            for i in range(0,len(enemyx)):
                xpos=enemyx[i]
                ypos=enemyy[i]
                enemyx.pop(i)
                enemyx.insert(i,xpos+diff)
                pygame.draw.circle(screen, enemycolor, (xpos,ypos),20)
                if xpos>width+10:
                    lives=lives-1
                    popliste.insert(0,i)
        #bulletsd
        if len(bulletx)>0:
            for i in range(0,len(bulletx)):
                xpos=bulletx[i]
                ypos=bullety[i]
                bullety.pop(i)
                bullety.insert(i,ypos-10)
                pygame.draw.circle(screen, shipcolor, (xpos,ypos),10)
                if ypos<-10:
                    poplistb.insert(0,i)
                #tests for collision with enemy
                for a in enemyx:
                    if xpos-a>-30 and xpos-a<30:
                        if ypos-(enemyy[enemyx.index(a)])>-30 and ypos-(enemyy[enemyx.index(a)])<30:
                            poplistb.insert(0,i)
                            popliste.insert(0,(enemyx.index(a)))
                            hits=hits+1
        #removes bullets that are off the screen
        if len(poplistb)>0:
            for i in poplistb:
                bulletx.pop(i)
                bullety.pop(i)
            poplistb=[]
        #removes and replaces enemies
        if len(popliste)>0:
            for i in popliste:
               enemyx.pop(i)
               enemyy.pop(i)
               xit=random.randint(-200,-20)
               yit=random.randint(30,300)
               for i in enemyx:
                   if xit-i>-50 and xit-i<50:
                       xit=xit-300
               enemyx.insert(0,(xit))
               enemyy.insert(0,(yit))
            popliste=[]

        pygame.display.flip()
        if lives<1:
            pygame.init()
            background.fill((30,30,30))
            screen.blit(background, (0,0))
            font=pygame.font.match_font('roboto')
            font=pygame.font.Font(font,185)
            dd=font.render('Game Over',1,(240,0,0))
            ddp=dd.get_rect()
            ddp.centerx=background.get_rect().centerx
            ddp.centery=background.get_rect().centery
            font=pygame.font.Font(None,140)
            t=font.render(str(hits),1,(0,150,240))
            tp=t.get_rect()
            tp.centerx=width/2
            tp.centery=100
            screen.blit(dd,ddp)
            screen.blit(t,tp)
            if difficulty=='EASY':
                if hits>int(easyscores[4]):
                    for i in range(len(easyscores)):
                        p=0
                        if hits>=int(easyscores[i]):
                            p=i
                            break
                    easyscores.pop()
                    easyscores.insert(p,hits)
                    font=pygame.font.Font(None,60)
                    t=font.render('TOP 5!',1,(0,220,0))
                    tp=t.get_rect()
                    tp.centerx=width/2
                    tp.centery=height-80
                    screen.blit(t,tp)
            elif difficulty=='MEDIUM':
                if hits>int(medscores[4]):
                    for i in range(len(medscores)):
                        p=0
                        if hits>=int(medscores[i]):
                            p=i
                            break
                    medscores.pop()
                    medscores.insert(p,hits)
                    font=pygame.font.Font(None,60)
                    t=font.render('TOP 5!',1,(0,220,0))
                    tp=t.get_rect()
                    tp.centerx=width/2
                    tp.centery=height-80
                    screen.blit(t,tp)
            elif difficulty=='HARD':
                if hits>int(hardscores[4]):
                    for i in range(len(hardscores)):
                        p=0
                        if hits>=int(hardscores[i]):
                            p=i
                            break
                    hardscores.pop()
                    hardscores.insert(p,hits)
                    font=pygame.font.Font(None,60)
                    t=font.render('TOP 5!',1,(0,220,0))
                    tp=t.get_rect()
                    tp.centerx=width/2
                    tp.centery=height-80
                    screen.blit(t,tp)
            pygame.display.flip()
            time.sleep(3)
            break
    background.fill((0,0,0))
    screen.blit(background,(0,0))
    display_scores()
    save()
    
main_menu()
