import json
import time
from init import *
from button import *
class Alert():
    #alert draw
    def draw(self,screen,text,sz,i):
        surface=gen_rhombus((0/2,0/2,0/2,i*24),(135,206,250,i*85),sz)
        screen.blit(surface,(width/2-sz/2,height/2-sz/2))
        textsize=35
        if(len(text)>=4):textsize=25
        for j in range(len(text)):    
            surface=pygame.font.Font('assets/font.ttf',textsize).render(text[j],True,pygame.Color(255,255,255,i*85))
            if(text[j]=='Warning!'):surface=pygame.font.Font('assets/font.ttf',textsize).render(text[j],True,pygame.Color(250,0,0,i*85))
            gen_border(surface)
            screen.blit(surface,(width/2-surface.get_width()/2,height/2-surface.get_height()/2+30+(j-len(text))*(textsize+5)))
    #alert part:listen of init
    def init(self,screen,type1=0):
        self.start_time=time.time()
        tick=0
        while(1):
            while time.time()-self.start_time<0.02:
                pass
            tick+=1
            self.confirm_button.draw(screen)
            if(type1==0):self.cancel_button.draw(screen)
            pygame.display.flip()
            a=self.listen(screen,type1)
            if(a>0):return a
    def __init__(self,screen,text,sz=360,type1=1):
        if(isinstance(text,str)):text=[text]
        for i in range(1,4):
            start_time=time.time()
            self.draw(screen,text,sz,i)
            if(type1==0):
                self.cancel_button=Button(screen,width/2-60-70,height/2-21+56,120,36,(0,0,0,255),(135,206,250,i*85),'Cancel')
                self.confirm_button=Button(screen,width/2-60+70,height/2-21+56,120,36,(0,0,0,255),(135,206,250,i*85),'Confirm')
            else:self.confirm_button=Button(screen,width/2-60,height/2-21+56,120,36,(0,0,0,255),(135,206,250,i*85),'Confirm')
            while time.time()-start_time<0.02:
                pass
            pygame.display.flip()
        if(type1==1):self.init(screen,type1)
    #alert listen
    def listen(self,screen,type1):
        self.confirm_button.hover(screen)
        if(type1==0):self.cancel_button.hover(screen)
        for event in pygame.event.get():
            if(event.type==pygame.QUIT):
                save_saving()
                pygame.quit()
                exit()
            if(event.type==pygame.MOUSEBUTTONDOWN):
                if(self.confirm_button.collidepoint(event.pos)):
                    return 1
                if(type1==0 and self.cancel_button.collidepoint(event.pos)):
                    return 2
        return 0
#load saving with checks
def load_saving(screen,origin,filename='saving.json'):
    global saving
    global success_loading
    try:
        file=open(filename,'r')
        try:
            saving=json.load(file)
        except:
            success_loading=0
            saving=origin
            return origin
    except:
        success_loading=0
        saving=origin
        return origin
    if(('settings' in saving) and ('music_volume' in saving['settings']) and (saving['settings']['music_volume'] in range(101)
                              and ('sound_effect_volume' in saving['settings']) and (saving['settings']['sound_effect_volume'] in range(101))
                              and ('judgement_offset' in saving['settings']) and (saving['settings']['judgement_offset'] in range(-200,201))
                              and ('default_char' in saving) and (saving['default_char'] in range(8))
                              and ('unlocked' in saving))
                              and ('copper' in saving)
                              and ('score' in saving) and type(saving['score'])==list and len(saving['score'])==5):
        pass
    else:
        success_loading=0
        saving=origin
        return origin
    success_loading=0
    for i in range(65536):
        if(hash_md5('copper'+str(i)+'copper')==saving['copper']):
            saving['copper']=i
            success_loading+=1
    for i in range(256):
        if(hash_md5('character'+str(i)+'character')==saving['unlocked']):
            saving['unlocked']=i
            success_loading+=1
    for x in range(5):
        for i in range(1000):
            if(hash_md5('score'+str(i)+'score'+str(x)+'score')==saving['score'][x]):
                saving['score'][x]=i
                success_loading+=1
    if(success_loading>=7):success_loading=1
    else:success_loading=0
    if(success_loading==0):
        saving=origin
        return origin
    if(((1<<saving['default_char'])&saving['unlocked'])==0):saving['default_char']=0
    return saving
