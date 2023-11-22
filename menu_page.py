import pygame
import time
import random
from init import *
from button import *
from files import *
from game import *

from settings_page import *
from info_page import *
from character_page import *

class Little_characters():
    def __init__(self,char,posx,posy,unlocked):
        if(char==0):self.image=pygame.image.load('assets-raw/sprites/outlined/unit-alpha.png')
        if(char==1):self.image=pygame.image.load('assets-raw/sprites/outlined/unit-mono.png')
        if(char==2):self.image=pygame.image.load('assets-raw/sprites/outlined/unit-oct.png')
        if(char==3):self.image=pygame.image.load('assets-raw/sprites/outlined/unit-crawler.png')
        if(char==4):self.image=pygame.image.load('assets-raw/sprites/outlined/unit-zenith.png')
        if(char==5):self.image=pygame.image.load('assets-raw/sprites/outlined/unit-quad.png')
        if(char==6):self.image=pygame.image.load('assets-raw/sprites/outlined/unit-oxynoe.png')
        if(char==7):self.image=pygame.image.load('assets-raw/sprites/outlined/unit-sei.png')
        self.image=pygame.transform.scale_by(self.image,(1.5,1.5))
        self.image=gen_border(self.image,-1)
        self.unlocked=unlocked
        if(self.unlocked==0):fill(self.image,(150,150,150,0))
        self.movelist=[]
        self.away=0
        self.posx=posx
        global char_dy
        self.posy=posy+char_dy[char]
    #check whether the mouse places in the character
    def collidepoint(self,pos):
        if(pos[0]>=self.posx and pos[0]<=self.posx+self.image.get_width() and pos[1]>=self.posy and pos[1]<=self.posy+self.image.get_height()):
            return 1
        return 0
    #listen
    def listen(self):
        if(len(self.movelist)>0):
            return
        if(self.collidepoint(pygame.mouse.get_pos()) and self.away==0 and self.unlocked==1):
            self.away=1
            self.movelist=[1,3,5,5,3,1,0,-1,-3,-5,-5,-3,-1]
        elif(self.collidepoint(pygame.mouse.get_pos())==0):
            self.away=0
    #draw
    def draw(self,screen):
        screen.blit(self.image,(self.posx,self.posy))
    #newtick
    def newtick(self,screen):
        if(len(self.movelist)>0):
            self.posy+=self.movelist[len(self.movelist)-1]
            self.movelist.pop()
        self.draw(screen)
