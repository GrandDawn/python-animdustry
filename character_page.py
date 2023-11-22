import pygame
import time
import math
import random
from init import *
from button import *
from files import *
orange_background=(196,87,25)
purple_background=(78,81,128)
green_background=(1,163,104) #(1,106,78)
class Little_shapes():
    #create circle
    def gen_circle(self,color):
        sz=(int)(random.uniform(10,30))
        ans=pygame.Surface((sz+1,sz+1)).convert_alpha()
        for x in range(sz+1):
            for y in range(sz+1):
                dist=round(((x-sz/2)**2+(y-sz/2)**2)**0.5)
                if(dist<=sz/3):
                    ans.set_at((x,y),(255+(color[0]-255)*dist/sz,255+(color[1]-255)*dist/sz,255+(color[2]-255)*dist/sz,255))
                elif(dist<=sz/2):
                    ans.set_at((x,y),(255+(color[0]-255)/2,255+(color[1]-255)/2,255+(color[2]-255)/2,255-255/(sz/6)*(dist-sz/3)))
                else:
                    ans.set_at((x,y),(255,255,255,0))
        return ans
    #create square(unused)
    def gen_square(self,color):
        sz=(int)(random.uniform(8,20))
        ans=pygame.Surface((sz+1,sz+1)).convert_alpha()
        for x in range(sz+1):
            for y in range(sz+1):
                dist=max(abs((x-sz/2)),abs(y-sz/2))
                if(dist<=sz/3):
                    ans.set_at((x,y),(255+(color[0]-255)*dist/sz,255+(color[1]-255)*dist/sz,255+(color[2]-255)*dist/sz,255))
                elif(dist<=sz/2):
                    ans.set_at((x,y),(255+(color[0]-255)/2,255+(color[1]-255)/2,255+(color[2]-255)/2,255-255/(sz/6)*(dist-sz/3)))
                else:
                    ans.set_at((x,y),(255,255,255,0))
        return ans
    #return p(t)
    def query_position(self,tick):
        return ((self.posx+self.dx*tick)%width-self.surface.get_width()/2,(self.posy+self.dy*tick)%height-self.surface.get_height()/2)
    #shapes draw
    def draw(self,screen,tick):
        screen.blit(self.surface,self.query_position(tick))
    def __init__(self,char):
        if(char==1 or char==5 or char==8):
            self.surface=self.gen_circle(orange_background)
        elif(char==4):
            self.surface=self.gen_circle(purple_background)
        else:
            self.surface=self.gen_circle(green_background)
        self.posx=random.uniform(0,width)
        self.posy=random.uniform(0,height)
        degree=random.uniform(0,math.pi)
        self.dx=math.sin(degree)/5
        self.dy=math.cos(degree)/5
            