#return status
def query_load_saving():return success_loading
#save savings
def save_saving(type1=1,filepath='saving.json'):
    global last_save
    if('last_save' not in locals().keys() or (time.time()-last_save)>10000 or type1==1 or filepath!='saving.json'):
        saving2=json.loads(json.dumps(saving))
        saving2['copper']=min(saving2['copper'],65535)
        saving2['unlocked']=hash_md5('character'+str(saving2['unlocked'])+'character')
        saving2['copper']=hash_md5('copper'+str(saving2['copper'])+'copper')
        for i in range(5):saving2['score'][i]=hash_md5('score'+str(saving2['score'][i])+'score'+str(i)+'score')
        file=open(filepath,'w')
        json.dump(saving2,file)
        last_save=time.time()
#check whether a user-made level is available
def checkcolor1(s):
    if(len(s)!=7):return 0
    if(s[0]!='#'):return 0
    for i in range(1,7):
        if((s[i]>='0' and s[i]<='9')or(s[i]>='a' and s[i]<='f')):
            pass
        else:return 0
    return 1
def check_color(screen,stuff,i,text1,text2):
    if(i not in stuff):
        alert=Alert(screen,text1)
        return 1
    if(checkcolor1(stuff[i])==0):
        alert=Alert(screen,text2)
        return 1
    return 0
def check_number(screen,stuff,i,range1,text1,text2):
    if(i not in stuff):
        alert=Alert(screen,text1)
        return 1
    if(stuff[i] not in range1):
        alert=Alert(screen,text2)
        return 1
    return 0
def check_find(screen,stuff,i,text):
    if(i not in stuff):
        alert=Alert(screen,text)
        return 1
    return 0
def check_start_point(screen,stuff,textend,type1=0):
    if('start_point' not in stuff):
        alert=Alert(screen,['Start point not found',textend])
        return 1
    if(type(stuff['start_point'])!=list):
        alert=Alert(screen,['Invalid start point',textend])
        return 1
    if(len(stuff['start_point'])!=2):
        alert=Alert(screen,['Invalid start point',textend])
        return 1
    if(type1==1):return 0
    if((stuff['start_point'][0] in range(gridsize) or stuff['start_point'][0]=='player') and (stuff['start_point'][1] in range(gridsize) or stuff['start_point'][1]=='player')):
        return 0
    else:
        alert=Alert(screen,['Start point out of border',textend])
        return 1
def check_direction(screen,stuff,textend):
    if(stuff['type']=='router'):return 0
    if('direction' not in stuff):
        alert=Alert(screen,['Direction not found',textend])
        return 1
    if(type(stuff['direction'])!=list):
        alert=Alert(screen,['Invalid direction',textend])
        return 1
    if(len(stuff['direction'])!=2):
        alert=Alert(screen,['Invalid direction',textend])
        return 1
    if(stuff['direction'][0] in range(-1,2) and stuff['direction'][1] in range(-1,2)):
        if(stuff['direction'][0]==0 and stuff['direction'][1]==0):
            alert=Alert(screen,['Invalid direction',textend])
            return 1
        return 0
    else:
        alert=Alert(screen,['Invalid direction',textend])
        return 1
def check_anticipation(i):
    if(i['start_point'][0]!='player' and(i['start_point'][0]-i['direction'][0]<0 or i['start_point'][0]-i['direction'][0]>=gridsize)):
        return 0
    if(i['start_point'][1]!='player' and(i['start_point'][1]-i['direction'][1]<0 or i['start_point'][1]-i['direction'][1]>=gridsize)):
        return 0
    return 1