class Level():
    def __init__(self,screen,left,top,w,h,title,score,music2,music3,backgroundcolor):
        self.left=left
        self.top=top
        self.w=w
        self.h=h
        self.backgroundcolor=backgroundcolor
        self.title=title
        self.on_hover=0
        self.title=title
        self.title_surface=gen_border(pygame.font.Font('assets/font.ttf',28).render(' '+title+' ',True,(255,255,255)))
        self.score_surface=gen_border(pygame.font.Font('assets/font.ttf',28).render(' '+'high score: '+str(score)+' ',True,(135,206,250)))
        self.music1_surface=gen_border(pygame.font.Font('assets/font.ttf',28).render(' '+'Music:'+' ',True,(100,100,100)))
        self.music2_surface=gen_border(pygame.font.Font('assets/font.ttf',28).render(' '+music2+' ',True,(100,100,100)))
        self.music3_surface=gen_border(pygame.font.Font('assets/font.ttf',28).render(' '+music3+' ',True,(100,100,100)))
        if(score==0):
            self.score_surface=gen_border(pygame.font.Font('assets/font.ttf',28).render(' [incomplete] ',True,(100,100,100)))
        self.draw(screen)
    #button level draw
    def draw(self,screen):
        pygame.draw.rect(screen,(self.backgroundcolor.r,self.backgroundcolor.g,self.backgroundcolor.b),(self.left,self.top,self.w,self.h))
        if(self.on_hover==0):
            screen.blit(self.title_surface,(self.left+self.w/2-self.title_surface.get_width()/2,self.top))
            pygame.draw.rect(screen,(135,206,250),(self.left,self.top,self.w,3))
            pygame.draw.rect(screen,(135,206,250),(self.left,self.top,3,self.h))
            pygame.draw.rect(screen,(135,206,250),(self.left+self.w-3,self.top,3,self.h))
            pygame.draw.rect(screen,(135,206,250),(self.left,self.top+self.h-3,self.w,3))
        else:
            screen.blit(self.title_surface,(self.left+self.w/2-self.title_surface.get_width()/2,self.top+10))
            screen.blit(self.score_surface,(self.left+self.w/2-self.score_surface.get_width()/2,self.top+40))
            screen.blit(self.music1_surface,(self.left+self.w/2-self.music1_surface.get_width()/2,self.top+self.h-100))
            screen.blit(self.music2_surface,(self.left+self.w/2-self.music2_surface.get_width()/2,self.top+self.h-70))
            screen.blit(self.music3_surface,(self.left+self.w/2-self.music3_surface.get_width()/2,self.top+self.h-40))
            pygame.draw.rect(screen,(255,255,255),(self.left-3,self.top-3,self.w+6,6))
            pygame.draw.rect(screen,(255,255,255),(self.left-3,self.top-3,6,self.h+6))
            pygame.draw.rect(screen,(255,255,255),(self.left+self.w-3,self.top-3,6,self.h+6))
            pygame.draw.rect(screen,(255,255,255),(self.left-3,self.top+self.h-3,self.w+6,6))
    #check whether the point is in the level button
    def collidepoint(self,pos):
        if(pos[0]>=self.left and pos[0]<=self.left+self.w and pos[1]>=self.top and pos[1]<=self.top+self.h):
            return 1
        return 0
    #change when the mouse is on the level button
    def hover(self,screen):
        if(self.title=='[locked]'):return
        on_hover=0
        if(self.collidepoint(pygame.mouse.get_pos())):
            on_hover=1
        else:
            on_hover=0
        if(self.on_hover==on_hover):return
        
        self.on_hover=on_hover
        self.draw(screen)
        
