import pygame
import time
from init import *
from button import *
from files import *
import tkinter.filedialog
class Settings_page():
    #draw starting transition
    def draw_transition_begin(self,screen,saving):
        start_time=time.time()
        tick=0
        while(1):
            while time.time()-start_time<tick/60:
                pass
            tick+=1
            if(tick>20):return
            screen.fill((0,0,0))
            self.back_button=Button(screen,20,height-20-36,80,36,(0,0,0),(135,206,250),'back')
            
            self.import_saving_button=Button(screen,width/2-60,height/2-18+56,120,36,(0,0,0),(135,206,250),'import')
            self.export_saving_button=Button(screen,width/2+70,height/2-18+56,120,36,(0,0,0),(135,206,250),'export')
            
            self.draw(screen,saving,0)
            gen_transition(screen,(135,206,250),-tick*height/20)
            pygame.display.flip()
    #draw
    def draw(self,screen,saving,type1=1):
        screen.fill((0,0,0))
        self.back_button.draw(screen)
        self.import_saving_button.draw(screen)
        self.export_saving_button.draw(screen)
        self.w=w=500
        w2=14
        h=36

        screen.blit(self.saving_text,(width/2-self.saving_text.get_width()-70,height/2-self.saving_text.get_height()/2+51))
        
        self.music_button.draw(screen,3)
        self.music_tick=Button(screen,width/2-14/2+(saving['settings']['music_volume']-50)/100*w,height/2-h/2-h-20,14,h,(0,0,0),self.music_tick_color)
        self.music_button.draw_text(screen,'Music Volume: '+str(saving['settings']['music_volume'])+'%')

        self.sound_effect_button.draw(screen,3)
        self.sound_effect_tick=Button(screen,width/2-14/2+(saving['settings']['sound_effect_volume']-50)/100*w,height/2-h/2,14,h,(0,0,0),self.sound_effect_tick_color)
        self.sound_effect_button.draw_text(screen,'Sound Effect Volume: '+str(saving['settings']['sound_effect_volume'])+'%')

        self.judgement_offset_button.draw(screen,3)
        self.judgement_offset_tick=Button(screen,width/2-14/2+(saving['settings']['judgement_offset']/2)/200*w,height/2-h/2-2*h-40,14,h,(0,0,0),self.judgement_offset_tick_color)
        self.judgement_offset_button.draw_text(screen,'Judgement Offset: '+str(saving['settings']['judgement_offset'])+'ms')

        
       
        if(type1==1):pygame.display.flip()
    def __init__(self,screen,saving):

        self.w=w=500
        w2=14
        h=36
        self.saving_text=pygame.font.Font('assets/font.ttf',35).render('saving',True,pygame.Color(255,255,255))
        gen_border(self.saving_text)
        self.music_button=Button(screen,width/2-(w+w2)/2,height/2-h/2-h-20,(w+w2),h,(0,0,0),(135,206,250))
        self.sound_effect_button=Button(screen,width/2-(w+w2)/2,height/2-h/2,(w+w2),h,(0,0,0),(135,206,250))
        self.judgement_offset_button=Button(screen,width/2-(w+w2)/2,height/2-h/2-2*h-40,(w+w2),h,(0,0,0),(135,206,250))

        self.music_tick_color=(47,122,255)
        self.sound_effect_tick_color=(47,122,255)
        self.judgement_offset_tick_color=(47,122,255)
        
        self.mouse_down=0
        
        self.draw_transition_begin(screen,saving)
        
        while(1):
            start_time=time.time()
            self.draw(screen,saving)
            if(self.listen(screen,saving)==1):
                save_saving()
                return
            while time.time()-start_time<0.02:
                pass
    #listen
    def listen(self,screen,saving):
        if(self.music_button.collidepoint(pygame.mouse.get_pos()) or self.mouse_down==1):
            self.music_tick_color=(255,255,255)
        else:
            self.music_tick_color=(47,122,255)
        
        if(self.sound_effect_button.collidepoint(pygame.mouse.get_pos()) or self.mouse_down==2):
            self.sound_effect_tick_color=(255,255,255)
        else:
            self.sound_effect_tick_color=(47,122,255)
        if(self.judgement_offset_button.collidepoint(pygame.mouse.get_pos()) or self.mouse_down==3):
            self.judgement_offset_tick_color=(255,255,255)
        else:
            self.judgement_offset_tick_color=(47,122,255)
        self.back_button.hover(screen)
        self.import_saving_button.hover(screen)
        self.export_saving_button.hover(screen)
        if(self.mouse_down==1):
            saving['settings']['music_volume']=(round)(((pygame.mouse.get_pos()[0]-width/2)+self.w/2)/self.w*100)
            saving['settings']['music_volume']=min(max(saving['settings']['music_volume'],0),100)
            save_saving(0)
        if(self.mouse_down==2):
            saving['settings']['sound_effect_volume']=(round)(((pygame.mouse.get_pos()[0]-width/2)+self.w/2)/self.w*100)
            saving['settings']['sound_effect_volume']=min(max(saving['settings']['sound_effect_volume'],0),100)
            save_saving(0)
        if(self.mouse_down==3):
            saving['settings']['judgement_offset']=(round)(((pygame.mouse.get_pos()[0]-width/2)+self.w/2)/self.w*200*2-200)
            saving['settings']['judgement_offset']=min(max(saving['settings']['judgement_offset'],-200),200)
            save_saving(0)
        
        for event in pygame.event.get():
            if(event.type==pygame.QUIT):
                save_saving()
                pygame.quit()
                exit()  
            if(event.type==pygame.MOUSEBUTTONDOWN):
                if(self.music_button.collidepoint(event.pos)):
                    self.mouse_down=1
                if(self.sound_effect_button.collidepoint(event.pos)):
                    self.mouse_down=2
                if(self.judgement_offset_button.collidepoint(event.pos)):
                    self.mouse_down=3
                if(self.back_button.collidepoint(event.pos)):
                    draw_transition_end(screen)
                    return 1
                #press import saving button
                if(self.import_saving_button.collidepoint(event.pos)):
                    alert=Alert(screen,['Warning!','All previous data will be eliminated.','It is irreverisible.','After importing, the game will automatically exit.'],480,0)
                    if(alert.init(screen)==2):
                        alert=None
                        return
                    self.draw(screen,saving)
                    filepath=tkinter.filedialog.askopenfilename(filetypes=[('JSON','*.json')])
                    if(filepath.strip()==''):return
                    saving=load_saving(screen,saving,filepath)
                    if(query_load_saving()==0):
                        alert=Alert(screen,'Invalid saving.')
                        return
                    alert=Alert(screen,'Exit the game.')
                    save_saving()
                    pygame.quit()
                    exit()
                if(self.export_saving_button.collidepoint(event.pos)):
                    filepath=tkinter.filedialog.asksaveasfilename(defaultextension='.json',filetypes=[('JSON','*.json')])
                    if(filepath.strip()==''):return
                    save_saving(1,filepath)
            if(event.type==pygame.MOUSEBUTTONUP):
                self.mouse_down=0
            if(event.type==pygame.KEYDOWN):
                if(event.key==pygame.K_ESCAPE):
                    draw_transition_end(screen)
                    return 1
                    
                    
        
        
