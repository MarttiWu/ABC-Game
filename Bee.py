# -*- coding: utf-8 -*
'''
    Bee.py
    
    Created by WU,MENG-TING on 2020/11/5.
    Copyright © 2020 WU,MENG-TING. All rights reserved.
'''
import pygame as pg
import random
import math
import numpy as np

#######################################
###    Bees behavior parameters    ###
#######################################
randomWalkProb=0.5
a_radius=50
s_radius=20
c_radius=40
employee_size=5
onlooker_size=40
maxspeed=5.0
numbers = list(range(-15,-1)) + list(range(1,15))

step=4

Ereturn = 1000

#######################
###    image size   ###
#######################
beeimgsize=(20,20) #bee image size
hiveimgsize=(80,100) #hive image size
floimgsize1=(20,20) #flower1 image size
floimgsize2=(30,30) #flower1 image size
floimgsize3=(40,40) #flower1 image size
graimgsize=(20,20) #grass image size
rockimgsize = (40,40) #obstacle image size


#initialize window
windowsize = (800,600)
pg.init()
screen = pg.display.set_mode(windowsize)
pg.display.set_caption("Bee Colony")
background = pg.image.load('images/background.png')
background.convert()
screen.blit(background,(0,0))
#bkgcolor = (205,133,63)
#screen.fill(bkgcolor)

###################################
###    buttons' parameters...   ###
###################################
color = (255,255,255)
st_light = (170,170,170)
st_dark = (100,100,100)
re_light = (255,102,102)
re_dark = (255,0,0)
ob_light = (51,255,255)
ob_dark = (0,204,204)
qu_light = (32,32,32)
qu_dark = (0,0,0)
buttonfont = pg.font.SysFont('Arial',16)


#load images
img = {
#        'E1':pg.transform.scale(pg.image.load('images/employee1.png'), beeimgsize),
#        'E2':pg.transform.scale(pg.image.load('images/employee2.png'), beeimgsize),
#        'E3':pg.transform.scale(pg.image.load('images/employee3.png'), beeimgsize),
#        'E4':pg.transform.scale(pg.image.load('images/employee4.png'), beeimgsize),
#        'E5':pg.transform.scale(pg.image.load('images/employee5.png'), beeimgsize),
#        'E6':pg.transform.scale(pg.image.load('images/employee6.png'), beeimgsize),
#        'E7':pg.transform.scale(pg.image.load('images/employee7.png'), beeimgsize),
#        'E8':pg.transform.scale(pg.image.load('images/employee8.png'), beeimgsize),
#        'O1':pg.transform.scale(pg.image.load('images/onlooker1.png'), beeimgsize),
#        'O2':pg.transform.scale(pg.image.load('images/onlooker2.png'), beeimgsize),
#        'O3':pg.transform.scale(pg.image.load('images/onlooker3.png'), beeimgsize),
#        'O4':pg.transform.scale(pg.image.load('images/onlooker4.png'), beeimgsize),
#        'O5':pg.transform.scale(pg.image.load('images/onlooker5.png'), beeimgsize),
#        'O6':pg.transform.scale(pg.image.load('images/onlooker6.png'), beeimgsize),
#        'O7':pg.transform.scale(pg.image.load('images/onlooker7.png'), beeimgsize),
#        'O8':pg.transform.scale(pg.image.load('images/onlooker8.png'), beeimgsize),
        'GRASS':pg.transform.scale(pg.image.load('images/grass.png'), graimgsize),
        'FLOWER1':pg.transform.scale(pg.image.load('images/flower1.png'), floimgsize1),
        'FLOWER2':pg.transform.scale(pg.image.load('images/flower2.png'), floimgsize2),
        'FLOWER3':pg.transform.scale(pg.image.load('images/flower3.png'), floimgsize3),
        'HIVE':pg.transform.scale(pg.image.load('images/hive.png'), hiveimgsize),
        'SMALLROCK':pg.transform.scale(pg.image.load('images/smallrock.png'), rockimgsize),
        'BIGROCK':pg.transform.scale(pg.image.load('images/bigrock.png'), rockimgsize),
        'eru':pg.transform.scale(pg.image.load('images/e_ru.png'), beeimgsize),
        'erd':pg.transform.scale(pg.image.load('images/e_rd.png'), beeimgsize),
        'elu':pg.transform.scale(pg.image.load('images/e_lu.png'), beeimgsize),
        'eld':pg.transform.scale(pg.image.load('images/e_ld.png'), beeimgsize),
        'oru':pg.transform.scale(pg.image.load('images/o_ru.png'), beeimgsize),
        'ord':pg.transform.scale(pg.image.load('images/o_rd.png'), beeimgsize),
        'olu':pg.transform.scale(pg.image.load('images/o_lu.png'), beeimgsize),
        'old':pg.transform.scale(pg.image.load('images/o_ld.png'), beeimgsize)
}