class Menu_page():
    #draw starting transition
    def draw_transition(self,screen):
        if(self.saving['copper']>=10):self.roll_button=Button(screen,width/2-60,0,120,36,(0,0,0),(135,206,250),'Roll',(255,255,255))
        else:self.roll_button=Button(screen,width/2-60,0,120,36,(50,50,50),(100,100,100),'Roll',(100,100,100))
        start_time=time.time()
        tick=0
        while(1):
            while time.time()-start_time<tick/60:
                pass
            tick+=1
            if(tick>20):return
            self.draw(screen)
            gen_transition(screen,(135,206,250),-tick*height/20)
            pygame.display.flip()
    #draw
    def draw(self,screen,type1=1):
        pygame.draw.rect(screen,(83,104,149),(0,0,width,240))
        self.settings_button.draw(screen,2)
        self.info_button.draw(screen,2)
        self.custom_game_button.draw(screen)
        surface=pygame.transform.scale_by(pygame.image.load('assets-raw/sprites/big-copper.png'),(0.75,0.75))
        screen.blit(surface,(width/2+60,0))
        self.roll_button.draw(screen,3)
        if(self.saving['copper']<10):
            self.roll_button.draw_text(screen,'Roll',(100,100,100))
            surface=pygame.font.Font('assets/font.ttf',32).render(' '+str(self.saving['copper'])+'/10',True,pygame.Color(204,0,0))
        else:
            self.roll_button.draw_text(screen,'Roll',(184+(math.sin(self.tick/20)+1)/2*(255-184),115+(math.sin(self.tick/20)+1)/2*(255-115),51+(math.sin(self.tick/20)+1)/2*(255-51)))
            surface=pygame.font.Font('assets/font.ttf',32).render(' '+str(self.saving['copper'])+'/10',True,pygame.Color(255,255,255))
        gen_border(surface)
        screen.blit(surface,(width/2+90,2))
        for i in range(5):
            if(self.levels[i].on_hover==0):self.levels[i].draw(screen)
        for i in range(5):
            if(self.levels[i].on_hover==1):self.levels[i].draw(screen)
        if(type1==0):
            return
        for i in range(8):
            self.little_characters[i].newtick(screen)
        pygame.display.flip()
    def handlelevels(self,screen):
        self.levels=[]
        flag=0
        self.levels.append(Level(screen,0,240,180,360,'Map 1',self.saving['score'][0],'Aritus - For You','',pygame.Color("#90ee90")))
        if(self.saving['score'][0]==0):flag=1
        if(flag==0):self.levels.append(Level(screen,180,240,180,360,'Map 2',self.saving['score'][1],'PYC - Stoplight','',pygame.Color("#2b174d")))
        else:self.levels.append(Level(screen,180,240,180,360,'[locked]',self.saving['score'][1],'PYC - Stoplight','',pygame.Color("#2b174d")))
        if(self.saving['score'][1]==0):flag=1
        if(flag==0):self.levels.append(Level(screen,360,240,180,360,'Map 3',self.saving['score'][2],'Kepter\'s Room -','Bright 79',pygame.Color("#a886e9")))
        else:self.levels.append(Level(screen,360,240,180,360,'[locked]',self.saving['score'][2],'Kepter\'s Room -','Bright 79',pygame.Color("#a886e9")))
        if(self.saving['score'][2]==0):flag=1
        if(flag==0):self.levels.append(Level(screen,540,240,180,360,'Map 4',self.saving['score'][3],'Aritus - ','Pina Colada II',pygame.Color("#0d091d")))
        else:self.levels.append(Level(screen,540,240,180,360,'[locked]',self.saving['score'][3],'Aritus - ','Pina Colada II',pygame.Color("#0d091d")))
        if(self.saving['score'][3]==0):flag=1
        if(flag==0):self.levels.append(Level(screen,720,240,180,360,'Map 5',self.saving['score'][4],'ADRIANWAVE - ','Peach Beach',pygame.Color("#fa712c")))
        else:self.levels.append(Level(screen,720,240,180,360,'[locked]',self.saving['score'][4],'ADRIANWAVE - ','Peach Beach',pygame.Color("#fa712c")))
    def __init__(self,screen,saving):
        pygame.mixer.Channel(0).set_volume(saving['settings']['music_volume']/100)
        pygame.mixer.Channel(0).play(pygame.mixer.Sound('assets/sounds/back.ogg'))
        self.saving=saving
        self.little_characters=[]
        for i in range(8):
            if((saving['unlocked']&(1<<i))>0):self.little_characters.append(Little_characters(i,width/2-160+i*40,175,1))
            else:self.little_characters.append(Little_characters(i,width/2-160+i*40,175,0))

        self.settings_button=Button(screen,0,0,50,50,(0,0,0),(135,206,250))
        self.settings_button.text_surface=pygame.image.load('assets-raw/sprites/outlined/settings.png')
        self.settings_button.text_surface=pygame.transform.scale_by(self.settings_button.text_surface,(1.5,1.5))

        self.info_button=Button(screen,width-50,0,50,50,(0,0,0),(135,206,250))
        self.info_button.text_surface=pygame.image.load('assets-raw/sprites/outlined/info.png')
        self.info_button.text_surface=pygame.transform.scale_by(self.info_button.text_surface,(1.5,1.5))

        self.custom_game_button=Button(screen,width-120,240-36,120,36,(0,0,0),(135,206,250),'custom game')
        
        if(self.saving['copper']>=10):self.roll_button=Button(screen,width/2-60,0,120,36,(0,0,0),(135,206,250),'Roll',(255,255,255))
        else:self.roll_button=Button(screen,width/2-60,0,120,36,(50,50,50),(100,100,100),'Roll',(100,100,100))
        self.handlelevels(screen)

        
        
        self.start_time=time.time()
        self.tick=0
        while(1):
            if(self.saving['score'][0]==0 and self.tick==0):
                draw_transition_end(screen)
                info_page=Info_page(screen)
                self.draw_transition(screen)
                self.back(screen)
            while time.time()-self.start_time<self.tick/60:
                for i in range(8):
                    self.little_characters[i].listen()
                pass
            self.tick+=1
            self.draw(screen)
            self.listen(screen)
            pygame.display.flip()
    def back(self,screen):
        pygame.mixer.Channel(0).set_volume(self.saving['settings']['music_volume']/100)
        pygame.mixer.Channel(0).play(pygame.mixer.Sound('assets/sounds/back.ogg'))
        if(self.saving['copper']>=10):self.roll_button=Button(screen,width/2-60,0,120,36,(0,0,0),(135,206,250),'Roll',(255,255,255))
        else:self.roll_button=Button(screen,width/2-60,0,120,36,(50,50,50),(100,100,100),'Roll',(100,100,100))
    #listen
    def listen(self,screen):
        self.settings_button.hover(screen,2)
        self.info_button.hover(screen,2)
        self.custom_game_button.hover(screen)
        if(self.saving['copper']>=10):self.roll_button.hover(screen)
        for i in range(5):
            self.levels[i].hover(screen)
        for i in range(8):
            self.little_characters[i].listen()
        for event in pygame.event.get():
            if(event.type==pygame.QUIT):
                save_saving()
                pygame.quit()
                exit()
            if(event.type==pygame.MOUSEBUTTONDOWN):
                for i in range(5):
                    if(self.levels[i].collidepoint(event.pos) and (i==0 or self.saving['score'][i-1]>0)):
                        draw_transition_end(screen)
                        start_time=time.time()
                        newgame(screen,'levels/level'+str(i+1)+'.json',self.saving)
                        self.draw_transition(screen)
                        endgame()
                        self.start_time+=time.time()-start_time
                        self.handlelevels(screen)
                        self.back(screen)
                for i in range(8):
                    if(self.little_characters[i].collidepoint(event.pos) and self.little_characters[i].unlocked==1):
                        start_time=time.time()
                        character_page=Character_page(screen,self.saving,i+1)
                        self.draw_transition(screen)
                        character_page=None
                        self.start_time+=time.time()-start_time
                        self.back(screen)
                if(self.custom_game_button.collidepoint(event.pos)):
                    start_time=time.time()
                    print('ok')
                    filepath=tkinter.filedialog.askopenfilename(filetypes=[('JSON','*.json')])
                    if(filepath.strip()==''):continue
                    tmp=readlevel(screen,filepath)
                    if(tmp==None):continue
                    draw_transition_end(screen)
                    newgame(screen,filepath,self.saving)
                    endgame()
                    self.draw_transition(screen)
                    self.start_time+=time.time()-start_time
                    self.back(screen)
                if(self.settings_button.collidepoint(event.pos)):
                    start_time=time.time()
                    draw_transition_end(screen)
                    settings_page=Settings_page(screen,self.saving)
                    self.draw_transition(screen)
                    settings_page=None
                    self.start_time+=time.time()-start_time
                    self.back(screen)
                if(self.info_button.collidepoint(event.pos)):
                    start_time=time.time()
                    draw_transition_end(screen)
                    info_page=Info_page(screen)
                    self.draw_transition(screen)
                    info_page=None
                    self.start_time+=time.time()-start_time
                    self.back(screen)
                if(self.roll_button.collidepoint(event.pos) and self.saving['copper']>=10):
                    self.saving['copper']-=10
                    char=random.randint(2,8)
                    self.saving['unlocked']=self.saving['unlocked']|(1<<(char-1))
                    save_saving()
                    start_time=time.time()
                    character_page=Character_page(screen,self.saving,char,1)
                    self.draw_transition(screen)
                    character_page=None
                    self.little_characters=[]
                    for i in range(8):
                        if((self.saving['unlocked']&(1<<i))>0):self.little_characters.append(Little_characters(i,width/2-160+i*40,175,1))
                        else:self.little_characters.append(Little_characters(i,width/2-160+i*40,175,0))
                    self.start_time+=time.time()-start_time
                    self.back(screen)
                
                    
                    
        
        
