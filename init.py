import pygame
import math
import time
import hashlib
gridsize=13
width=900
height=600
light_blue=(135,206,250)
#character offset
char_dy=[-1,2,6,0,-4,1,1,0]
#calc the pos at a length
def calc(pos,length):
    return length/2-10+(pos-gridsize/2+0.5)*33
#fill a color without changing alpha
def fill(surface,color):
    w,h=surface.get_size()
    r,g,b,_=color
    for x in range(w):
        for y in range(h):
            a=surface.get_at((x, y))[3]
            surface.set_at((x, y),(r, g, b, a))
#make the surface darker
def fill_darker(surface):
    w,h=surface.get_size()
    for x in range(w):
        for y in range(h):
            a=surface.get_at((x,y))
            surface.set_at((x,y),(a.r/2,a.g/2,a.b/2,a.a))
#flip a surface
def flip(surface):
    w,h=surface.get_size()
    #print(w,h)
    for x in range((int)(w/2)):
        for y in range(h):
            a=surface.get_at((x,y))
            b=surface.get_at((w-1-x,y))
            surface.set_at((x,y),b)
            surface.set_at((w-1-x,y),a)
#generate a rhombus for alert
def gen_rhombus(color1,color2,sz=360):
    ans=pygame.Surface((sz+1,sz+1)).convert_alpha()
    for x in range(sz+1):
        for y in range(sz+1):
            if(abs(x-sz/2)+abs(y-sz/2)<=sz/2-10):
                ans.set_at((x,y),color1)
            elif(abs(x-sz/2)+abs(y-sz/2)<=sz/2):
                ans.set_at((x,y),color2)
            else:
                ans.set_at((x,y),(255,255,255,0))
    return ans
#generate transition
def gen_transition(screen,color,param):
    tmp=1
    if(param>0):
        pygame.draw.rect(screen,color,(0,param,width,height-param))
    elif(param==0):
        pass
    else:
        pygame.draw.rect(screen,color,(0,0,width,height+param))
#draw ending transition
def draw_transition_end(screen):
    start_time=time.time()
    tick=0
    while(1):
        while time.time()-start_time<tick/60:
            pass
        tick+=1
        if(tick>20):return
        gen_transition(screen,(135,206,250),(19-tick)*height/20)
        pygame.display.flip()
#generate black border for outlined elements
def gen_border(surface,type1=0):
    if(type1!=0):surface.scroll(0,type1)
    w,h=surface.get_size()
    #print(surface.get_size())
    lst=[]
    for x in range(w):
        for y in range(h):
            if(x!=0 and surface.get_at((x-1,y)).a!=0):
                lst.append([x,y])
            if(y!=0 and surface.get_at((x,y-1)).a!=0):
                lst.append([x,y])
            if(x!=w-1 and surface.get_at((x+1,y)).a!=0):
                lst.append([x,y])
            if(y!=h-1 and surface.get_at((x,y+1)).a!=0):
                lst.append([x,y])
    for i in lst:
        if(surface.get_at((i[0],i[1])).a!=0):
            continue
        #print(i)
        surface.set_at((i[0],i[1]),(0,0,0,255))
    return surface
#crop a surface
def crop(surface,x,y,lenx,leny):
    ans=pygame.Surface((lenx,leny)).convert_alpha()
    for i in range(lenx):
        for j in range(leny):
            ans.set_at((i,j),(0,0,0,0))
    for i in range(max(x,0),min(x+lenx,surface.get_width())):
        for j in range(max(y,0),min(y+leny,surface.get_height())):
            ans.set_at((i-x,j-y),surface.get_at((i,j)))
    return ans
#get the MD5 of a string
def hash_md5(s):
    #print(s)
    md5=hashlib.md5()
    md5.update(s.encode('utf-8'))
    return md5.hexdigest()
