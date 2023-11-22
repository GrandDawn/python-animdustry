from init import *
from files import *
import pygame

class Char():
    def __init__(self,saving):
        self.is_hit=0
        self.hit_animation=0
        self.movelist=[]
        self.faillist=[]
        self.repaintlist=[]
        self.char=[]
        self.char_hit=[]
        self.explode_animation=[]
        self.x=width/2
        self.y=height/2
        self.posx=(gridsize-1)/2
        self.posy=(gridsize-1)/2
        self.direction=0
        self.nowdirection=0
        self.lastmove=[0,0]
        self.change_char(saving,saving['default_char'])
        self.shieldsize=0
        self.fail_pic=pygame.transform.scale_by(pygame.image.load('assets-raw/sprites/outlined/fail.png'),(1.5,1.5))
        gen_border(self.fail_pic)
        self.shield_pic=pygame.transform.scale_by(pygame.image.load('assets-raw/sprites/outlined/shield.png'),(1.2,1.2))
        gen_border(self.shield_pic)
        #load images
        self.char.append(gen_border(pygame.transform.scale_by(pygame.image.load('assets-raw/sprites/outlined/unit-alpha.png'),(1.5,1.5)),-1))
        self.char_hit.append(gen_border(pygame.transform.scale_by(pygame.image.load('assets-raw/sprites/outlined/unit-alpha-hit.png'),(1.5,1.5)),-1))
        self.char.append(gen_border(pygame.transform.scale_by(pygame.image.load('assets-raw/sprites/outlined/unit-mono.png'),(1.5,1.5)),-1))
        self.char_hit.append(gen_border(pygame.transform.scale_by(pygame.image.load('assets-raw/sprites/outlined/unit-mono-hit.png'),(1.5,1.5)),-1))
        self.char.append(gen_border(pygame.transform.scale_by(pygame.image.load('assets-raw/sprites/outlined/unit-oct.png'),(1.5,1.5)),-1))
        self.char_hit.append(gen_border(pygame.transform.scale_by(pygame.image.load('assets-raw/sprites/outlined/unit-oct-hit.png'),(1.5,1.5)),-1))
        self.char.append(gen_border(pygame.transform.scale_by(pygame.image.load('assets-raw/sprites/outlined/unit-crawler.png'),(1.5,1.5)),-1))
        self.char_hit.append(gen_border(pygame.transform.scale_by(pygame.image.load('assets-raw/sprites/outlined/unit-crawler-hit.png'),(1.5,1.5)),-1))
        self.char.append(gen_border(pygame.transform.scale_by(pygame.image.load('assets-raw/sprites/outlined/unit-zenith.png'),(1.5,1.5)),-1))
        self.char_hit.append(gen_border(pygame.transform.scale_by(pygame.image.load('assets-raw/sprites/outlined/unit-zenith-hit.png'),(1.5,1.5)),-1))
        self.char.append(gen_border(pygame.transform.scale_by(pygame.image.load('assets-raw/sprites/outlined/unit-quad.png'),(1.5,1.5)),-1))
        self.char_hit.append(gen_border(pygame.transform.scale_by(pygame.image.load('assets-raw/sprites/outlined/unit-quad-hit.png'),(1.5,1.5)),-1))
        self.char.append(gen_border(pygame.transform.scale_by(pygame.image.load('assets-raw/sprites/outlined/unit-oxynoe.png'),(1.5,1.5)),-1))
        self.char_hit.append(gen_border(pygame.transform.scale_by(pygame.image.load('assets-raw/sprites/outlined/unit-oxynoe-hit.png'),(1.5,1.5)),-1))
        self.char.append(gen_border(pygame.transform.scale_by(pygame.image.load('assets-raw/sprites/outlined/unit-sei.png'),(1.5,1.5)),-1))
        self.char_hit.append(gen_border(pygame.transform.scale_by(pygame.image.load('assets-raw/sprites/outlined/unit-sei-hit.png'),(1.5,1.5)),-1))
        #load explosion animations
        self.explode_animation.append(pygame.transform.scale_by(pygame.image.load('assets-raw/sprites/explode0.png'),(1.5,1.5)))
        self.explode_animation.append(pygame.transform.scale_by(pygame.image.load('assets-raw/sprites/explode1.png'),(1.5,1.5)))
        self.explode_animation.append(pygame.transform.scale_by(pygame.image.load('assets-raw/sprites/explode2.png'),(1.5,1.5)))
        self.explode_animation.append(pygame.transform.scale_by(pygame.image.load('assets-raw/sprites/explode3.png'),(1.5,1.5)))
        self.explode_animation.append(pygame.transform.scale_by(pygame.image.load('assets-raw/sprites/explode4.png'),(1.5,1.5)))
        self.explode_tick=0
        self.explode_grid=[]
        
        self.wall_image=pygame.transform.scale_by(pygame.image.load('assets-raw/sprites/wall.png'),(1.5,1.5))
        self.wall_size=0
        self.wall_health=3
        self.wall_turnleft=10
        self.wall_position=[-1,-1]
    #refill skill cooldown
    def newskill(self):
        if(self.type==0):self.skilltime=10
        elif(self.type==2):self.skilltime=30
        elif(self.type==5):self.skilltime=6
        else:self.skilltime=4
    #change character
    def change_char(self,saving,type1):
        save_saving(0)
        if(type1==3):self.explode_color=(147,112,219,255)
        elif(type1==0 or type1==4 or type1==7):self.explode_color=(196,87,25,255)
        else:self.explode_color=(1,163,104,255)
        self.type=type1
        saving['default_char']=type1
        self.newskill()
    #decrease skill time and make skill
    def moveend(self,maingame,direction):
        self.skilltime-=1
        if(self.skilltime==0):
            if(self.type==0):
                self.wall_position=[self.posx-direction[0],self.posy-direction[1]]
                self.wall_size=1
                self.wall_health=3
                self.wall_turnleft=10
            elif(self.type==1):
                maingame.score+=1
            elif(self.type==2):
                if(self.shieldsize==0):
                    self.shieldsize=0.1
            elif(self.type==3):
                self.explode_tick=-1
                self.explode_grid=[[self.posx,self.posy],[self.posx-1,self.posy],[self.posx+1,self.posy],[self.posx,self.posy-1],[self.posx,self.posy+1]]
            elif(self.type==4):
                self.explode_tick=-1
                self.explode_grid=[[self.posx,self.posy],[self.posx+direction[0],self.posy+direction[1]],
                                   [self.posx+direction[0]*2,self.posy+direction[1]*2],[self.posx+direction[0]*3,self.posy+direction[1]*3]]
            elif(self.type==5):
                self.explode_tick=-1
                self.explode_grid=[[self.posx-1,self.posy-1],[self.posx-1,self.posy],[self.posx-1,self.posy+1],
                                   [self.posx,self.posy-1],[self.posx,self.posy],[self.posx,self.posy+1],
                                   [self.posx+1,self.posy-1],[self.posx+1,self.posy],[self.posx+1,self.posy+1]]
            elif(self.type==6):
                maingame.bot_move+=1
                maingame.drawbotmove()
            elif(self.type==7):
                self.explode_tick=-1
                self.explode_grid=[[self.posx,self.posy],[self.posx-1,self.posy-1],[self.posx-2,self.posy-2],[self.posx+1,self.posy-1],[self.posx+2,self.posy-2]
                                                        ,[self.posx-1,self.posy+1],[self.posx-2,self.posy+2],[self.posx+1,self.posy+1],[self.posx+2,self.posy+2]]

            else:assert(0)
            self.newskill()
    #check whether movable
    def check(self,maingame):
        turndist=(maingame.tick%(60*maingame.fps/maingame.bpm))/(60*maingame.fps/maingame.bpm)
        if(turndist>=0.95 or turndist<=0.05):print('precise!')
        elif(turndist<0.20):print('slow!')
        elif(turndist>0.8):print('fast!')
        else:print('bad!')
        if((turndist>=0.20 and turndist<=0.80) or len(self.movelist)>0):
            self.faillist=[self.posx,self.posy,maingame.fps/5]
            maingame.score-=2
            maingame.score=max(0,maingame.score)
            return 0
        return 1
    #charcater move
    def move(self,maingame,direction):
        if(direction==[0,0]):
            return
        if(self.posx+direction[0]<0 or self.posx+direction[0]>=gridsize or self.posy+direction[1]<0 or self.posy+direction[1]>=gridsize):
            return
        if(self.check(maingame)==0):
            return
        self.lastmove=direction
        for i in range(22):self.movelist.append([0,0])
        self.movelist.append([9*direction[0],9*direction[1]])
        self.movelist.append([15*direction[0],15*direction[1]])
        self.movelist.append([9*direction[0],9*direction[1]])
        if(direction==[1,0]):
            self.repaintlist=[[self.posx,self.posy],[self.posx,self.posy-1],[self.posx+1,self.posy],[self.posx+1,self.posy-1]]
            if(self.type==6):self.repaintlist.append([self.posx-1,self.posy-1])
        if(direction==[-1,0]):
            self.repaintlist=[[self.posx,self.posy],[self.posx,self.posy-1],[self.posx-1,self.posy],[self.posx-1,self.posy-1]]
        if(direction==[0,-1]):
            self.repaintlist=[[self.posx,self.posy],[self.posx,self.posy-1],[self.posx,self.posy-2]]
            if(self.type==6):self.repaintlist.append([self.posx-1,self.posy-1])
        if(direction==[0,1]):
            self.repaintlist=[[self.posx,self.posy],[self.posx,self.posy-1],[self.posx,self.posy+1]]
            if(self.type==6):self.repaintlist.append([self.posx-1,self.posy-1])

        if(direction==[1,0]):self.direction=0
        if(direction==[-1,0]):self.direction=1
        self.posx+=direction[0]
        self.posy+=direction[1]
        maingame.score+=1
        if(self.posx==self.wall_position[0] and self.posy==self.wall_position[1]):
            self.wall_size=0
        self.moveend(maingame,direction)
        maingame.drawscore()
    #character draw
    def draw(self,screen,maingame):
        turndist=(maingame.tick%(60*maingame.fps/maingame.bpm))/(60*maingame.fps/maingame.bpm)
        #draw wall
        if(self.wall_size>0):
            if(self.wall_size<1):image1=pygame.transform.scale_by(self.wall_image,(self.wall_size,self.wall_size))
            else:image1=pygame.transform.scale_by(self.wall_image,(max(4*math.sin(2*math.pi*turndist+1.25)+0.2-3,1),max(4*math.sin(2*math.pi*turndist+1.25)+0.2-3,1)))
            screen.blit(image1,(calc(self.wall_position[0],width)+15-image1.get_width()/2,calc(self.wall_position[1],height)+15-image1.get_height()/2))
        #draw explosion
        for i in self.explode_grid:
            if(i[0]<0 or i[1]<0 or i[0]>=gridsize or i[1]>=gridsize):continue
            image1=self.explode_animation[self.explode_tick]
            fill(image1,self.explode_color)
            screen.blit(image1,(calc(i[0],width)+15-image1.get_width()/2,calc(i[1],height)+15-image1.get_height()/2))
        #draw shield
        if(self.shieldsize>0):
            tmp2=pygame.transform.scale_by(self.shield_pic,(self.shieldsize,self.shieldsize))
            screen.blit(tmp2,(self.x-tmp2.get_width()/2+5,self.y-tmp2.get_height()/2))
        
        if self.direction!=self.nowdirection:
            self.nowdirection=self.direction
            for i in self.char:
                flip(i)
            for i in self.char_hit:
                flip(i)
        if(self.hit_animation==0):tmp=self.char[self.type]
        else:tmp=self.char_hit[self.type]
        
        if(turndist<=0.1):tmp=pygame.transform.scale_by(tmp,(1,1-turndist*2))
        else:tmp=pygame.transform.scale_by(tmp,(1,2/9*turndist+7/9))
        screen.blit(tmp,(self.x-tmp.get_width()/2+5,self.y-tmp.get_height()+5))
    #character new tick
    def newtick(self,screen,maingame):
        #move
        leng=len(self.movelist)
        if(leng==0 or self.movelist[leng-1]==[0,0]):
            self.repaintlist=[[self.posx,self.posy],[self.posx,self.posy-1]]
            if(self.type==6):self.repaintlist.append([self.posx-1,self.posy-1])
        if(leng>0):
            self.x+=self.movelist[leng-1][0]
            self.y+=self.movelist[leng-1][1]
            self.movelist.pop()
        if(self.faillist!=[]):
            if(self.faillist[2]>=1):screen.blit(self.fail_pic,(calc(self.faillist[0],width),calc(self.faillist[1],height)))
            self.repaintlist.append([self.faillist[0],self.faillist[1]])
            self.faillist[2]-=1
            if self.faillist[2]==0:
                self.faillist=[]
        #whether be hitted
        if(self.is_hit==1):
            pygame.mixer.Channel(0).set_volume(0.1)
            pygame.mixer.Channel(0).play(pygame.mixer.Sound('assets/sounds/hit.ogg'))
            if(self.shieldsize>0):
                self.shieldsize=0
                if(self.type==2):self.newskill()
            elif(self.hit_animation==0):
                self.hit_animation=maingame.fps*3/4    
                maingame.health-=1
                maingame.drawhealth()
                maingame.score=max(maingame.score-15,0)
                maingame.drawscore()
        #update shield
        if(self.shieldsize>0 and self.shieldsize<1):
            self.shieldsize+=0.1
        
        self.hit_animation=max(self.hit_animation-1,0)
        self.is_hit=0
        #update explosion
        self.explode_tick+=1
        if(self.explode_tick==4):self.explode_grid=[]
        self.repaintlist+=self.explode_grid
        #update wall
        if(self.wall_size>0):self.repaintlist.append(self.wall_position)
        if(self.wall_size<1 and self.wall_size>0):
            self.wall_size-=0.33
            self.repaintlist.append(self.wall_position)
        
        self.draw(screen,maingame)
    #character new turn
    def newturn(self):
        self.wall_turnleft-=1
        if((self.wall_turnleft==0 or self.wall_health<=0) and self.wall_size==1):
            self.wall_size=0.99
            self.repaintlist.append(self.wall_position)
            
