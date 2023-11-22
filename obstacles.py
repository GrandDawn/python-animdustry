import pygame
from init import *
from duo import *
from bullet import *
from conveyor import *
from arc import *
from lancer import *
from sorter import *
from router import *
class Whatever():
    def __init__(self):
        self.unuse=1
        self.repaintlist=[]
class Anticipation():
    def __init__(self,posx,posy,screen):
        self.animation=[]
        self.part_animation=[[[],[],[]],[[],[],[]],[[],[],[]]]
        self.animation.append(gen_border(pygame.transform.scale_by(pygame.image.load('assets-raw/sprites/outlined/wave0.png'),(1.3,1.3))))
        self.animation.append(gen_border(pygame.transform.scale_by(pygame.image.load('assets-raw/sprites/outlined/wave1.png'),(1.3,1.3))))
        self.animation.append(gen_border(pygame.transform.scale_by(pygame.image.load('assets-raw/sprites/outlined/wave2.png'),(1.3,1.3))))
        self.animation.append(gen_border(pygame.transform.scale_by(pygame.image.load('assets-raw/sprites/outlined/wave3.png'),(1.3,1.3))))
        self.posx=posx
        self.posy=posy
        self.repaintlist=[]
        for i in range(3):
            for j in range(3):
                for k in range(4):
                    self.part_animation[i][j].append(crop(self.animation[k],(int)(self.animation[k].get_width()/2-50+i*33),(int)(self.animation[k].get_height()/2-50+j*33),33,33))
        self.unuse=0
        self.round=0
        for i in range(self.posx-1,self.posx+2):
            for j in range(self.posy-1,self.posy+2):
                screen.blit(self.part_animation[i-self.posx+1][j-self.posy+1][self.round],(calc(i,width)-1.5,calc(j,height)-1.5))
    #anticipation animation draw
    def draw(self,screen,repaintlist):
        if(self.unuse==1):return
        if(self.round==2):
            flag=0
            for i in range(self.posx-1,self.posx+2):
                for j in range(self.posy-1,self.posy+2):
                    if([i,j] in repaintlist):flag=1
            if(flag==0):return
            for i in range(self.posx-1,self.posx+2):
                for j in range(self.posy-1,self.posy+2):
                    screen.blit(self.part_animation[i-self.posx+1][j-self.posy+1][self.round],(calc(i,width)-1.5,calc(j,height)-1.5))
            return
        for i in range(self.posx-1,self.posx+2):
            for j in range(self.posy-1,self.posy+2):
                if([i,j] in repaintlist):
                    screen.blit(self.part_animation[i-self.posx+1][j-self.posy+1][self.round],(calc(i,width)-1.5,calc(j,height)-1.5))
    #anticipation animation newturn
    def newturn(self):
        self.repaintlist=[]
        self.round+=1
        for i in range(self.posx-1,self.posx+2):
            for j in range(self.posy-1,self.posy+2):
                self.repaintlist.append([i,j])
        if(self.round==4):self.unuse=1
class Collision():
    def __init__(self,posx,posy):
        self.posx=posx
        self.posy=posy
        self.unuse=0
        self.tick=0
    #collision animation draw
    def draw(self,screen):
        if(self.unuse==1):return
        if(self.tick<=10):image=gen_rhombus((255,255,255,255),(255,255,255,255),(int)(self.tick*2))
        else:image=gen_rhombus((255,255,255,255-(self.tick-10)*25.5),(255,255,255,255-(self.tick-10)*25.5),20)
        screen.blit(image,(calc(self.posx,width)+15-image.get_width()/2,calc(self.posy,height)+15-image.get_height()/2))
    #collision animation newtick
    def newtick(self,screen):
        if(self.unuse==1):return
        self.tick+=1
        if(self.tick==20):
            self.unuse=1
            return
        self.draw(screen)