Sources = []
GlobalBestSource = -1

def FitnessFunction(hive,flower):
    distance = math.sqrt( ((hive.x-flower.x)**2)+((hive.y-flower.y)**2) )
    longestdis = math.sqrt( windowsize[0]**2 + windowsize[1]**2 )
    fmaxsize=3
    if flower.size=='FLOWER1':
        fsize=1
    elif flower.size=='FLOWER2':
        fsize=2
    elif flower.size=='FLOWER3':
        fsize=3
    return (fsize/fmaxsize)/(distance/longestdis)



class Onlooker(pg.sprite.Sprite):
    
    def __init__(self,x,dx,y,dy):
        super().__init__()
        self.image = img['oru']
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.source = -1
        self.carry = 0
        self.sneighbors = []
        self.wing=1
        self.globest = -1
        
    def draw(self,obstacles):
        #goes oppsite direction when reaches the boundaries
        if self.x>800:
            self.x = 1600-self.x
            self.dx = -self.dx
        if self.x<0:
            self.x = -self.x
            self.dx = -self.dx
        if self.y>600:
            self.y = 1200-self.y
            self.dy = -self.dy
        if self.y<0:
            self.y = -self.y
            self.dy = -self.dy

        #change image for different directions
#        if self.dx==0 and self.dy<0:
#            self.image = img['O1']
#        elif self.dx>0 and self.dy<0:
#            self.image = img['O2']
#        elif self.dx>0 and self.dy==0:
#            self.image = img['O3']
#        elif self.dx>0 and self.dy>0:
#            self.image = img['O4']
#        elif self.dx==0 and self.dy>0:
#            self.image = img['O5']
#        elif self.dx<0 and self.dy>0:
#            self.image = img['O6']
#        elif self.dx<0 and self.dy==0:
#            self.image = img['O7']
#        elif self.dx<0 and self.dy<0:
#            self.image = img['O8']
        self.wing = -self.wing
        if self.dx>=0:
            if self.wing==1:
                self.image = img['oru']
            else:
                self.image = img['ord']
                
        else:
            if self.wing==1:
                self.image = img['olu']
            else:
                self.image = img['old']
            
        
        self.rect.center = (self.x,self.y)
        self.x += int(self.dx*step)
        self.y += int(self.dy*step)
                    
        
    def separation(self):
        sV = np.zeros(2)
        if not self.sneighbors:
            return sV
        for n in self.sneighbors:
            sV[0]+=self.x-n.x + random.uniform(0,1)
            sV[1]+=self.y-n.y + random.uniform(0,1)
        sV/=len(self.sneighbors)
        
        uu = np.linalg.norm(sV)
        #prevent divided by 0
        if uu==0:
            uu=0.01
                
        sV = (sV/uu)*maxspeed
    
        return sV
        
            
    def arrivedSource(self):
        x = self.globest.x
        y = self.globest.y
        floimgsize = (0,0)
        if self.globest.size=='FLOWER1':
            floimgsize = floimgsize1
        elif self.globest.size=='FLOWER2':
            floimgsize = floimgsize2
        elif self.globest.size=='FLOWER3':
            floimgsize = floimgsize3
        
        if ((self.x>x-floimgsize[0]//2-5) and (self.x<x+floimgsize[0]//2+5)) and ((self.y>y-floimgsize[1]//2-5) and (self.y<y+floimgsize[1]//2+5)):
            return True
            
        return False
                
    def atHome(self,hives):
        for h in hives:
            if self.x>h.x-hiveimgsize[0]//2+30 and self.x<h.x+hiveimgsize[0]//2-30 and self.y>h.y-hiveimgsize[1]//2+30 and self.y<h.y+hiveimgsize[1]//2-30:
                return True
                
        return False
    
    def update_direction(self,other,flowers,hives,obstacles):
        self.find_neighbors(other)
        #check for collision with obstacles
        if self.is_collided_with(obstacles):
            self.dx = -self.dx
            self.dy = -self.dy
            self.x += self.dx*step
            self.y += self.dy*step
            return
        
        if self.globest!=-1 and self.carry==0 and self.arrivedSource():
            self.carry=1
            self.dx = -self.dx
            self.dy = -self.dy
            self.x += self.dx*step
            self.y += self.dy*step
            self.globest.food-=1
            
            print('food: ',self.globest.food)
            return
        
        #Return to hive with food and store
        if self.carry==1:
            if self.atHome(hives):
                self.carry=0
                self.dx=0
                self.dy=0
                self.globest = GlobalBestSource

            else:
                dx = hives[0].x-self.x
                dy = hives[0].y-self.y
                #prevent divide by 0
                if np.linalg.norm(np.array([dx,dy]))==0:
                    divisor = 0.01
                else:
                    divisor = np.linalg.norm(np.array([dx,dy]))
                self.dx = dx/divisor
                self.dy = dy/divisor
            return
        
        
        
        else:
            #If any source found by employee, go to global best source
            if self.globest!=-1:
                dx = self.globest.x-self.x
                dy = self.globest.y-self.y
                
                if np.linalg.norm(np.array([dx,dy]))==0:
                    divisor = 0.01
                else:
                    divisor = np.linalg.norm(np.array([dx,dy]))
                
                self.dx = dx/divisor
                self.dy = dy/divisor
            #stay at home
            else:
                self.dx=0
                self.dy=0
                self.globest = GlobalBestSource
        #Commented to make the picture not too messy
        '''
        #separation
        #self.find_neighbors(other)
        V = np.zeros(2)
        V += self.separation()
        #prevent divided by 0
        uu = np.linalg.norm(V)
        if uu==0:
            uu=0.01
        print('V: ',V)
        self.dx += V[0]
        self.dy += V[1]
        '''
        
    def find_neighbors(self,other):
        self.sneighbors.clear()
        for o in other:
            if o!=self:
                if math.sqrt((self.x-o.x)**2+(self.y-o.y)**2) < s_radius:
                    self.sneighbors.append(o)
                    
                
    def is_collided_with(self, obstacles):
        for ob in obstacles:
            if ((self.x > ob.x-rockimgsize[0]//2) and (self.x < ob.x+rockimgsize[0]//2)) and ((self.y > ob.y-rockimgsize[1]//2) and (self.y < ob.y+rockimgsize[1]//2)):
                print('self.x: ',self.x)
                print('ob.x: ',ob.x)
                print('rockimgsize[0]//2: ',rockimgsize[0]//2)
                print('self.y: ',self.y)
                print('ob.y: ',ob.y)
                print('rockimgsize[1]//2: ',rockimgsize[1]//2)
                return True
                    
        return False
        

def init_onlookers():

    onlookers = [Onlooker(hiveimgsize[0]//2+10,0,windowsize[1]-hiveimgsize[1]//2-60,0) for i in range(onlooker_size)]
    
    ONLOOKER = pg.sprite.Group()

    for o in onlookers:
        ONLOOKER.add(o)
        
    return onlookers,ONLOOKER










boolchoice = [True,False]


class Employee(pg.sprite.Sprite):
    
    def __init__(self,x,dx,y,dy):
        super().__init__()
        self.image = img['eru']
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.source = -1
        self.foundFlower = -1
        self.carry = 0
        self.sneighbors = []
        self.count=15
        self.wing = 1
        self.back=Ereturn
        self.globest = -1
        self.globalsearch = random.choice(boolchoice)
        self.acheive=False
        self.hit_box = (self.x + 17, self.y + 11, 29, 52)
        
    def draw(self,obstacles):
        life = 1 if self.back<=0 else self.back

        self.hit_box = (self.x - 17, self.y + 11, 29, 52)
        pg.draw.rect(screen, (0, 128, 0), (self.hit_box[0], self.hit_box[1] - 30, 40, 6))
        #print('self.back: ',self.back)
        pg.draw.rect(screen, (255, 0, 0),
                         (self.hit_box[0] + life * 4 *(10/Ereturn), self.hit_box[1] - 30, 40 - life * 4 *(10/Ereturn), 6))
    
        #goes oppsite direction when reaches the boundaries
        if self.x>800:
            self.x = 1600-self.x
            self.dx = -self.dx
        if self.x<0:
            self.x = -self.x
            self.dx = -self.dx
        if self.y>600:
            self.y = 1200-self.y
            self.dy = -self.dy
        if self.y<0:
            self.y = -self.y
            self.dy = -self.dy
        '''
        #check for collision with obstacles
        if self.is_collided_with(obstacles):
            self.dx = -self.dx
            self.dy = -self.dy
            self.x += random.choice(numbers)*2
            self.y += random.choice(numbers)*2
        '''
        #change image for different directions
#        if self.dx==0 and self.dy<0:
#            self.image = img['E1']
#        elif self.dx>0 and self.dy<0:
#            self.image = img['E2']
#        elif self.dx>0 and self.dy==0:
#            self.image = img['E3']
#        elif self.dx>0 and self.dy>0:
#            self.image = img['E4']
#        elif self.dx==0 and self.dy>0:
#            self.image = img['E5']
#        elif self.dx<0 and self.dy>0:
#            self.image = img['E6']
#        elif self.dx<0 and self.dy==0:
#            self.image = img['E7']
#        elif self.dx<0 and self.dy<0:
#            self.image = img['E8']
        self.wing = -self.wing
        if self.dx>=0:
            if self.wing==1:
                self.image = img['eru']
            else:
                self.image = img['erd']
                
        else:
            if self.wing==1:
                self.image = img['elu']
            else:
                self.image = img['eld']


            
        
        self.rect.center = (self.x,self.y)
        self.x += int(self.dx*step)
        self.y += int(self.dy*step)
                    
                
    def foundSource(self,flowers,hives):
        for flower in flowers:
            if flower.size=='FLOWER1':
                floimgsize = floimgsize1
            elif flower.size=='FLOWER2':
                floimgsize = floimgsize2
            elif flower.size=='FLOWER3':
                floimgsize = floimgsize3
        
            if ((self.x>flower.x-floimgsize[0]//2-5) and (self.x<flower.x+floimgsize[0]//2+5)) and ((self.y>flower.y-floimgsize[1]//2-5) and (self.y<flower.y+floimgsize[1]//2+5)):
                self.foundFlower = flower
                self.source = flower
                self.source.val = FitnessFunction(hives[0],flower)
                return True
        return False
                
    def atHome(self,hives):
        for h in hives:
            if self.x>h.x-hiveimgsize[0]//2+20 and self.x<h.x+hiveimgsize[0]//2-20 and self.y>h.y-hiveimgsize[1]//2+20 and self.y<h.y+hiveimgsize[1]//2-20:
                return True
        return False
    
    def isNearGlobal(self):
        a = math.sqrt( ((self.x-self.globest.x)**2)+((self.y-self.globest.y)**2) ) < step*2
        self.acheive = a
        return a
    
    def update_direction(self,other,flowers,hives,obstacles):
        self.back-=1
        global GlobalBestSource
        #global GlobalBestFlower
        #check for collision with obstacles
        if self.is_collided_with(obstacles):
            self.dx = -self.dx
            self.dy = -self.dy
            self.x += self.dx*step
            self.y += self.dy*step
            return
            
        #go home after Ereturn iterations
        if self.back<=0:
            if self.atHome(hives):
                self.globest = GlobalBestSource
                self.back=Ereturn
                self.acheive=False
                print('Time up, back home!')
            else:
                #self.count=3
                dx = hives[0].x-self.x
                dy = hives[0].y-self.y
                self.dx = dx/np.linalg.norm(np.array([dx,dy]))
                self.dy = dy/np.linalg.norm(np.array([dx,dy]))
            return
        
        #Return to hive with food and store and dance
        if self.carry==1:
            if self.atHome(hives):
                if GlobalBestSource==-1 or self.source.val>GlobalBestSource.val:
                    GlobalBestSource = self.source
                Sources.append(self.source)
                if self.count<0:
                    self.carry=0
                    self.count=15
                self.dx=0
                self.dy=0
    
                self.count-=1
                print('count: ',self.count)
                self.globest = GlobalBestSource
                
                self.back=Ereturn
                
            else:
                dx = hives[0].x-self.x
                dy = hives[0].y-self.y
                self.dx = dx/np.linalg.norm(np.array([dx,dy]))
                self.dy = dy/np.linalg.norm(np.array([dx,dy]))
            return
        #Stay at current position to extract food
        if self.foundSource(flowers,hives):
            print('Found Source')
            self.carry=1
            self.dx=0
            self.dy=0
            return
        
        #random walk
        p = random.uniform(0,1)
        
        if self.globest==-1 or self.isNearGlobal() or self.acheive or self.globalsearch:
                
            dx = random.uniform(-1, 1)
            dy = random.uniform(-1, 1)
            dx += self.dx*2
            dy += self.dy*2
            self.dx = dx/np.linalg.norm(np.array([dx,dy]))
            self.dy = dy/np.linalg.norm(np.array([dx,dy]))
        #local search
        else:
            dx = self.globest.x-self.x
            dy = self.globest.y-self.y
            
            if np.linalg.norm(np.array([dx,dy]))==0:
                divisor = 0.01
            else:
                divisor = np.linalg.norm(np.array([dx,dy]))
            
            dx = dx/divisor
            dy = dy/divisor
            
            dx += random.uniform(0,1)
            dy += random.uniform(0,1)

            dx += self.dx*2
            dy += self.dy*2
            self.dx = dx/np.linalg.norm(np.array([dx,dy]))
            self.dy = dy/np.linalg.norm(np.array([dx,dy]))
                    
    def find_neighbors(self,other):
        self.sneighbors.clear()
        for o in other:
            if o!=self:
                if math.dist([self.x,self.y],[o.x,o.y]) < s_radius:
                    self.sneighbors.append(o)
                    
                
            
            
    def is_collided_with(self, obstacles):
        for ob in obstacles:
            if ((self.x > ob.x-rockimgsize[0]//2) and (self.x < ob.x+rockimgsize[0]//2)) and ((self.y > ob.y-rockimgsize[1]//2) and (self.y < ob.y+rockimgsize[1]//2)):
                print('self.x: ',self.x)
                print('ob.x: ',ob.x)
                print('rockimgsize[0]//2: ',rockimgsize[0]//2)
                print('self.y: ',self.y)
                print('ob.y: ',ob.y)
                print('rockimgsize[1]//2: ',rockimgsize[1]//2)
                return True
                    
        return False
        

def init_employees():
    dx = random.uniform(-1, 1)
    dy = random.uniform(-1, 1)
    employees = [Employee(hiveimgsize[0]//2+10,dx/np.linalg.norm(np.array([dx,dy])),windowsize[1]-hiveimgsize[1]//2-60,dy/np.linalg.norm(np.array([dx,dy]))) for i in range(employee_size)]
    
    EMPLOYEE = pg.sprite.Group()

    for e in employees:
        EMPLOYEE.add(e)
        
    return employees,EMPLOYEE
 
##################################################

class Obstacle(pg.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = img['SMALLROCK']
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.x = x
        self.y = y
    def draw(self):
        self.rect.center = (self.x,self.y)

def init_obs():
    obstacles = []
    OBSTACLE = pg.sprite.Group()
    return obstacles,OBSTACLE

##################################################

##################################################

class Flower(pg.sprite.Sprite):
    def __init__(self,x,y,size):
        super().__init__()
        self.image = img[size]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.x = x
        self.y = y
        self.size = size
        self.food=0
        self.val = -1
        self.hit_box = (self.x + 17, self.y + 11, 29, 52)
        if size=='FLOWER1':
            self.food=onlooker_size
        elif size=='FLOWER2':
            self.food=onlooker_size*3
        elif size=='FLOWER3':
            self.food=onlooker_size*9
        
    def draw(self):
        life = 0 if self.food<=0 else self.food
        tot=1
        if self.size=='FLOWER1':
            tot=onlooker_size
        elif self.size=='FLOWER2':
            tot=onlooker_size*3
        elif self.size=='FLOWER3':
            tot=onlooker_size*9
        
        self.hit_box = (self.x - 17, self.y + 11, 29, 52)
        pg.draw.rect(screen, (0, 255, 255), (self.hit_box[0], self.hit_box[1] - 40, 40, 6))
        #print('self.food: ',self.food)
        pg.draw.rect(screen, (255, 250, 250),
                         (self.hit_box[0] + life * 4 *(10/tot), self.hit_box[1] - 40, 40 - life * 4 *(10/tot), 6))
        self.rect.center = (self.x,self.y)

def init_flower():
    flowers = []
    for i in range(3):
        flowers.append(Flower(random.randint(hiveimgsize[0]+5,windowsize[0]-5),random.randint(hiveimgsize[1]+5,windowsize[1]-5),'FLOWER1'))
        
    for i in range(1):
        flowers.append(Flower(random.randint(hiveimgsize[0]+5,windowsize[0]-5),random.randint(hiveimgsize[1]+5,windowsize[1]-5),'FLOWER2'))
        
    for i in range(1):
        flowers.append(Flower(random.randint(hiveimgsize[0]+5,windowsize[0]-5),random.randint(hiveimgsize[1]+5,windowsize[1]-5),'FLOWER3'))
        
    FLOWER = pg.sprite.Group()
    for f in flowers:
        FLOWER.add(f)
    return flowers,FLOWER

##################################################

##################################################

class Grass(pg.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = img['GRASS']
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.x = x
        self.y = y
    def draw(self):
        self.rect.center = (self.x,self.y)

def init_grass():
    grass = [Grass(random.randint(hiveimgsize[0]+5,windowsize[0]-5),random.randint(hiveimgsize[1]+5,windowsize[1]-5)) for i in range(40)]
    
    GRASS = pg.sprite.Group()
    for g in grass:
        GRASS.add(g)
    return grass,GRASS

##################################################

##################################################

class Hive(pg.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = img['HIVE']
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.x = x
        self.y = y
    def draw(self):
        self.rect.center = (self.x,self.y)

def init_hive():
    hives = [Hive(hiveimgsize[0]//2+10,windowsize[1]-hiveimgsize[1]//2-60)]
    HIVE = pg.sprite.Group()
    for h in hives:
        HIVE.add(h)
    return hives,HIVE

##################################################

def main():
    global GlobalBestSource
    global Sources
    
    flowerchoice = ['FLOWER1','FLOWER2','FLOWER3']
    
    clock = pg.time.Clock()

    employees,EMPLOYEE = init_employees()
    onlookers,ONLOOKER = init_onlookers()
    obstacles,OBSTACLE = init_obs()
    flowers,FLOWER = init_flower()
    hives,HIVE = init_hive()
    grass,GRASS = init_grass()
    
    running = True
    START=False
    OBon=False
    while running:
        clock.tick(40)
        for e in pg.event.get():
            if e.type == pg.QUIT:
                running = False
                
            if e.type == pg.MOUSEBUTTONDOWN and OBon:
                pos = pg.mouse.get_pos()
                if 0 <= pos[1] <= 540:
                    ob = Obstacle(pos[0],pos[1])
                    obstacles.append(ob)
                    OBSTACLE.add(ob)
                
            if e.type == pg.MOUSEBUTTONDOWN:
                if 600 <= mouse[0] <= 700 and 560 <= mouse[1] <= 580:
                    pg.quit()
                    
                if 100 <= mouse[0] <= 200 and 560 <= mouse[1] <= 580:
                    START=True
                    
                if 250 <= mouse[0] <= 350 and 560 <= mouse[1] <= 580:
                    GlobalBestSource = -1
                    Sources.clear()
                    employees.clear()
                    EMPLOYEE.empty()
                    onlookers.clear()
                    ONLOOKER.empty()
                    employees,EMPLOYEE = init_employees()
                    onlookers,ONLOOKER = init_onlookers()
                    flowers,FLOWER = init_flower()
                    obstacles.clear()
                    OBSTACLE.empty()
                    START=True
                    OBon=False
                    
                if 450 <= mouse[0] <= 550 and 560 <= mouse[1] <= 580:
                    OBon=True
                
        screen.blit(background,(0,0))
        #screen.fill(bkgcolor)
        '''
            Game start
        '''
        if START:
            if GlobalBestSource!=-1 and GlobalBestSource.food<=0:
                #print('GlobalBestSource: ',GlobalBestSource)
                Sources.remove(GlobalBestSource)
                Sources = sorted(Sources, key= lambda e:e.val)
                
                if GlobalBestSource in flowers:
                    flowers.remove(GlobalBestSource)
                    FLOWER.remove(GlobalBestSource)
                    f = Flower(random.randint(hiveimgsize[0]+5,windowsize[0]-5),random.randint(hiveimgsize[1]+5,windowsize[1]-5),random.choice(flowerchoice))
                    flowers.append(f)
                    FLOWER.add(f)
                    
                if len(Sources)>0:
                    GlobalBestSource = Sources[0]
                else:
                    GlobalBestSource = -1
                print('hurray!')
        
            for ob in obstacles:
                ob.draw()
            
            OBSTACLE.draw(screen)
            
            for g in grass:
                g.draw()
            
            GRASS.draw(screen)
            
            for f in flowers:
                f.draw()
            
            FLOWER.draw(screen)
            
            for h in hives:
                h.draw()
            
            HIVE.draw(screen)
            
            
            for employee in employees:
                employee.draw(obstacles)
                
            for employee in employees:
                employee.update_direction(employees,flowers,hives,obstacles)
                
            EMPLOYEE.draw(screen)
            
            for onlooker in onlookers:
                onlooker.draw(obstacles)
                
            for onlooker in onlookers:
                onlooker.update_direction(onlookers,flowers,hives,obstacles)
                
            ONLOOKER.draw(screen)
        
        
        mouse = pg.mouse.get_pos()
        '''
            Display buttons
        '''
        #Quit button
        if 600 <= mouse[0] <= 700 and 560 <= mouse[1] <= 580:
            pg.draw.rect(screen,qu_light,[600,560,100,20])
        else:
            pg.draw.rect(screen,qu_dark,[600,560,100,20])
        screen.blit(buttonfont.render('Quit' , True , color) , (600+35,560+3))
        #Start button
        if 100 <= mouse[0] <= 200 and 560 <= mouse[1] <= 580:
            pg.draw.rect(screen,st_light,[100,560,100,20])
        else:
            pg.draw.rect(screen,st_dark,[100,560,100,20])
        screen.blit(buttonfont.render('Start' , True , color) , (100+30,560+3))
        #Restart button
        if 250 <= mouse[0] <= 350 and 560 <= mouse[1] <= 580:
            pg.draw.rect(screen,re_light,[250,560,100,20])
        else:
            pg.draw.rect(screen,re_dark,[250,560,100,20])
        screen.blit(buttonfont.render('Restart' , True , color) , (250+30,560+3))
        #Obstacle button
        if 450 <= mouse[0] <= 550 and 560 <= mouse[1] <= 580:
            pg.draw.rect(screen,ob_light,[450,560,100,20])
        else:
            pg.draw.rect(screen,ob_dark,[450,560,100,20])
        screen.blit(buttonfont.render('Obstacle' , True , color) , (450+20,560+3))
        
        pg.display.update()
        

if __name__=='__main__':
    main()
    pg.quit()


