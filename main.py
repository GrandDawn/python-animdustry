import json
from game import *
from settings_page import *
from info_page import *
from character_page import *
from menu_page import *
from files import *
    
if __name__=='__main__':
    #print(pygame.font.get_fonts())
    global screen
    pygame.font.init()
    screen=pygame.display.set_mode([width,height],pygame.DOUBLEBUF)
    pygame.display.set_icon(pygame.image.load('assets-raw/icon.png'))
    pygame.display.set_caption('test')
    pygame.mixer.init()
    pygame.mixer.set_num_channels(2)
    
    saving=load_saving(screen,{'settings':{'music_volume':100,'sound_effect_volume':100,'judgement_offset':0},'copper': 0,'default_char':0,'unlocked':1,'score':[0,0,0,0,0]})
    
    menu_page=Menu_page(screen,saving)

    #newgame(screen,readlevel(screen,'test.json'),saving)
    
    #newgame(screen,readlevel(screen,'ustc1958.json'),saving)
    #newgame(screen,readlevel(screen,'badlevel.json'),saving)
#character shadow
