import pygame
class Button():
    #return a button with width=w,height=h,background color=color1,border color=color2
    def gen_button(self,w,h,color1,color2):
        ans=pygame.Surface((w,h)).convert_alpha()
        for x in range(w):
            for y in range(h):
                if(x<3 or x>=w-3 or y<3 or y>=h-3):
                    ans.set_at((x,y),color2)
                else:
                    ans.set_at((x,y),color1)
        return ans
    '''
    button draw:
    type1=0:only draw text
    type1=1:default
    type1=2:default but without offset
    type1=3:only button
    '''
    def draw(self,screen,type1=1):
        if(type1==1 or type1==2 or type1==3):screen.blit(self.surface,(self.left,self.top))
        if(type1==0 or type1==1):screen.blit(self.text_surface,(self.left+self.w/2-self.text_surface.get_width()/2+2,self.top+self.h/2-self.text_surface.get_height()/2-2))
        elif(type1==2):screen.blit(self.text_surface,(self.left+self.w/2-self.text_surface.get_width()/2,self.top+self.h/2-self.text_surface.get_height()/2))
    def draw_text(self,screen,text,text_color=(255,255,255)):
        self.text_surface=pygame.font.Font('assets/font.ttf',28).render(text,True,text_color)
        self.draw(screen,0)
    def __init__(self,screen,left,top,w,h,color1,color2,text='',text_color=(255,255,255)):
        self.left=left
        self.top=top
        self.w=w
        self.h=h
        self.color1=color1
        self.color2=color2
        self.surface=self.gen_button(w,h,color1,color2)
        self.text_surface=pygame.font.Font('assets/font.ttf',28).render(text,True,text_color)
        self.draw(screen)
    #check whether the point is in the button
    def collidepoint(self,pos):
        if(pos[0]>=self.left and pos[0]<=self.left+self.w and pos[1]>=self.top and pos[1]<=self.top+self.h):
            return 1
        return 0
    #make the button grey when the mouse is on the button
    def hover(self,screen,type1=1):
        if(self.collidepoint(pygame.mouse.get_pos())):
            color1=(100,100,100)
        else:
            color1=(0,0,0)
        if(self.color1==color1):return
        
        self.color1=color1
        self.surface=self.gen_button(self.w,self.h,color1,self.color2)
        self.draw(screen,type1)
