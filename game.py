import pygame
import time
import math
from init import *
from obstacles import *
from button import *
from character import *
from files import *
from bot import *
class Grid():
    #paint row:posx column:posy
    def paint(self,posx,posy):
        global obstacles
        if(posx>=gridsize or posx<0 or posy>=gridsize or posy<0):
            pygame.draw.rect(self.screen,self.backgroundcolor,(calc(posx,width)-3,calc(posy,height)-3,39,39))
            return
        if(posx>=gridsize or posx<0 or posy>=gridsize or posy<0):
            return
        if([posx,posy] in obstacles.influence_list):
            return
        pygame.draw.rect(self.screen,self.backgroundcolor,(calc(posx,width)-3,calc(posy,height)-3,39,39))
        fill(self.tile,self.grid[int(posx)][int(posy)])
        self.screen.blit(self.tile,(calc(posx,width),calc(posy,height)))
    def __init__(self,screen,backgroundcolor,color,color2):
        self.screen=screen
        self.movelist=[]
        self.tile=pygame.image.load('assets-raw/sprites/tile.png')
        self.tile=pygame.transform.scale_by(self.tile,(1.5,1.5))
        self.color=color
        self.backgroundcolor=backgroundcolor
        self.color2=color2
        self.grid=[]
        for i in range(gridsize):
            lst=[]
            for j in range(gridsize):
                lst.append(self.color)
            self.grid.append(lst)
    #paint all grid first
    def draw_init(self):
        self.repaintlist=[]
        self.screen.fill(self.backgroundcolor)
        for i in range(0,gridsize):
            for j in range(0,gridsize):
                self.paint(i,j)
                self.repaintlist.append([i,j])
    #grid newtick
    def newtick(self,type1=0):
        #repaint the shining grids and store into repaintlist
        self.repaintlist=[]
        leng=len(self.movelist)
        if(leng>0):
            for i in self.movelist[leng-1]:
                self.repaintlist.append(i)
                self.grid[i[0]][i[1]]=self.color
                self.paint(i[0],i[1])
            self.movelist.pop()
        for i in char.repaintlist:
            self.repaintlist.append(i)
            self.paint(i[0],i[1])
        for i in obstacles.repaintlist:
            self.repaintlist.append(i)
            self.paint(i[0],i[1])
        tmp=[]
        for i in self.repaintlist:
            if i not in tmp:
                tmp.append(i)
        self.repaintlist=tmp
    #grid newturn
    def newturn(self,turn):
        lst=[]
        for i in range(0,gridsize):
            for j in range(0,gridsize):
                if((abs(i-gridsize/2+0.5)+abs(j-gridsize/2+0.5))%5==turn%5):
                    self.grid[i][j]=self.color2
                    self.paint(i,j)
                    lst.append([i,j])
        self.movelist.append(lst)
        self.movelist.append([])
        self.movelist.append([])
        self.movelist.append([])
        self.movelist.append([])
        self.movelist.append([])
