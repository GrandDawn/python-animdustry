from init import *
import math
import pygame
from conveyor import *
class Sorter():
    def __init__(self,screen,pos,direction):
        self.unuse=0
        self.type=1
        self.posx=pos[0]
        self.posy=pos[1]
        self.direction=direction
        self.repaintlist=[]
        self.movelist=[]
        
        self.image=pygame.image.load('assets-raw/sprites/outlined/sorter.png')
        self.image=pygame.transform.scale_by(self.image,(1.4,1.4))
        self.degree=0
        
        
        self.x=calc(self.posx,width)+self.image.get_width()/2+2
        self.y=calc(self.posy,height)+self.image.get_height()/2+3

        self.shoot_tick=0
        self.turntype=0
        self.draw(screen)
    #sorter shoot
    def shoot(self,screen,conveyor_list):
        for i in [[1,0],[-1,0],[0,-1],[0,1]]:
            if(i[0]+self.direction[0]==0 and i[1]+self.direction[1]==0):continue
            if(self.posx+i[0]<0 or self.posx+i[0]>=gridsize or self.posy+i[1]<0 or self.posy+i[1]>=gridsize):continue
            conveyor_list.append(Conveyor(screen,[self.posx+i[0],self.posy+i[1]],i))
    #sorter move
    def move(self):
        if(self.posx==gridsize-1 and self.direction[0]==1 or self.posy==gridsize-1  and self.direction[1]==1 or self.posx==0 and self.direction[0]==-1 or self.posy==0 and self.direction[1]==-1):
            self.unuse=1
            self.repaintlist=[[self.posx,self.posy]]
            return
        self.repaintlist.clear()
        for i in [self.posx,self.posx+self.direction[0]]:
            for j in [self.posy,self.posy+self.direction[1]]:
                self.repaintlist.append([i,j])
        self.posx+=self.direction[0]
        self.posy+=self.direction[1]
        self.movelist.append([0,0,0])
        self.movelist.append([9*self.direction[0],9*self.direction[1],30])
        self.movelist.append([15*self.direction[0],15*self.direction[1],30])
        self.movelist.append([9*self.direction[0],9*self.direction[1],30])
    #sorter draw
    def draw(self,screen):
        if(self.unuse==1):
            return
        image1=pygame.transform.rotate(self.image,self.degree)
        gen_border(image1)
        screen.blit(image1,(self.x-image1.get_width()/2,self.y-image1.get_height()/2))
    #sorter new tick
    def newtick(self,screen,char):
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
            self.x+=self.movelist[leng-1][0]
            self.y+=self.movelist[leng-1][1]
            self.degree+=self.movelist[leng-1][2]
            self.movelist.pop()
            self.draw(screen)
            if(len(self.movelist)==0):
                self.repaintlist=[[self.posx,self.posy]]
        if(self.shoot_tick>0):
            self.shoot_tick-=1
            if(self.shoot_tick==0):return 1919810
    #sorter new turn
    def newturn(self,char):
        self.turntype=1-self.turntype
        if(self.turntype==0):
            self.move()
        else:
            self.movelist.append([0,0,0])
            self.movelist.append([0,0,30])
            self.movelist.append([0,0,30])
            self.movelist.append([0,0,30])
            self.repaintlist=[[self.posx,self.posy]]
            self.shoot_tick=3
            
        
