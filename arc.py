from init import *
import math
import pygame
class Mine():
    def __init__(self,screen,pos,turnleft=6):
        self.unuse=0
        self.posx=pos[0]
        self.posy=pos[1]
        self.turnleft=turnleft
        self.repaintlist=[]
        self.size=1
        self.image=pygame.image.load('assets-raw/sprites/outlined/mine.png')
        self.image=pygame.transform.scale_by(self.image,(1.5,1.5))
        gen_border(self.image)
        self.x=calc(self.posx,width)+self.image.get_width()/2
        self.y=calc(self.posy,height)+self.image.get_height()/2
        self.draw_tick=0
        self.draw(screen)
    #mine draw
    def draw(self,screen):
        if(self.unuse==1):return
        image1=pygame.transform.scale_by(self.image,(self.size,self.size))
        screen.blit(image1,(self.x-image1.get_width()/2,self.y-image1.get_height()/2))
    #mine newtick
    def newtick(self,screen,char):
        if(self.unuse==1):return
        self.repaintlist=[]
        if(self.turnleft==0):
            self.size-=0.5
            self.draw(screen)
            self.repaintlist=[[self.posx,self.posy]]
        if(self.size==0):self.unuse=1
        if(self.unuse==1):return
        if((len(char.movelist)==0 or char.movelist[len(char.movelist)-1]==[0,0]) and self.posx==char.posx and self.posy==char.posy):
            char.is_hit=1
            self.unuse=1
            self.repaintlist=[[self.posx,self.posy]]
        if(self.draw_tick>0):
            self.draw_tick=0
            self.draw(screen)
        
    #mine newturn
    def newturn(self,char):
        self.turnleft-=1
        self.draw_tick=3
        if(self.turnleft==0):
            self.size+=0.5
            self.repaintlist=[[self.posx,self.posy]]
        
class Arc():
    def __init__(self,screen,pos,direction,mine_turn):
        self.unuse=0
        self.posx=pos[0]
        self.posy=pos[1]
        self.direction=direction
        self.repaintlist=[]
        self.movelist=[]
        self.image=pygame.image.load('assets-raw/sprites/outlined/arc.png')
        self.image=pygame.transform.scale_by(self.image,(1.5,1.5))
        self.x=calc(self.posx,width)+self.image.get_width()/2+2
        self.y=calc(self.posy,height)+self.image.get_height()/2+2
        self.mine_turn=mine_turn
        gen_border(self.image)
        deg=math.atan2(-direction[1],direction[0])/math.pi*180
        self.image=pygame.transform.rotate(self.image,deg)
        self.draw(screen)
    #arc move
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
    #arc draw
    def draw(self,screen):
        if(self.unuse==1):
            return
        screen.blit(self.image,(self.x-self.image.get_width()/2,self.y-self.image.get_height()/2))
    #arc newtick
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
    #arc leave mine
    def leave_mine(self,screen,mine_list):
        if(self.unuse==1):
            return
        mine_list.append(Mine(screen,[self.posx,self.posy],self.mine_turn))
    #arc new turn
    def newturn(self,char):
        self.move()