class Maingame():
    #draw score on the top-left
    def drawscore(self):
        text=str(self.score)
        while len(text)<4:
            text='0'+text
        text_surface=pygame.font.Font('assets/font.ttf',28).render(' ['+text+']',True,pygame.Color(255,255,255))
        gen_border(text_surface)
        pygame.draw.rect(self.screen,grid.backgroundcolor,(10,10,75,25))
        self.screen.blit(text_surface,(10,10))
    #draw progress bar on the top
    def drawprogress(self):
        pygame.draw.rect(self.screen,grid.backgroundcolor,(width/2-self.progress.get_width()/2,10,self.progress.get_width(),self.progress.get_height()))
        self.screen.blit(self.progress,(width/2-self.progress.get_width()/2,10))
        ratio=self.turn/self.turn_limit
        ratio=min(ratio,1.0)
        self.screen.blit(self.progresstick,(width/2-self.progress.get_width()/2-self.progresstick.get_width()/2+4+ratio*(self.progress.get_width()-8),10))
    #draw health on the top-right
    def drawhealth(self):
        pygame.draw.rect(self.screen,grid.backgroundcolor,(width-60,0,60,60))
        image1=self.health_image.copy()
        tmp=math.sin(math.pi/15*(char.hit_animation-22.5))/2+1/2
        if(char.hit_animation==0):tmp=0
        fill(image1,(135*(1-tmp)+255*tmp,206*(1-tmp),250*(1-tmp),255))
        image1=pygame.transform.scale_by(image1,(1+tmp/4,1+tmp/4))
        image1=gen_border(image1)
        self.screen.blit(image1,(width-self.health_image.get_width()/2-10-image1.get_width()/2,10+self.health_image.get_height()/2-image1.get_height()/2))
        text_surface=pygame.font.Font('assets/font.ttf',28).render(' '+str(self.health),True,pygame.Color(255,255,255))
        gen_border(text_surface)
        self.screen.blit(text_surface,(width-self.health_image.get_width()/2-text_surface.get_width()/2-10,11))
    def drawbotmove(self):
        pygame.draw.rect(self.screen,grid.backgroundcolor,(width-150,height-50,150,50))
        surface=pygame.font.Font('assets/font.ttf',25).render(' Bot Moves:'+str(self.bot_move),True,pygame.Color(255,255,255))
        surface=gen_border(surface)
        self.screen.blit(surface,(width-10-surface.get_width(),height-10-surface.get_height()))
    def drawabove(self):
        self.drawscore()
        self.drawprogress()
        self.drawhealth()
        self.drawbotmove()
    #draw characters list
    def drawbelow(self):
        for i in range(len(self.char_list)):
            if(self.char_list[i]==0):image=pygame.image.load('assets-raw/sprites/outlined/unit-alpha.png')
            if(self.char_list[i]==1):image=pygame.image.load('assets-raw/sprites/outlined/unit-mono.png')
            if(self.char_list[i]==2):image=pygame.image.load('assets-raw/sprites/outlined/unit-oct.png')
            if(self.char_list[i]==3):image=pygame.image.load('assets-raw/sprites/outlined/unit-crawler.png')
            if(self.char_list[i]==4):image=pygame.image.load('assets-raw/sprites/outlined/unit-zenith.png')
            if(self.char_list[i]==5):image=pygame.image.load('assets-raw/sprites/outlined/unit-quad.png')
            if(self.char_list[i]==6):image=pygame.image.load('assets-raw/sprites/outlined/unit-oxynoe.png')
            if(self.char_list[i]==7):image=pygame.image.load('assets-raw/sprites/outlined/unit-sei.png')
            image=gen_border(image)
            if(char.type==self.char_list[i]):fill_darker(image)
            self.screen.blit(image,(22*i,height-40+char_dy[self.char_list[i]]))
            surface=pygame.font.Font('assets/font.ttf',25).render(str(i+1),True,pygame.Color(255,255,255))
            surface=gen_border(surface)
            self.screen.blit(surface,(22*i+5,height-25))
        
    #play music
    def playmusic(self):
        pygame.mixer.music.load(self.level['music'])
        pygame.mixer.music.set_volume(self.saving['settings']['music_volume']/100)
        pygame.mixer.music.play()
    #handle a new turn
    def newturn(self):
        self.turn+=1
        if(self.bot_on==1 and self.bot_move>0):
            bot=Bot(obstacles,self.turn-1)
            char.move(self,bot.calc([char.posx,char.posy],char.lastmove))
            self.bot_move-=1
            maingame.drawbotmove()
        if(self.bot_move==0):self.bot_on=0
        grid.newturn(self.turn)
        obstacles.newturn(char,self.turn)
        char.newturn()
    #handle a new tick
    def newtick(self):
        grid.newtick()
        #start_time=time.time()
        obstacles.newtick(char,grid.repaintlist)
        #print(time.time()-start_time)
        char.newtick(self.screen,self)
        
        self.drawprogress()
        if(char.hit_animation>=15):self.drawhealth()
        pygame.display.flip()
        self.listen_in_game()
    #redraw the screen before pausing/ending
    def draw(self):
        grid.draw_init()
        obstacles.repaint(grid.repaintlist)
        char.draw(self.screen,self)
        self.drawabove()
        self.drawbelow()
    #startgame
    def start(self):
        self.progress=pygame.image.load('assets-raw/sprites/outlined/progress.png')
        self.progress=pygame.transform.scale_by(self.progress,(2,2))
        self.progresstick=pygame.image.load('assets-raw/sprites/outlined/progress-tick.png')
        self.progresstick=pygame.transform.scale_by(self.progresstick,(2,2))
        self.health_image=pygame.image.load('assets-raw/sprites/outlined/health.png')
        
        self.health_image=pygame.transform.scale_by(self.health_image,(1.5,1.5))
    #end
    def end(self):
        pygame.mixer.music.load('assets/sounds/win.ogg')
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play()
        self.draw()
        self.score=max(self.score,1)
        copper=0
        if('copper' in self.level):
            for j in range(1,21):
                if(hash_md5('copper'+str(j)+'copper')==self.level['copper']):copper=j
        if(copper>0):copper+=(int)(math.log(self.score,5))
        
        level=-1
        with open(self.levelpath,'r') as f:
            md5=hash_md5(f.read())
        if(md5=='8322f8f96e730633e09a6da93788b83b'):level=0
        if(md5=='a9a8b39808871a8d3901353b4898de68'):level=1
        if(md5=='d10ebf83072ff94dfc2a115101be1d45'):level=2
        if(md5=='90d00788c771c50160a94a02bddce4c2'):level=3
        if(md5=='c2ed0fcbdb777a2ea903d825c2fb32bb'):level=4
        if(level!=-1):
            if(self.saving['score'][level]==0):copper+=10
            self.saving['score'][level]=max(self.score,self.saving['score'][level])
            self.saving['copper']+=copper
        else:copper=0
        for i in range(1,5):
            start_time=time.time()
            #border
            surface=gen_rhombus((grid.backgroundcolor[0]/2,grid.backgroundcolor[1]/2,grid.backgroundcolor[2]/2,i*16),(135,206,250,i*64-1))
            self.screen.blit(surface,(width/2-180,height/2-180))
            #content
            surface=pygame.font.Font('assets/font.ttf',35).render(' [level complete!]',True,pygame.Color(135,206,250,i*64-1))
            gen_border(surface)
            self.screen.blit(surface,(width/2-surface.get_width()/2,height/2-surface.get_height()/2-33))
            surface=pygame.font.Font('assets/font.ttf',35).render('final score: '+str(self.score),True,pygame.Color(135,206,250,i*64-1))
            gen_border(surface)
            self.screen.blit(surface,(width/2-surface.get_width()/2,height/2-surface.get_height()/2-6))
            
            surface=pygame.transform.scale_by(pygame.image.load('assets-raw/sprites/outlined/copper.png'),(1.5,1.5))
            gen_border(surface)
            self.screen.blit(surface,(width/2-surface.get_width()/2-15,height/2-surface.get_height()/2+21))
            surface=pygame.font.Font('assets/font.ttf',32).render('+'+str(copper),True,pygame.Color(184,115,51,i*64-1))
            gen_border(surface)
            self.screen.blit(surface,(width/2,height/2-surface.get_height()/2+21))
            
            self.button_menu=Button(self.screen,width/2-60,height/2-21+60,120,36,(0,0,0,255),(135,206,250,i*64-1),'Menu')
            while time.time()-start_time<1/self.fps:
                pass
            pygame.display.flip()
    #fail
    def fail(self):
        pygame.mixer.music.load('assets/sounds/die.ogg')
        pygame.mixer.music.set_volume(self.saving['settings']['sound_effect_volume']/100)
        pygame.mixer.music.play()
        self.draw()
        for i in range(1,5):
            start_time=time.time()
            #border
            surface=gen_rhombus((grid.backgroundcolor[0]/2,grid.backgroundcolor[1]/2,grid.backgroundcolor[2]/2,i*16),(135,206,250,i*64-1))
            self.screen.blit(surface,(width/2-180,height/2-190))
            #content
            surface=pygame.font.Font('assets/font.ttf',35).render(' [level failed!]',True,pygame.Color(250,0,0,i*64-1))
            gen_border(surface)
            self.screen.blit(surface,(width/2-surface.get_width()/2,height/2-surface.get_height()/2-33))

            self.button_retry=Button(self.screen,width/2-60,height/2-21+14,120,36,(0,0,0,255),(135,206,250,i*64-1),'Retry')
            
            self.button_menu=Button(self.screen,width/2-60,height/2-21+56,120,36,(0,0,0,255),(135,206,250,i*64-1),'Menu')

            while time.time()-start_time<1/self.fps:
                pass
            pygame.display.flip()
    def pause(self):
        if(self.inpause==1):
            #unpause
            pygame.mixer.Channel(0).set_volume(self.saving['settings']['sound_effect_volume']/100)
            pygame.mixer.Channel(0).play(pygame.mixer.Sound('assets/sounds/unpause.ogg'))
            self.draw()
            pygame.mixer.music.unpause()
            self.pausetime=time.time()-self.pausetime
            self.inpause=0
            return
        #pause
        pygame.mixer.Channel(0).set_volume(self.saving['settings']['sound_effect_volume']/100)
        pygame.mixer.Channel(0).play(pygame.mixer.Sound('assets/sounds/pause.ogg'))
        pygame.mixer.music.pause()
        self.pausetime=time.time()
        self.inpause=1
        self.draw()
        for i in range(1,5):
            start_time=time.time()
            #border
            surface=gen_rhombus((grid.backgroundcolor[0]/2,grid.backgroundcolor[1]/2,grid.backgroundcolor[2]/2,i*16),(135,206,250,i*64-1))
            self.screen.blit(surface,(width/2-180,height/2-180))
            #content
            surface=pygame.font.Font('assets/font.ttf',35).render(' [paused]',True,pygame.Color(255,255,255,i*64-1))
            gen_border(surface)
            self.screen.blit(surface,(width/2-surface.get_width()/2,height/2-surface.get_height()/2-33))

            self.button_retry=Button(self.screen,width/2-60,height/2-21+14,120,36,(0,0,0,255),(135,206,250,i*64-1),'Retry')
            
            self.button_menu=Button(self.screen,width/2-60,height/2-21+56,120,36,(0,0,0,255),(135,206,250,i*64-1),'Menu')
            
            while time.time()-start_time<1/self.fps:
                pass
            pygame.display.flip()
    def __init__(self,screen,levelpath,level,saving):
        self.levelpath=levelpath
        self.screen=screen
        self.level=level
        self.saving=saving
        self.inpause=0
        self.pausetime=0
        self.score=0
        self.tick=0
        self.turn=0
        self.fps=60
        self.bot_move=0
        self.above_change=[0,0,0]
        self.bot_on=0
        self.char_list=[]
        for i in range(8):
            if((saving['unlocked']&(1<<i))>0):
                self.char_list.append(i)
        self.health=level['health']
        self.bpm=level['bpm']
        self.turn_limit=level['turn_limit']
    #draw the starting transition
    def draw_transition_begin(self,screen):
        start_time=time.time()
        tick=0
        while(1):
            while time.time()-start_time<tick/60:
                pass
            tick+=1
            if(tick>20):return

            pygame.draw.rect(screen,grid.backgroundcolor,(0,height-tick*height/20,width,height/20))
            if(tick<=2):self.drawbelow()
                
            for i in range(gridsize):
                for j in range(gridsize):
                    if(calc(j,height)+36<height-tick*height/20 or calc(j,height)-2>height-(tick-1)*height/20):
                        pass
                    else:
                        grid.paint(i,j)
            char.draw(self.screen,self)
            if(tick>=19):self.drawabove()
            gen_transition(screen,(135,206,250),-tick*height/20)
            pygame.display.flip()
    #mainggame
    def game(self):
        self.start()
        self.draw_transition_begin(self.screen)
        grid.draw_init()
        self.drawabove()
        self.drawbelow()
        music_on=0
        
        offset=self.level['beat_offset']+self.saving['settings']['judgement_offset']/1000
        if(offset>=0):
            self.playmusic()
            time.sleep(offset)
            music_on=1
        start_time=time.time()
        while(1):
            if(self.inpause==1):
                time.sleep(0.017)
                tmp=self.listen_pause()
                if(tmp==1 or tmp==2):return tmp
                continue
            start_time+=self.pausetime
            self.pausetime=0
            self.tick+=1
            while time.time()-start_time<self.tick/self.fps:
                pass
            if(music_on==0 and abs(time.time()-start_time+offset)<0.01):
                self.playmusic()
                music_on=1
            if((self.turn+1)*(60*self.fps/self.bpm)<self.tick):
                self.newturn()
            self.newtick()
            if(self.turn>=self.turn_limit):
                self.end()
                break
            if(self.health<=0):
                self.fail()
                break
        save_saving()
        while(1):
            tmp=self.listen_exit()
            if(tmp==1 or tmp==2):return tmp
    #listen when pausing
    def listen_pause(self):
        if(hasattr(self,'button_menu')):
            self.button_menu.hover(self.screen)
        if(hasattr(self,'button_retry')):
            self.button_retry.hover(self.screen)
        for event in pygame.event.get():
            if(event.type==pygame.QUIT):
                save_saving()
                pygame.quit()
                exit()
            if(event.type==pygame.KEYDOWN):
                if(event.key==pygame.K_ESCAPE):
                    self.pause()
                if(event.key==pygame.K_SPACE):
                    self.pause()
            if(event.type==pygame.MOUSEBUTTONDOWN):
                if(hasattr(self,'button_menu')):
                    if(self.button_menu.collidepoint(event.pos)):
                        draw_transition_end(self.screen)
                        return 1
                if(hasattr(self,'button_retry')):
                    if(self.button_retry.collidepoint(event.pos)):
                        return 2
        pygame.display.flip()
    #listen when fail/finish
    def listen_exit(self):
        if(hasattr(self,'button_menu')):
            self.button_menu.hover(self.screen)
        if(hasattr(self,'button_retry')):
            self.button_retry.hover(self.screen)
        for event in pygame.event.get():
            if(event.type==pygame.QUIT):
                save_saving()
                pygame.quit()
                exit()
            if(event.type==pygame.MOUSEBUTTONDOWN):
                if(hasattr(self,'button_menu')):
                    if(self.button_menu.collidepoint(event.pos)):
                        draw_transition_end(self.screen)
                        return 1
                if(hasattr(self,'button_retry')):
                    if(self.button_retry.collidepoint(event.pos)):
                        return 2
        pygame.display.flip()
    #listen when the game is in progress
    def listen_in_game(self):
        for event in pygame.event.get():
            if(event.type==pygame.QUIT):
                save_saving()
                pygame.quit()
                exit()
            if(event.type==pygame.KEYDOWN):
                if(event.key==pygame.K_ESCAPE):
                    self.pause()
                if(event.key==pygame.K_SPACE):
                    self.pause()
                if(event.key==pygame.K_1):
                    if(len(self.char_list)<1):continue
                    char.change_char(self.saving,self.char_list[0])
                    self.drawbelow()
                if(event.key==pygame.K_2):
                    if(len(self.char_list)<2):continue
                    char.change_char(self.saving,self.char_list[1])
                    self.drawbelow()
                if(event.key==pygame.K_3):
                    if(len(self.char_list)<3):continue
                    char.change_char(self.saving,self.char_list[2])
                    self.drawbelow()
                if(event.key==pygame.K_4):
                    if(len(self.char_list)<4):continue
                    char.change_char(self.saving,self.char_list[3])
                    self.drawbelow()
                if(event.key==pygame.K_5):
                    if(len(self.char_list)<5):continue
                    char.change_char(self.saving,self.char_list[4])
                    self.drawbelow()
                if(event.key==pygame.K_6):
                    if(len(self.char_list)<6):continue
                    char.change_char(self.saving,self.char_list[5])
                    self.drawbelow()
                if(event.key==pygame.K_7):
                    if(len(self.char_list)<7):continue
                    char.change_char(self.saving,self.char_list[6])
                    self.drawbelow()
                if(event.key==pygame.K_8):
                    if(len(self.char_list)<8):continue
                    char.change_char(self.saving,self.char_list[7])
                    self.drawbelow()
                if(event.key==pygame.K_RIGHT):
                    char.move(self,[1,0])
                if(event.key==pygame.K_LEFT):
                    char.move(self,[-1,0])
                if(event.key==pygame.K_DOWN):
                    char.move(self,[0,1])
                if(event.key==pygame.K_UP):
                    char.move(self,[0,-1])
                if(event.key==pygame.K_d):
                    char.move(self,[1,0])
                if(event.key==pygame.K_a):
                    char.move(self,[-1,0])
                if(event.key==pygame.K_s):
                    char.move(self,[0,1])
                if(event.key==pygame.K_w):
                    char.move(self,[0,-1])
                if(event.key==pygame.K_p):
                    self.bot_on=1-self.bot_on
#make a new game
def newgame(screen,levelpath,saving):
    level=readlevel(screen,levelpath)
    global maingame
    maingame=Maingame(screen,levelpath,level,saving)
    global char
    char=Char(saving)
    global grid
    grid=Grid(screen,pygame.Color(level['background_color']),pygame.Color(level['color']),pygame.Color(level['shine_color']))
    global obstacles
    obstacles=Obstacles(screen,level['obstacles'],grid.backgroundcolor)
    if(maingame.game()==2):
        newgame(screen,levelpath,saving)
#end game
def endgame():
    global obstacles
    obstacles=None
    global char
    char=None
    global grid
    grid=None
                
