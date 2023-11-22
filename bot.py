from init import *
import random
def random_with_weight(lst):
    s=0
    for i in range(len(lst)):s+=lst[i]
    tmp=random.randint(1,s)
    for i in range(len(lst)):
        tmp-=lst[i]
        if(tmp<=0):return i
class Bot():
    #check whether a place is affected by duo
    def check_duo(self,posx,posy,direction,start_turn,turnleft,turn,x,y):
        if(direction==[0,0]):
            if(posx==0):direction=[1,0]
            if(posy==0):direction=[0,1]
            if(posx==gridsize-1):direction=[-1,0]
            if(posy==gridsize-1):direction=[0,-1]
        for i in range(start_turn+1,min(turn+1,start_turn+turnleft)):
            if((start_turn+turnleft-i)%2==1):
                char_pos=self.pos[i-self.start_turn]
                if(direction[0]==0):
                    if(char_pos[0]>posx):posx+=1
                    elif(char_pos[0]<posx):posx-=1
                if(direction[1]==0):
                    if(char_pos[1]>posy):posy+=1
                    elif(char_pos[1]<posy):posy-=1
            if((start_turn+turnleft-i)%4==1):
                if(x==posx+(turn-i)*direction[0] and y==posy+(turn-i)*direction[1]):return 0
        return 1
    #check whether a place is affected by router
    def check_router(self,posx,posy,start_turn,diag,turn,x,y):
        for i in range(max(start_turn,self.start_turn),min(start_turn+2,turn+1)):
            if(diag==0):
                for j in [[1,0],[-1,0],[0,-1],[0,1]]:
                    if(x==posx+(turn-i)*j[0] and y==posy+(turn-i)*j[1]):return 0
            else:
                for j in [[1,1],[-1,1],[1,-1],[-1,-1]]:
                    if(x==posx+(turn-i)*j[0] and y==posy+(turn-i)*j[1]):return 0
        if(turn==start_turn+2 and x==posx and y==posy):return 0
        return 1
    #check whether a place is affected by sorter
    def check_sorter(self,posx,posy,direction,turntype,start_turn,turn,x,y):
        turntype=1-turntype
        for i in range(start_turn,turn+1):
            turntype=1-turntype
            if(turntype==0):
                if(i!=start_turn):
                    posx+=direction[0]
                    posy+=direction[1]
                if(posx<0 or posx>=gridsize or posy<0 or posy>=gridsize):break
                for j in [[1,0],[-1,0],[0,-1],[0,1]]:
                    if(j[0]+direction[0]==0 and j[1]+direction[1]==0):continue
                    if(x==posx+(turn-i)*j[0] and y==posy+(turn-i)*j[1]):return 0
            if(i==turn and x==posx and y==posy):return 0
        return 1
    #initialize the obstacles besides the three things mentioned above
    def __init__(self,obstacles,start_turn):
        self.obstacles=[]
        for i in obstacles.obstacles_list:
            if(i['turn']>start_turn and i['turn']<start_turn+10):
                self.obstacles.append(i)
        self.start_turn=start_turn#start_turn has ended
        self.grid=[]
        self.pos=[]
        #handle all determined obstacles place
        for k in range(10):
            tmp=[]
            for i in range(gridsize):
                tmp2=[]
                for j in range(gridsize):tmp2.append(0)
                tmp.append(tmp2)
            self.grid.append(tmp)        
        
        for s in obstacles.lancer_list:
            if(s.unuse==1):continue
            if(s.posx==-1 or s.posx==gridsize):
                for i in range(0,gridsize):
                    self.grid[s.turnleft][i][(int)(s.posy)]=1
            else:
                for i in range(0,gridsize):
                    self.grid[s.turnleft][(int)(s.posx)][i]=1
        for s in obstacles.mine_list:
            if(s.unuse==1):continue
            for i in range(min(s.turnleft,10)):
                self.grid[i][s.posx][s.posy]=1
        for s in obstacles.conveyor_list:self.grid_bullets(s)
        for s in obstacles.normal_bullet_list:self.grid_bullets(s)
        for s in obstacles.duo_bullet_list:self.grid_bullets(s)
        for s in obstacles.arc_list:
            if(s.unuse==1):continue
            for i in range(10):
                x=s.posx+s.direction[0]*i
                y=s.posy+s.direction[1]*i
                if(x<0 or x>=gridsize or y<0 or y>=gridsize):break
                for j in range(i,min(10,i+s.mine_turn+1)):
                    self.grid[j][x][y]=1
        self.duo_list=obstacles.duo_list
        self.sorter_list=obstacles.sorter_list
        self.router_list=obstacles.router_list
        '''
        for k in range(10):
            for i in range(gridsize):print(self.grid[k][i])
            print()
        '''
    #find the next move
    def calc(self,pos,lastmove):
        for i in range(6,0,-1):
            tmp=self.dfs(self.start_turn,(int)(pos[0]),(int)(pos[1]),lastmove,i)
            if(tmp!=0):return tmp
        print('fail to find a move')
        return [0,0]
    #the same for conveyors/bullets
    #don't want to handle conveyors collision
    def grid_bullets(self,s):
        if(s.unuse==1):return
        for i in range(10):
            x=s.posx+s.direction[0]*i
            y=s.posy+s.direction[1]*i
            if(x<0 or x>=gridsize or y<0 or y>=gridsize):break
            self.grid[i][x][y]=1
    #check anticipation
    def check_anticipation(self,i):
        if(i['start_point'][0]!='player' and(i['start_point'][0]-i['direction'][0]<0 or i['start_point'][0]-i['direction'][0]>=gridsize)):
            return 0
        if(i['start_point'][1]!='player' and(i['start_point'][1]-i['direction'][1]<0 or i['start_point'][1]-i['direction'][1]>=gridsize)):
            return 0
        return 1
    #check whether a position is safe in turn
    def check(self,turn,x,y):
        if(self.grid[turn-self.start_turn][x][y]==1):return 0
        for i in self.obstacles:
            if(i['type']=='lancer'):
                if(i['turn']!=turn):continue
                posx=i['start_point'][0]
                posy=i['start_point'][1]
                if(posx=='player'):posx=self.pos[turn-self.start_turn-2]
                if(posy=='player'):posy=self.pos[turn-self.start_turn-2]
                if(posx==x or posy==y):return 0
            elif(i['type']=='duo'):
                if(self.check_duo(i['start_point'][0],i['start_point'][1],[0,0],i['turn'],i['turn_count'],turn,x,y)==0):return 0
            elif(i['type']=='sorter'):
                if(i['turn']>turn):continue
                posx=i['start_point'][0]
                posy=i['start_point'][1]
                if(posx=='player'):posx=self.pos[turn-self.start_turn-3*self.check_anticipation(i)][0]
                if(posy=='player'):posy=self.pos[turn-self.start_turn-3*self.check_anticipation(i)][1]
                if(self.check_sorter(posx,posy,i['direction'],0,i['turn'],turn,x,y)==0):return 0
            elif(i['type']=='router'):
                if(i['turn']>turn):continue
                posx=i['start_point'][0]
                posy=i['start_point'][1]
                if(posx=='player'):posx=self.pos[turn-self.start_turn-3*self.check_anticipation(i)][0]
                if(posy=='player'):posy=self.pos[turn-self.start_turn-3*self.check_anticipation(i)][1]
                if(self.check_router(posx,posy,i['turn'],i['diagonal'],turn,x,y)==0):return 0
            else:
                if(i['turn']>turn):continue
                posx=i['start_point'][0]
                posy=i['start_point'][1]
                if(posx=='player'):posx=self.pos[turn-self.start_turn-3*self.check_anticipation(i)][0]
                if(posy=='player'):posy=self.pos[turn-self.start_turn-3*self.check_anticipation(i)][1]
                if(posx+i['direction'][0]*(turn-i['turn'])==x and posy+i['direction'][1]*(turn-i['turn'])==y):return 0
                if(i['type']=='arc'):
                    for j in range(max(turn-i['turn']-i['mine_turn'],0),turn-i['turn']):
                        if(posx+i['direction'][0]*j==x and posy+i['direction'][1]*j==y):return 0
        for i in self.duo_list:
            if(i.unuse==1):continue
            if(self.check_duo(i.posx,i.posy,i.direction,self.start_turn,i.turnleft,turn,x,y)==0):return 0
        for i in self.sorter_list:
            if(i.unuse==1):continue
            if(self.check_sorter(i.posx,i.posy,i.direction,i.turntype,self.start_turn,turn,x,y)==0):return 0
        for i in self.router_list:
            if(i.unuse==1):continue
            if(self.check_router(i.posx,i.posy,self.start_turn+i.turnleft-3,i.diag,turn,x,y)==0):return 0
    
    def dfs(self,turn,posx,posy,lastmove,maxstep):
        if(posx<0 or posy<0 or posx>=gridsize or posy>=gridsize):return 0
        while(len(self.pos)>turn-self.start_turn):self.pos.pop()
        self.pos.append([posx,posy])
        if(self.check(turn,posx,posy)==0):return 0
        if(turn==self.start_turn+maxstep):return 1
        #50% move front,25% move back,25% turn
        direction_list_tmp=[[-1,0],[1,0],[0,-1],[0,1]]
        direction_list=[]
        posibility_list=[]
        if(lastmove==[0,0]):
            posibility_list=[1,1,1,1]
        else:
            for i in direction_list_tmp:
                if(i==lastmove):posibility_list.append(i)
            for i in direction_list_tmp:
                if(i[0]+lastmove[0]==0 and i[1]+lastmove[1]==0):posibility_list.append(i)
            for i in direction_list_tmp:
                if(i==lastmove or i[0]+lastmove[0]==0 and i[1]+lastmove[1]==0):continue
                posibility_list.append(i)
            direction_list_tmp=posibility_list
            posibility_list=[4,2,1,1]

        for abc in range(4):
            i=random_with_weight(posibility_list)
            posibility_list[i]=0
            direction_list.append(direction_list_tmp[i])
        for i in direction_list:
            if(self.dfs(turn+1,posx+i[0],posy+i[1],i,maxstep)):return i
        if(self.dfs(turn+1,posx,posy+1,[0,0],maxstep)!=0):return [0,0]
        return 0