class Character_page():
    #draw roll animation
    def roll_animation(self,screen,saving,char):
        pygame.mixer.Channel(0).set_volume(saving['settings']['music_volume']/100)
        pygame.mixer.Channel(0).play(pygame.mixer.Sound('assets/music/reveal.ogg'))
        
        start_time=time.time()
        tick=0
        image1=self.image.copy()
        fill(image1,(100,100,100,0))
        ticknum=180
        while(1):
            while time.time()-start_time<tick/60:
                pass
            tick+=1
            for i in range(5,-1,-1):
                sz=100*i+(tick*10)%100
                pygame.draw.rect(screen,(135,206,250),(width/2-sz,height/2-sz,2*sz,2*sz))
                sz=sz-i*20
                pygame.draw.rect(screen,(83,104,149),(width/2-sz,height/2-sz,2*sz,2*sz))
            if(tick>=ticknum-20):
                sz=(tick-ticknum+20)*(tick-ticknum+20)/400
                image=pygame.transform.scale_by(image1,(sz,sz))
                screen.blit(image,(width/2-image.get_width()/2,height/2-image.get_height()/2))
            pygame.display.flip()
            if(tick>=ticknum):break
    #draw transition begin
    def draw_transition(self,screen,char):
        start_time=time.time()
        tick=0
        while(1):
            while time.time()-start_time<tick/60:
                pass
            tick+=1
            if(tick>20):return
            self.back_button=Button(screen,20,height-20-36,80,36,(0,0,0),(135,206,250),'back')
            self.draw(screen,char,2-tick*0.05)                
            pygame.display.flip()
    #generate character shadow
    def gen_shadow(self,surface):
        lst=[]
        w,h=surface.get_size()
        param=8
        for i in range(w):
            for j in range(h):
                if(i+param<w and j-param>=0):
                    if(surface.get_at((i,j)).a!=0):
                        continue
                    if(surface.get_at((i+param,j-param)).a!=0):
                        lst.append([i,j])
        for i in lst:
            surface.set_at((i[0],i[1]),(50,50,50,128))
        return surface
    #processing sei
    def func8(self,surface):
        w,h=surface.get_size()
        for i in range(w):
            for j in range(h):
                if(surface.get_at((i,j)).r<=200 and surface.get_at((i,j)).g<=200 and surface.get_at((i,j)).b<=200):
                    surface.set_at((i,j),(255,255,255,0))
                if(surface.get_at((i,j)).a==255):
                    a=surface.get_at((i,j))
                    surface.set_at((i,j),(a.r,a.g,a.b,192))
        return surface
    #character draw
    def draw(self,screen,char,size=1):
        image=pygame.transform.scale_by(self.image,(size,size))
        if(char==1 or char==5 or char==8):
            screen.fill(orange_background)
        elif(char==4):
            screen.fill(purple_background)
        else:
            screen.fill(green_background)
        for i in self.little_shapes:
            i.draw(screen,self.tick)
        if(char!=4 and char!=6 and char!=7):
            screen.blit(image,(width/2-image.get_width()/2,height/2+20-image.get_height()/2+math.sin(self.tick/20)*5))
        else:
            screen.blit(image,(width/2-image.get_width()/2,height/2+20-image.get_height()/2))
        if(char==5):
            image1=pygame.transform.scale_by(self.image1,(size,size))
            screen.blit(image1,(width/2-image1.get_width()/2,height/2-image1.get_height()/2-math.sin(self.tick/20)*5))
            image2=pygame.transform.scale_by(self.image2,(size,size))
            screen.blit(image2,(width/2-image2.get_width()/2,height/2-image2.get_height()/2+math.sin((self.tick+3)/20)*5))
        if(size!=1):
            return
        if(char==2):
            screen.blit(self.image1,(width/2-self.image.get_width()/2,height/2-self.image.get_height()/2+163+math.sin(self.tick/20)*5))
        elif(char==6):
            screen.blit(self.image1,(width/2-self.image.get_width()/2,height/2+20-self.image.get_height()/2))
        elif(char==7):
            screen.blit(self.image1,(width/2-self.image.get_width()/2,height/2+160-self.image.get_height()/2))
        elif(char==8):
            screen.blit(self.image1,(width/2-self.image.get_width()/2+150,height/2-self.image.get_height()/2+20+math.sin(self.tick/20-math.pi/3)*5))
        self.back_button.draw(screen)
        for i in range(len(self.skill_description_surface)):
            screen.blit(self.skill_description_surface[i],(width-10-self.skill_description_surface[i].get_width(),height-10-22*(len(self.skill_description_surface)-i)))
        for i in range(len(self.title_surface)):
            sz=0.5+min(180,self.tick)/360
            sz=-2*((sz-1)**2)+1
            screen.blit(self.title_surface[i],(width/2-20+(i-(len(self.title_surface)-1)/2)*60*sz,10))
        screen.blit(self.title_description_surface,(width/2-self.title_description_surface.get_width()/2,40))
        pygame.display.flip()
    def __init__(self,screen,saving,char,roll=0):
        #load all images
        if(char==1):
            self.image=self.gen_shadow(pygame.transform.scale_by(pygame.image.load('assets/textures/alpha.png'),(0.28,0.28)))
            self.title='ALPHA'
            self.title_description='the first of many'
            self.skill_description=['creates a wall every 10 moves']
        if(char==2):
            self.image=self.gen_shadow(pygame.transform.scale_by(pygame.image.load('assets/textures/mono.png'),(0.28,0.28)))
            self.image1=pygame.transform.scale_by(pygame.image.load('assets/textures/mono-glow.png'),(0.28,0.28))
            self.title='MONO'
            self.title_description='the gatherer'
            self.skill_description=['earns one extra point every 4 moves']
        if(char==3):
            self.image=self.gen_shadow(pygame.transform.scale_by(pygame.image.load('assets/textures/oct.png'),(0.25,0.25)))
            self.title='OCT'
            self.title_description='the protector'
            self.skill_description=['creates a shield every 30 moves']
        if(char==4):
            self.image=self.gen_shadow(pygame.transform.scale_by(pygame.image.load('assets/textures/crawler.png'),(0.28,0.28)))
            self.title='CRAWLER'
            self.title_description='boom'
            self.skill_description=['destroys 4 adjacent blocks every 4','moves']
        if(char==5):
            self.image=self.gen_shadow(pygame.transform.scale_by(pygame.image.load('assets/textures/zenith.png'),(0.28,0.28)))
            self.image1=self.gen_shadow(pygame.transform.scale_by(pygame.image.load('assets/textures/zenith-wowitos.png'),(0.28,0.28)))
            self.image2=self.gen_shadow(pygame.transform.scale_by(pygame.image.load('assets/textures/zenith-controller.png'),(0.28,0.28)))
            self.title='ZENITH'
            self.title_description='gaming'
            self.skill_description=['destroys the next 4 blocks in a line','every 4 moves']
        if(char==6):
            self.image=self.gen_shadow(pygame.transform.scale_by(pygame.image.load('assets/textures/quad.png'),(0.28,0.28)))
            self.image1=pygame.transform.scale_by(pygame.image.load('assets/textures/quad-energy.png'),(0.28,0.28))
            self.title='QUAD'
            self.title_description='the "support" has arrived'
            self.skill_description=['destroys 8 adjacent blocks every 6','moves']
        if(char==7):
            self.image=self.gen_shadow(pygame.transform.scale_by(pygame.image.load('assets/textures/oxynoe.png'),(0.28,0.28)))
            self.image1=pygame.transform.scale_by(pygame.image.load('assets/textures/oxynoe-flame.png'),(0.28,0.28))
            self.title='OXYNOE'
            self.title_description='as was foretold'
            self.skill_description=['gain one bot move every 4 moves']
        if(char==8):
            self.image=self.gen_shadow(pygame.transform.scale_by(pygame.image.load('assets/textures/sei.png'),(0.28,0.28)))
            self.image1=self.func8(pygame.transform.scale_by(pygame.image.load('assets/textures/sei-missiles.png'),(0.28,0.28)))
            self.title='SEI'
            self.title_description='crossed out'
            self.skill_description=['destroys blocks in a diagonal cross','every 4 moves']
        self.skill_description_surface=[]
        for i in self.skill_description:
            self.skill_description_surface.append(gen_border(pygame.font.Font('assets/font.ttf',25).render(' '+i,True,(255,255,255))))
        self.title_description_surface=gen_border(pygame.font.Font('assets/font.ttf',25).render(' '+self.title_description,True,(255,255,255)))
        self.title='-'+self.title+'-'
        self.title_surface=[]
        for i in range(len(self.title)):
            tmp=gen_border(pygame.font.Font('assets/title.ttf',40).render(' '+self.title[i],True,(255,255,255)))
            self.title_surface.append(pygame.transform.scale_by(tmp,(1,1)))
        self.little_shapes=[]
        for i in range(40):
            self.little_shapes.append(Little_shapes(char))
        
        self.back_button=Button(screen,20,height-20-36,80,36,(0,0,0),(135,206,250),'back')
        if(roll==1):
            self.roll_animation(screen,saving,char)
            pygame.mixer.Channel(1).set_volume(saving['settings']['music_volume']/100)
            pygame.mixer.Channel(1).play(pygame.mixer.Sound('assets/music/get.ogg'))
        else:
            pygame.mixer.Channel(1).set_volume(saving['settings']['music_volume']/100)
            pygame.mixer.Channel(1).play(pygame.mixer.Sound('assets/music/view.ogg'))
        
        self.tick=0
        self.draw_transition(screen,char)
        start_time=time.time()
        self.draw(screen,char)
        while(1):
            while time.time()-start_time<self.tick/60:
                pass
            self.tick+=1
            self.draw(screen,char)
            while(self.listen(screen)==1):
                return
    #listen movements
    def listen(self,screen):
        self.back_button.hover(screen)
        for event in pygame.event.get():
            if(event.type==pygame.QUIT):
                save_saving()
                pygame.quit()
                exit()
            if(event.type==pygame.KEYDOWN):
                if(event.key==pygame.K_ESCAPE):
                    draw_transition_end(screen)
                    return 1
            if(event.type==pygame.MOUSEBUTTONDOWN):
                if(self.back_button.collidepoint(event.pos)):
                    draw_transition_end(screen)
                    return 1
                
                    
                    
        
        
