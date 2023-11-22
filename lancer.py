import pygame
from init import *
class Lancer():
    def __init__(self,screen,pos,backgroundcolor):
        self.backgroundcolor=backgroundcolor
        self.unuse=0
        self.turnleft=2
        self.size=1
        self.tick=0
        self.posx=pos[0]
        self.posy=pos[1]
        #influence_list for no drawing tile
        self.influence_list=[]
        self.repaintlist=[]
        if(self.posx==-1 or self.posx==gridsize):
            for i in range(0,gridsize):self.influence_list.append([i,self.posy])
        else:
            for i in range(0,gridsize):self.influence_list.append([self.posx,i])

        self.image=gen_border(pygame.image.load('assets-raw/sprites/outlined/lancer.png'))
        if(self.posx==-1):self.image=pygame.transform.rotate(self.image,270)
        if(self.posx==gridsize):self.image=pygame.transform.rotate(self.image,90)
        if(self.posy==-1):self.image=pygame.transform.rotate(self.image,180)
        
        self.draw(screen)
    #clear the parts for a lancer
    def draw_clear(self,screen):
        if(self.posx==-1):pygame.draw.rect(screen,self.backgroundcolor,(calc(-2,width),calc(self.posy-1,height),66,99))
        if(self.posx==gridsize):pygame.draw.rect(screen,self.backgroundcolor,(calc(gridsize,width),calc(self.posy-1,height),66,99))
        if(self.posy==-1):pygame.draw.rect(screen,self.backgroundcolor,(calc(self.posx-1,width),calc(-2,height),99,66))
        if(self.posy==gridsize):pygame.draw.rect(screen,self.backgroundcolor,(calc(self.posx-1,width),calc(gridsize,height),99,66))
    #lancer draw
    def draw(self,screen,type1=0):
        if(self.unuse==1):return    
        if(self.posx==-1 or self.posx==gridsize):pygame.draw.rect(screen,self.backgroundcolor,(calc(0,width)-3,calc(self.posy,height)-3,calc(gridsize,width)-calc(0,width)+6,39))
        else:pygame.draw.rect(screen,self.backgroundcolor,(calc(self.posx,width)-3,calc(0,height)-3,39,calc(gridsize,height)-calc(0,height)+6))
        if(self.turnleft==2 and self.tick<=20):
            #start animation
            self.draw_clear(screen)
            image1=pygame.transform.scale_by(self.image,(self.tick/10,self.tick/10))
            screen.blit(image1,(calc(self.posx,width)+16.5-image1.get_width()/2,calc(self.posy,height)+16.5-image1.get_height()/2))
            if(self.posx==-1 or self.posx==gridsize):
                pygame.draw.rect(screen,(255,255,255),(calc(0,width),calc(self.posy,height)-3+self.tick/4,calc(gridsize,width)-calc(0,width),5))
                pygame.draw.rect(screen,(self.backgroundcolor[0]+(255-self.backgroundcolor[0])/20*self.tick,
                                         self.backgroundcolor[1]+(255-self.backgroundcolor[1])/20*self.tick,
                                         self.backgroundcolor[2]+(255-self.backgroundcolor[2])/20*self.tick),(calc(0,width),calc(self.posy,height)+2,calc(gridsize,width)-calc(0,width),26))
                pygame.draw.rect(screen,(255,255,255),(calc(0,width),calc(self.posy,height)+28-self.tick/4,calc(gridsize,width)-calc(0,width),5))
            else:
                pygame.draw.rect(screen,(255,255,255),(calc(self.posx,width)-3+self.tick/4,calc(0,height),5,calc(gridsize,height)-calc(0,height)))
                pygame.draw.rect(screen,(self.backgroundcolor[0]+(255-self.backgroundcolor[0])/20*self.tick,
                                         self.backgroundcolor[1]+(255-self.backgroundcolor[1])/20*self.tick,
                                         self.backgroundcolor[2]+(255-self.backgroundcolor[2])/20*self.tick),(calc(self.posx,width)+2,calc(0,height),26,calc(gridsize,height)-calc(0,height)))
                pygame.draw.rect(screen,(255,255,255),(calc(self.posx,width)+28-self.tick/4,calc(0,height),5,calc(gridsize,height)-calc(0,height)))
        elif(self.turnleft==0):
            #end animation
            if(self.tick==7):return
            self.draw_clear(screen)
            image1=pygame.transform.scale_by(self.image,(0.6*(7-self.tick),0.6*(7-self.tick)))
            screen.blit(image1,(calc(self.posx,width)+16.5-image1.get_width()/2,calc(self.posy,height)+16.2-image1.get_height()/2))
            color1=(170*113/255+self.backgroundcolor[0]*142/255,208*113/255+self.backgroundcolor[1]*142/255,255*113/255+self.backgroundcolor[1]*142/255)
            if(self.posx==-1 or self.posx==gridsize):
                pygame.draw.rect(screen,color1,(calc(0,width),calc(self.posy,height)+15-2*(7-self.tick),calc(gridsize,width)-calc(0,width),4*(7-self.tick)))
                pygame.draw.rect(screen,(170,208,255),(calc(0,width),calc(self.posy,height)+15-1.5*(7-self.tick),calc(gridsize,width)-calc(0,width),3*(7-self.tick)))
                pygame.draw.rect(screen,(255,255,255),(calc(0,width),calc(self.posy,height)+15-0.75*(7-self.tick),calc(gridsize,width)-calc(0,width),1.5*(7-self.tick)))
            else:
                pygame.draw.rect(screen,color1,(calc(self.posx,width)+15-2*(7-self.tick),calc(0,height),4*(7-self.tick),calc(gridsize,height)-calc(0,height)))
                pygame.draw.rect(screen,(170,208,255),(calc(self.posx,width)+15-1.5*(7-self.tick),calc(0,height),3*(7-self.tick),calc(gridsize,height)-calc(0,height)))
                pygame.draw.rect(screen,(255,255,255),(calc(self.posx,width)+15-0.75*(7-self.tick),calc(0,height),1.5*(7-self.tick),calc(gridsize,height)-calc(0,height)))
        else:
            #normal animation
            if(type1==1):
                image1=pygame.transform.scale_by(self.image,(2,2))
                screen.blit(image1,(calc(self.posx,width)+16.5-image1.get_width()/2,calc(self.posy,height)+16.5-image1.get_height()/2))
            if(self.posx==-1 or self.posx==gridsize):
                pygame.draw.rect(screen,(255,255,255),(calc(0,width),calc(self.posy,height)+2,calc(gridsize,width)-calc(0,width),26))
            else:
                pygame.draw.rect(screen,(255,255,255),(calc(self.posx,width)+2,calc(0,height),26,calc(gridsize,height)-calc(0,height)))
    #lancer new tick
    def newtick(self,screen,char):
        if(self.unuse==1):return
        self.tick+=1
        if(self.turnleft<0 or self.turnleft==0 and self.tick==8):
            self.draw_clear(screen)
            self.unuse=1
        if(self.unuse==1):
            return
        self.draw(screen)
    #lancer new turn
    def newturn(self,char):
        if(self.unuse==1):return
        self.turnleft-=1
        self.tick=0
        if(self.turnleft==0):
            self.repaintlist+=self.influence_list
            self.influence_list=[]
            if((char.posx==self.posx or char.posy==self.posy)):
                char.is_hit=1
        