class Obstacles():
    def __init__(self,screen,obstacles,backgroundcolor):
        self.backgroundcolor=backgroundcolor
        self.screen=screen
        self.obstacles_list=obstacles
        self.conveyor_list=[]
        self.normal_bullet_list=[]
        self.duo_list=[]
        self.duo_bullet_list=[]
        self.arc_list=[]
        self.mine_list=[]
        self.repaintlist=[]
        self.sorter_list=[]
        self.router_list=[]
        self.lancer_list=[]
        self.influence_list=[]
        self.anticipation_list=[]
        self.collision_list=[]
    #every object newturn
    def newturn_handle(self,i,char,type1=1):
        if(i.unuse==1):return
        i.newturn(char)
        if(type1==1 and i.posx==char.wall_position[0] and i.posy==char.wall_position[1] and char.wall_size==1):
            char.wall_health-=1
            i.unuse=1
    #check whether anticipation is needed
    def check_anticipation(self,i):
        if(i['start_point'][0]!='player' and(i['start_point'][0]-i['direction'][0]<0 or i['start_point'][0]-i['direction'][0]>=gridsize)):
            return 0
        if(i['start_point'][1]!='player' and(i['start_point'][1]-i['direction'][1]<0 or i['start_point'][1]-i['direction'][1]>=gridsize)):
            return 0
        return 1
    #newturn
    def newturn(self,char,turn):
        for i in self.anticipation_list:
            if(i.unuse==1):continue
            i.newturn()
        for i in self.lancer_list:self.newturn_handle(i,char,0)
        for i in self.conveyor_list:self.newturn_handle(i,char)
        for i in self.sorter_list:self.newturn_handle(i,char)
        for i in self.router_list:self.newturn_handle(i,char)
        for i in self.mine_list:self.newturn_handle(i,char)
        for i in self.normal_bullet_list:self.newturn_handle(i,char)
        for i in self.duo_list:self.newturn_handle(i,char,0)
        for i in self.duo_bullet_list:self.newturn_handle(i,char)
        for i in self.arc_list:
            i.leave_mine(self.screen,self.mine_list)
            self.newturn_handle(i,char)
        new_anticipation_list=[]
        #add obstacles
        for i in self.obstacles_list:
            if(i['turn']==turn+3):
                if((i['type']=='bullet' or i['type']=='conveyor' or i['type']=='arc' or i['type']=='sorter' or i['type']=='router')and self.check_anticipation(i)):
                    if(i['start_point'][0]=='player'):i['start_point'][0]=(int)(char.posx)
                    if(i['start_point'][1]=='player'):i['start_point'][1]=(int)(char.posy)
                    new_anticipation_list.append(i['start_point'])
            if(i['turn']==turn+2):
                if(i['type']=='lancer'):
                    if(i['start_point'][0]=='player'):i['start_point'][0]=(int)(char.posx)
                    if(i['start_point'][1]=='player'):i['start_point'][1]=(int)(char.posy)
                    self.lancer_list.append(Lancer(self.screen,i['start_point'],self.backgroundcolor))
            if(i['turn']==turn):
                if(i['start_point'][0]=='player'):i['start_point'][0]=(int)(char.posx)
                if(i['start_point'][1]=='player'):i['start_point'][1]=(int)(char.posy)
                if(i['type']=='duo'):
                    self.duo_list.append(Duo(self.screen,i['start_point'],i['turn_count']))
                elif(i['type']=='bullet'):
                    self.normal_bullet_list.append(Bullet(self.screen,i['start_point'],i['direction'],i['color']))
                elif(i['type']=='conveyor'):
                    self.conveyor_list.append(Conveyor(self.screen,i['start_point'],i['direction']))
                elif(i['type']=='arc'):
                    self.arc_list.append(Arc(self.screen,i['start_point'],i['direction'],i['mine_turn']))
                elif(i['type']=='sorter'):
                    self.sorter_list.append(Sorter(self.screen,i['start_point'],i['direction']))
                elif(i['type']=='router'):
                    self.router_list.append(Router(self.screen,i['start_point'],i['diagonal']))
        #add anticipation
        tmp=[]
        for i in new_anticipation_list:
            if i not in tmp:tmp.append(i)
        new_anticipation_list=tmp
        for i in new_anticipation_list:
            self.anticipation_list.append(Anticipation(i[0],i[1],self.screen))
        #the collision of conveyors
        conveyor_list=[]
        collision_list=[]
        for i in self.conveyor_list:
            if(i.unuse==1):continue
            conveyor_list.append([i.posx,i.posy,i.direction])
        for i in self.conveyor_list:
            if(i.unuse==1):continue
            if([i.posx,i.posy,[-i.direction[0],-i.direction[1]]] in conveyor_list):
                i.unuse=1
                collision_list.append([i.posx,i.posy])
        tmp=[]
        for i in collision_list:
            if i not in tmp:tmp.append(i)
        self.collision_list=[]
        for i in tmp:
            self.collision_list.append(Collision(i[0],i[1]))
    #every object repaint
    def repaint_handle(self,i,repaintlist):
        if(i.unuse==1 and i.repaintlist==[]):return
        if([i.posx,i.posy] in repaintlist):
            i.draw(self.screen)
        if(i.posx==-1 or i.posx==gridsize or i.posy==-1 or i.posy==gridsize):
            i.draw(self.screen,1)
    #repaint
    def repaint(self,repaintlist):
        for i in self.anticipation_list:
            if(i.unuse==1):continue
            if(i.round!=3):continue
            i.draw(self.screen,repaintlist)
        for i in self.lancer_list:self.repaint_handle(i,repaintlist)
        for i in self.conveyor_list:self.repaint_handle(i,repaintlist)
        for i in self.sorter_list:self.repaint_handle(i,repaintlist)
        for i in self.router_list:self.repaint_handle(i,repaintlist)
        for i in self.mine_list:self.repaint_handle(i,repaintlist)
        for i in self.duo_bullet_list:self.repaint_handle(i,repaintlist)
        for i in self.duo_list:self.repaint_handle(i,repaintlist)
        for i in self.normal_bullet_list:self.repaint_handle(i,repaintlist)
        for i in self.arc_list:self.repaint_handle(i,repaintlist)
        for i in self.anticipation_list:
            if(i.unuse==1):continue
            if(i.round==3):continue
            i.draw(self.screen,repaintlist)
        for i in self.collision_list:
            if(i.unuse==1):continue
            i.draw(self.screen)
    #every object newtick
    def newtick_handle(self,i,char,repaintlist,type1=0):
        if(i.unuse==1 and i.repaintlist==[]):
            i=Whatever()
            return
        tmp=i.newtick(self.screen,char)
        if(tmp==114514):i.shoot(self.screen,self.duo_bullet_list)
        if(tmp==1919810):i.shoot(self.screen,self.conveyor_list)
        self.repaintlist+=i.repaintlist
        if([i.posx,i.posy] in repaintlist or [i.posx,i.posy] in self.influence_list):
            i.draw(self.screen)
        if(type1==1 and [i.posx,i.posy] in char.explode_grid):
            i.unuse=1
        if(i.unuse==1):
            i.repaintlist=[]
    #newtick
    def newtick(self,char,repaintlist):
        self.repaintlist=[]
        for i in self.anticipation_list:
            if(i.unuse==1):continue
            if(i.round!=3):continue
            i.draw(self.screen,repaintlist)
            self.repaintlist+=i.repaintlist
            i.repaintlist=[]
        for i in self.lancer_list:self.newtick_handle(i,char,repaintlist)
        for i in self.conveyor_list:self.newtick_handle(i,char,repaintlist,1)
        for i in self.sorter_list:self.newtick_handle(i,char,repaintlist,1)
        for i in self.router_list:self.newtick_handle(i,char,repaintlist,1)
        for i in self.mine_list:self.newtick_handle(i,char,repaintlist)
        for i in self.duo_bullet_list:self.newtick_handle(i,char,repaintlist)
        for i in self.duo_list:self.newtick_handle(i,char,repaintlist)
        for i in self.normal_bullet_list:self.newtick_handle(i,char,repaintlist)
        for i in self.arc_list:self.newtick_handle(i,char,repaintlist,1)
        for i in self.anticipation_list:
            if(i.unuse==1):continue
            if(i.round==3):continue
            i.draw(self.screen,repaintlist)
            self.repaintlist+=i.repaintlist
            i.repaintlist=[]
        for i in self.collision_list:
            if(i.unuse==1):continue
            i.newtick(self.screen)
            self.repaintlist.append([i.posx,i.posy])
        tmp=[]
        for i in self.repaintlist:
            if i not in tmp:tmp.append(i)
        self.repaintlist=tmp

        self.influence_list=[]
        for i in self.lancer_list:
            self.influence_list+=i.influence_list
        tmp=[]
        for i in self.influence_list:
            if i not in tmp:tmp.append(i)
        self.influence_list=tmp
