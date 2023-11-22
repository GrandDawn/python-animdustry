from init import *
import math
import pygame
class Conveyor():
    def __init__(self,screen,pos,direction):
        self.unuse=0
        self.type=1
        self.posx=pos[0]
        self.posy=pos[1]
        self.direction=direction
        self.repaintlist=[]
        self.movelist=[]
        
        self.image=pygame.image.load('assets-raw/sprites/outlined/conveyor.png')
        if(self.direction[0]==0 or self.direction[1]==0):
            self.image=pygame.transform.scale_by(self.image,(1.4,1.4))
            self.image1=pygame.transform.scale_by(self.image,(1.4,1))
        else:
            self.image=pygame.transform.scale_by(self.image,(1.3,1.3))
            self.image1=pygame.transform.scale_by(self.image,(1.3,1))
        gen_border(self.image)
        gen_border(self.image1)
        
        self.x=calc(self.posx,width)+self.image.get_width()/2+2
        self.y=calc(self.posy,height)+self.image.get_height()/2+3
        
        
        deg=math.atan2(-direction[1],direction[0])/math.pi*180
        self.image=pygame.transform.rotate(self.image,deg)
        self.image1=pygame.transform.rotate(self.image1,deg)
        self.draw(screen)
    #conveyor move
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
        self.movelist.append([0,0])
        self.movelist.append([9*self.direction[0],9*self.direction[1]])
        self.movelist.append([15*self.direction[0],15*self.direction[1]])
        self.movelist.append([9*self.direction[0],9*self.direction[1]])
    #conveyor draw
    def draw(self,screen):
        if(self.unuse==1):
            return
        if(len(self.movelist)==0):screen.blit(self.image,(self.x-self.image.get_width()/2,self.y-self.image.get_height()/2))
        else:screen.blit(self.image1,(self.x+1-self.image1.get_width()/2,self.y-self.image1.get_height()/2))
    #conveyor new tick
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
            self.movelist.pop()
            self.draw(screen)
            if(len(self.movelist)==0):
                self.repaintlist=[[self.posx,self.posy]]
    #conveyor new turn
    def newturn(self,char):
        self.move()
