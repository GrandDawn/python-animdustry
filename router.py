from init import *
import math
import pygame
from conveyor import *
class Router():
    def __init__(self,screen,pos,diag=0):
        self.unuse=0
        self.diag=diag
        self.posx=pos[0]
        self.posy=pos[1]
        self.turnleft=3
        self.repaintlist=[]
        self.movelist=[]
        
        self.image=pygame.image.load('assets-raw/sprites/outlined/router.png')
        self.image=pygame.transform.scale_by(self.image,(1.4,1.4))
        self.degree=0
        
        self.x=calc(self.posx,width)+self.image.get_width()/2+2
        self.y=calc(self.posy,height)+self.image.get_height()/2+3

        self.size=1
        self.shoot_tick=0
        self.turntype=0
        self.draw(screen)
    #router shoot
    def shoot(self,screen,conveyor_list):
        if(self.diag!=0):
            for i in [[1,1],[-1,-1],[1,-1],[-1,1]]:
                if(self.posx+i[0]<0 or self.posx+i[0]>=gridsize or self.posy+i[1]<0 or self.posy+i[1]>=gridsize):continue
                conveyor_list.append(Conveyor(screen,[self.posx+i[0],self.posy+i[1]],i))
        else:
            for i in [[1,0],[-1,0],[0,-1],[0,1]]:
                if(self.posx+i[0]<0 or self.posx+i[0]>=gridsize or self.posy+i[1]<0 or self.posy+i[1]>=gridsize):continue
                conveyor_list.append(Conveyor(screen,[self.posx+i[0],self.posy+i[1]],i))
    #router move
    def move(self,shr=0):
        self.repaintlist=[[self.posx,self.posy]]
        self.movelist.append([0,1-shr*1])
        self.movelist.append([30,1-shr*0.7])
        self.movelist.append([30,1-shr*0.3])
        self.movelist.append([30,1])
    #router draw
    def draw(self,screen):
        if(self.unuse==1):
            return
        image1=pygame.transform.rotate(self.image,self.degree)
        gen_border(image1)
        image1=pygame.transform.scale_by(image1,(self.size,self.size))
        screen.blit(image1,(self.x-image1.get_width()/2,self.y-image1.get_height()/2))
    #router new tick
    def newtick(self,screen,char):
        if(self.size==0):self.unuse=1
        if(self.unuse==1):
            return
        leng=len(self.movelist)
        if(leng==0):
            self.repaintlist=[]
        if(leng==0 or leng==4):
            if((len(char.movelist)==0 or char.movelist[len(char.movelist)-1]==[0,0]) and self.posx==char.posx and self.posy==char.posy):
                char.is_hit=1
                self.unuse=1
        if(leng>0):
            self.degree+=self.movelist[leng-1][0]
            self.size=self.movelist[leng-1][1]
            self.movelist.pop()
            self.draw(screen)
            if(len(self.movelist)==0):
                self.repaintlist=[[self.posx,self.posy]]
        if(self.shoot_tick>0):
            self.shoot_tick-=1
            if(self.shoot_tick==0):return 1919810
    #router new turn
    def newturn(self,char):
        self.turnleft-=1
        if(self.turnleft==0):
            self.move(1)
        else:
            self.move()
            self.shoot_tick=3
            
        