#no explanatory notes,because it is unreadable even explanatory notes are added
def readlevel(screen,filename):
    if(filename.strip()==''):return
    try:
        file=open(filename,'r')
        try:
            level=json.load(file)
            if(check_color(screen,level,'background_color','Background color not found','Invalid background color')==1):return
            if(check_color(screen,level,'color','Color not found','Invalid color')==1):return
            if(check_color(screen,level,'shine_color','Shine color not found','Invalid shine color')==1):return
            if(check_number(screen,level,'bpm',range(1,3600),'BPM not found','Invalid BPM')):return
            if(check_number(screen,level,'turn_limit',range(1,65536),'Turn limit not found','Invalid turn limit')):return
            if(check_number(screen,level,'health',range(1,65536),'Health not found','Invalid health')):return
            
            if('beat_offset' not in level):level['beat_offset']=0
            if((type(level['beat_offset'])!=float and type(level['beat_offset'])!=int) or level['beat_offset']<-1 or level['beat_offset']>1):
                alert=Alert(screen,'Invalid beat offset')
                return
            
            if(check_find(screen,level,'music','Music not found')):return
            
            try:pygame.mixer.music.load(level['music'])
            except:
                alert=Alert(screen,'Invalid music')
                return
            if(check_find(screen,level,'obstacles','Obstacles not found')):return
            if(type(level['obstacles'])!=list):
                alert=Alert(screen,'Obstacles not list')
                return
            for i in range(len(level['obstacles'])):
                textend='in obstacles['+str(i)+']'
                if(check_find(screen,level['obstacles'][i],'type',['Type not found',textend])):return
                if(check_number(screen,level['obstacles'][i],'turn',range(1,level['turn_limit']+1),['Turn not found',textend],['Invalid turn',textend])):return
                if(level['obstacles'][i]['type']=='duo'):
                    if(check_start_point(screen,level['obstacles'][i],textend)):return
                    if(level['obstacles'][i]['start_point']!=[0,(gridsize-1)/2] and level['obstacles'][i]['start_point']!=[gridsize-1,(gridsize-1)/2] and
                       level['obstacles'][i]['start_point']!=[(gridsize-1)/2,0] and level['obstacles'][i]['start_point']!=[(gridsize-1)/2,gridsize-1]):
                        alert=Alert(screen,['Invalid duo start point',textend])
                        
                    if(check_number(screen,level['obstacles'][i],'turn_count',range(4,level['turn_limit']+1),
                                    ['Turn count not found',textend],['Invalid turn count',textend])):return
                elif(level['obstacles'][i]['type']=='arc' or level['obstacles'][i]['type']=='bullet' or level['obstacles'][i]['type']=='conveyor'
                                                          or level['obstacles'][i]['type']=='sorter' or level['obstacles'][i]['type']=='router'):
                    if(level['obstacles'][i]['type']=='router'):
                        level['obstacles'][i]['direction']=[0,0]
                        if('diagonal' not in level['obstacles'][i]):level['obstacles'][i]['diagonal']=0
                        if(level['obstacles'][i]['diagonal'] not in [0,1]):level['obstacles'][i]['diagonal']=1
                    if(level['obstacles'][i]['type']=='bullet'):
                        if('color' not in level['obstacles'][i]):level['obstacles'][i]['color']='pink'
                        if(level['obstacles'][i]['color']!='purple'):level['obstacles'][i]['color']='pink'
                    if(check_start_point(screen,level['obstacles'][i],textend)):return
                    if(check_direction(screen,level['obstacles'][i],textend)):return
                    if(check_anticipation(level['obstacles'][i])==1 and level['obstacles'][i]['turn']<4):
                        alert=Alert(screen,['Anticipation is needed',textend])
                    if(level['obstacles'][i]['type']=='arc' and 'mine_turn' not in level['obstacles'][i]):level['obstacles'][i]['mine_turn']=6
                    elif(level['obstacles'][i]['type']=='arc'):
                        if(level['obstacles'][i]['mine_turn'] not in range(0,level['turn_limit']+1)):
                            alert=Alert(screen,['Invalid mine turn',textend])
                            return
                elif(level['obstacles'][i]['type']=='lancer'):
                    if(level['obstacles'][i]['turn']<3):
                        alert=Alert(screen,'Lancer need anticipation')
                        return
                    if(check_start_point(screen,level['obstacles'][i],textend,1)):return  
                    if((level['obstacles'][i]['start_point'][0]==-1 or level['obstacles'][i]['start_point'][0]==gridsize) and (level['obstacles'][i]['start_point'][1] in range(gridsize) or level['obstacles'][i]['start_point'][1]=='player')):pass
                    elif((level['obstacles'][i]['start_point'][1]==-1 or level['obstacles'][i]['start_point'][1]==gridsize) and (level['obstacles'][i]['start_point'][0] in range(gridsize) or level['obstacles'][i]['start_point'][0]=='player')):pass
                    else:
                        alert=Alert(screen,['Invalid lancer start point',textend])
                        return
                else:
                    alert=Alert(screen,['Invalid type',textend])
                    return
            return level
        except:
            alert=Alert(screen,'Invalid json format')
            return
    except:
        alert=Alert(screen,'File not found')
        return
        
    
