import pygame
import time
from init import *
from button import *
from files import *
class Info_page():
    #draw the starting transition
    def draw_transition(self,screen):
        start_time=time.time()
        tick=0
        while(1):
            while time.time()-start_time<tick/60:
                pass
            tick+=1
            if(tick>20):return
            screen.fill((0,0,0))
            self.draw(screen,0)
            self.back_button=Button(screen,20,height-20-36,80,36,(0,0,0),(135,206,250),'back')
            gen_transition(screen,(135,206,250),-tick*height/20)
            pygame.display.flip()
    #info page draw
    def draw(self,screen,type1=1):
        pygame.draw.rect(screen,(0,0,0),(100,0,width-100,height))
        for i in range(len(self.text_surface)):
            pos=i*30+height-self.position
            if(pos<=-20 or pos>=height+20):continue
            
            screen.blit(self.text_surface[i],(width/2-self.text_surface[i].get_width()/2,pos-self.text_surface[i].get_height()/2))
        
        if(type1==1):pygame.display.flip()
    def __init__(self,screen):
        
        self.speed=1
        self.position=0
        self.text_surface=[]
        
        
        self.text=['Welcome to this game!','This game is a wholly rewritten version of the game Animdustry',
                   '','','-----------------------------------------','','',
                   'How to Play the Game','','Start by selecting a level','Move - WASD','Change Character - 1~8','Turn On/Off Bot Move - P','Pause - ESC/SPACE',
                   '','','-----------------------------------------','','',
                   '- CREDIT -','(Contact me if copyright problems happen)','','Art: @Anuke','Character Designs: @Anuke','','Code (all rewritten): Grand_Dawn','',
                   'Music:','1. Aritus - For You','2. PYC - Stoplight','3. Kepter\'s Room - Bright 79','4. Aritus - Pina Colada II','5. ADRIANWAVE -Peach Beach',
                   '','','-----------------------------------------','','',
                   'The game is all written under python programming language.','','Thank you @illume for pygame library.','','Open sourced at: github.com/GrandDawn/python-animdustry/'
                   '','','-----------------------------------------','','',
                   'To-do List:','1. Different Languages','2. Irregular Grids',
                   '','','-----------------------------------------','','',
                   'FAQs:','','1. Why there is little difference','between this game and the original one?','A: Python is too slow.','',
                   '2. Why would you imitate the game Animdustry?','A: I would like to make custom game for this game','and I would like to make a bot for this game.'
                   '','','-----------------------------------------','','',
                   'This work is a homework for','University of Science and Technology of China','Computer Programming & Computational Thinking Class',
                   'If you are in USTC, my student ID is PB23000188'
                   ]
        self.draw_transition(screen)

        self.back_button=Button(screen,20,height-20-36,80,36,(0,0,0),(135,206,250),'back')
        
        for i in range(len(self.text)):
            self.text_surface.append(pygame.font.Font('assets/font.ttf',32).render(self.text[i],True,pygame.Color(255,255,255)))
        
        start_time=time.time()
        tick=0
        while(1):
            while time.time()-start_time<tick/60:
                pass
            tick+=1
            self.position+=self.speed
            self.draw(screen)
            while(self.listen(screen)==1):
                return
    #listen
    def listen(self,screen):
        self.back_button.hover(screen)
        for event in pygame.event.get():
            if(event.type==pygame.QUIT):
                save_saving()
                pygame.quit()
                exit()
            if(event.type==pygame.KEYDOWN):
                if(event.key==pygame.K_SPACE):
                    self.speed=2
                if(event.key==pygame.K_ESCAPE):
                    draw_transition_end(screen)
                    return 1
            if(event.type==pygame.KEYUP):
                if(event.key==pygame.K_SPACE):
                    self.speed=1
            if(event.type==pygame.MOUSEBUTTONDOWN):
                if(self.back_button.collidepoint(event.pos)):
                    draw_transition_end(screen)
                    return 1
                self.speed=2
            if(event.type==pygame.MOUSEBUTTONUP):
                self.speed=1
                
                    
                    
        
        
