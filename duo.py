import pygame
from init import *
from bullet import *
class Duo():
    def __init__(self,screen,pos,turns):
        self.posx=pos[0]
        self.posy=pos[1]
        self.image=pygame.image.load('assets-raw/sprites/outlined/duo.png')
        self.image=pygame.transform.scale_by(self.image,(1.5,1.5))
        if(self.posx==0):
            self.direction=[1,0]
            self.image=pygame.transform.rotate(self.image,-90)
        if(self.posy==0):
            self.direction=[0,1]
            self.image=pygame.transform.rotate(self.image,180)
        if(self.posx==gridsize-1):
            self.direction=[-1,0]
            self.image=pygame.transform.rotate(self.image,90)
        if(self.posy==gridsize-1):
            self.direction=[0,-1]
            self.image=pygame.transform.rotate(self.image,0)
        gen_border(self.image)
        self.x=calc(self.posx,width)+self.image.get_width()/2+3
        self.y=calc(self.posy,height)+self.image.get_height()/2+3
        self.repaintlist=[]
        self.movelist=[]
        self.turnleft=turns
        self.unuse=0
        self.shoot_tick=0
        self.size=1
        self.draw(screen)
    #duo draw
    def draw(self,screen):
        tmp=pygame.transform.scale_by(self.image,[self.size,self.size])
        screen.blit(tmp,(self.x-tmp.get_width()/2,self.y-tmp.get_height()/2))
    #duo newtick
    def newtick(self,screen,char):
        if(self.turnleft==0):
            return
        leng=len(self.movelist)
        if(leng==0):
            self.size=1
            self.repaintlist=[]
        if(leng>0):
            self.x+=self.movelist[leng-1][0]
            self.y+=self.movelist[leng-1][1]
            self.size=self.movelist[leng-1][2]
            self.draw(screen)
            self.movelist.pop()
            if(len(self.movelist)==0):
                self.repaintlist=[[self.posx,self.posy]]
        if(self.shoot_tick>0):
            self.shoot_tick-=1
            if(self.shoot_tick==0):return 114514
    #duo move
    def move(self,direction):
        self.repaintlist=[[self.posx,self.posy],[self.posx+direction[0],self.posy+direction[1]]]
        self.posx+=direction[0]
        self.posy+=direction[1]
        self.movelist.append([9*direction[0],9*direction[1],1.3])
        self.movelist.append([15*direction[0],15*direction[1],1.3])
        self.movelist.append([9*direction[0],9*direction[1],1.3])
    #duo shoot
    def shoot(self,screen,duo_bullet_list):
        duo_bullet_list.append(Bullet(screen,[self.posx,self.posy],self.direction,'yellow'))
    #duo newturn
    def newturn(self,char):
        self.turnleft-=1;
        if(self.turnleft==0):
            self.unuse=1;
            return
        if(self.turnleft%2==1):
            if(self.direction[0]==0):
                if(char.posx>self.posx):self.move([1,0])
                elif(char.posx<self.posx):self.move([-1,0])
                else:self.move([0,0])
            if(self.direction[1]==0):
                if(char.posy>self.posy):self.move([0,1])
                elif(char.posy<self.posy):self.move([0,-1])
                else:self.move([0,0])
        else:self.move([0,0])
        if(self.turnleft%4==1):
            self.shoot_tick=3
