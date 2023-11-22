from init import *
import math
import pygame
class Bullet():
    def __init__(self,screen,pos,direction,color='pink'):
        self.unuse=0
        self.type=1
        self.posx=pos[0]
        self.posy=pos[1]
        self.direction=direction
        self.repaintlist=[]
        self.movelist=[]
        if(color=='yellow'):self.image=pygame.image.load('assets-raw/sprites/outlined/bullet.png')
        elif(color=='pink'):self.image=pygame.image.load('assets-raw/sprites/outlined/bullet-pink.png')
        elif(color=='purple'):self.image=pygame.image.load('assets-raw/sprites/outlined/bullet-purple.png')
        self.image=pygame.transform.scale_by(self.image,(1.5,1.5))
        self.x=calc(self.posx,width)+self.image.get_width()/2
        self.y=calc(self.posy,height)+self.image.get_height()/2
        
        gen_border(self.image)
        deg=math.atan2(-direction[1],direction[0])/math.pi*180
        self.image=pygame.transform.rotate(self.image,deg)
        self.draw(screen)
    #bullet move
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
        self.movelist.append([9*self.direction[0],9*self.direction[1]])
        self.movelist.append([15*self.direction[0],15*self.direction[1]])
        self.movelist.append([9*self.direction[0],9*self.direction[1]])
    #bullet draw
    def draw(self,screen):
        if(self.unuse==1):
            return
        screen.blit(self.image,(self.x-self.image.get_width()/2,self.y-self.image.get_height()/2))
    #bullet newtick
    def newtick(self,screen,char):
        if(self.unuse==1):
            return
        leng=len(self.movelist)
        if(leng==0):
            self.repaintlist=[]
        if(leng==0 or leng==3):
            if((len(char.movelist)==0 or char.movelist[len(char.movelist)-1]==[0,0]) and self.posx==char.posx and self.posy==char.posy):
                char.is_hit=1
                self.unuse=1
        if(leng>0):
            self.x+=self.movelist[leng-1][0]
            self.y+=self.movelist[leng-1][1]
            self.movelist.pop()
            self.draw(screen)
            if(len(self.movelist)==0):
                self.repaintlist=[[self.posx,self.posy]]
    #bullet newturn
    def newturn(self,char):
        self.move()
