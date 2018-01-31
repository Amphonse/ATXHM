import numpy as np
import random,pygame
import path_iso_copy
import useful_fucs

#dont know not my code
def convert_iso_dots(r):
    y = r[1]*32
    x = r[0]*32
    x +=32
    y += 32
    if (r[0]-(r[0]-int(r[0])))%2 == 0:
        y -= 16

    return (int(x),int(y))


#basic items class
class items():
    def __init__(self,cost,weight,name):
        self.name = name
        self.cost = cost
        self.weight = weight 

    def draw_self(self,screen):
        pygame.draw.circle(screen, (255,0,255), convert_iso_dots(self.coords), 3)
#here follows item types which inheret the items above
#this in general needs more stuff added as this is still kinda bare bones possibley
class armor(items):
    def __init__(self,cost,weight,name,armor,location,health,cmod):
        super().__init__(cost,weight,name)
        self.armor = armor
        self.location = location
        self.health = health
        self.cmod = cmod
        self.maxhealth = health
class weepons(items):
    def __init__(self,cost,weight,name,dtype,atktype,dmg,ranges=0,coords= None):
        self.ranges = ranges
        super().__init__(cost,weight,name)
        self.dtype = dtype
        self.atktype = atktype
        self.dmg = dmg
        self.coords = coords
#this needs work
class consumables(items):
    def __init__(self,cost,weight,name,charges,types,coords= None):
        super().__init__(cost,weight,name)
        self.charges = charges
        self.coords = coords
#this needs work        
class shield(weepons):
    def __init_(self,cost,weight,name,dtype,atktype,dmg,shielding):
        super().__init__(cost,weight,name,dtype,atktype,dmg)
        self.shielding = shielding
#main person calss
class mans():
    def __init__(self,name,screen):
        #here follows a ton of variables needed in later functions
        self.screen = screen
        self.vatss = False
        self.name = name
        self.wounds = 0
        self.wound = 0
        self.shock = 0
        self.state = "Normal"
        self.will = np.random.normal(50,16.6)
        self.magic = np.random.normal(50,16.6)
        self.strn = np.random.normal(50,16.6)
        self.melee = np.random.normal(50,16.6)
        self.ranged = np.random.normal(50,16.6)
        self.thrown = np.random.normal(50,16.6)
        self.movment = np.random.normal(50,16.6)
        self.shielding = np.random.normal(50,16.6)
        self.dodge = np.random.normal(50,16.6)
        self.parry = np.random.normal(50,16.6)
        self.endurance = np.random.normal(100,16.6)
        self.attacks = 1
        self.actions = 0
        self.tot_actions = 2
        self.limbs = {'Head':[100,1,armor(0,0,"Head armor of some sort",20,"Head",200,20),"Normal",10]
                      ,'Torso':[100,1,armor(0,0,"Basically a pillow",0,'Torso',100,5),"Normal",5]
                      ,'Vitals':[100,1,armor(0,0,"Basically a pillow",0,'Vitals',100,5),"Normal",20]
                      ,'Left Arm':[100,0.2,armor(0,0,"Bare",0,'Left Arm',0,0),"Normal",2]
                      ,'Right Arm':[100,0.2,armor(0,0,"Bare",0,'Right Arm',0,0),"Normal",2]
                      ,'Left Leg':[100,0.3,armor(0,0,"Bare",0,'Left Leg',0,0),"Normal",2]
                      ,'Right Leg':[100,0.3,armor(0,0,"Bare",0,'Right Leg',0,0),"Normal",2]
                      ,'Left Hand':[100,0.1,armor(0,0,"Iron Gauntlets",20,'Left Hand',100,5),"Normal",1]
                      ,'Right Hand':[100,0.1,armor(0,0,"Bare",0,'Right Hand',0,0),"Normal",1]
                      ,'Left Foot':[100,0.1,armor(0,0,"Bare",0,'Left Foot',0,0),"Normal",1]
                      ,'Right Feet':[100,0.1,armor(0,0,"Slipper",1,'Right Feet',100,1),"Normal",1]
                      ,'Groin':[100,0.2,armor(0,0,"Godpiece",100,'Groin',100,0),"Normal",60]
                      }
        self.health = 100
        self.equipment = {"Left Hand":[[None],1],"Right Hand":[[weepons(0,0,"The pow bow wow","Impaling","Ranged",20)],1],"Back":[[consumables(0,0,"Arrers",10,"Ammo")],5],"Belt":[[weepons(0,0,"Dagger","Cutting","Melee",100)],2]}
        self.head_im = pygame.image.load("Head.png").convert()
        self.head_im.set_colorkey((255,255,255))
        self.head_rekt = self.head_im.get_rect()
        self.torso_im = pygame.image.load("Torso.png").convert()
        self.torso_im.set_colorkey((255,255,255))
        self.torso_rekt = self.head_im.get_rect()
        self.legs1_im = pygame.image.load("Legs.png").convert()
        self.legs1_im.set_colorkey((255,255,255))
        self.legs1_rekt = self.head_im.get_rect()
        self.legs2_im = pygame.image.load("Legs.png").convert()
        self.legs2_im.set_colorkey((255,255,255))
        self.legs2_rekt = self.head_im.get_rect()
        self.feet1_im = pygame.image.load("Feets.png").convert()
        self.feet1_im.set_colorkey((255,255,255))
        self.feet1_rekt = self.head_im.get_rect()
        self.feet2_im = pygame.image.load("Feets.png").convert()
        self.feet2_im.set_colorkey((255,255,255))
        self.feet2_rekt = self.head_im.get_rect()
        self.larm_im = pygame.image.load("Left Arm.png").convert()
        self.larm_im.set_colorkey((255,255,255))
        self.larm_rekt = self.head_im.get_rect()
        self.rarm_im = pygame.image.load("Right Arm.png").convert()
        self.rarm_im.set_colorkey((255,255,255))
        self.rarm_rekt = self.head_im.get_rect()
        self.hand1_im = pygame.image.load("Hands.png").convert()
        self.hand1_im.set_colorkey((255,255,255))
        self.hand1_rekt = self.head_im.get_rect()
        self.hand2_im = pygame.image.load("Hands.png").convert()
        self.hand2_im.set_colorkey((255,255,255))
        self.hand2_rekt = self.head_im.get_rect()
        self.mpos = (0,0)
        self.drawing = None
        self.menu = False
        self.chose_who = False
        self.whoo = None
        self.resize()
    def get_hit(self,location,dmg,dtype):
        #calculates dmg wounds shock and wound
        #dmg is as it sounds
        #wounds is a % of dmg and cause wound to slowly accumilate
        #if wound >health they die
        #shock makes it harder to wake up /easier to fall unconciouos is also a % of dmg
        #variations depending on cutting,crushing or impaling dmg
        odmg = dmg
        if dtype == "Crushing":
            if self.limbs[location][2].maxhealth>0:
                dmg -= self.limbs[location][2].cmod*self.limbs[location][2].health/self.limbs[location][2].maxhealth
            self.limbs[location][2].health -= odmg
        else:
            if self.limbs[location][2].maxhealth>0:
                dmg -= self.limbs[location][2].cmod*self.limbs[location][2].health/self.limbs[location][2].maxhealth
            self.limbs[location][2].health -= odmg
        if dmg < 0:
            dmg = 0
        if dtype == "Impaling":
            self.limbs[location][2].health -= odmg/10
            dmg *= 2
        if dtype == "Cutting":
            self.limbs[location][2].health -= odmg/10
            dmg *= 1.5
        if self.limbs[location][2].health < 0:
            self.limbs[location][2] = armor(0,0,"Bare",0,9,0,0)
        self.limbs[location][0] -= dmg
        print(self.name + " was hit in the "+location +" for "+str(dmg)+" Damage")
        self.health -= (dmg*self.limbs[location][1])*100/self.endurance
        print(self.name +" took "+str((dmg*self.limbs[location][1])*100/self.endurance)+" Damage")
        self.wounds +=((dmg*self.limbs[location][1])*100/self.endurance)/10
        self.wound += ((dmg*self.limbs[location][1])*100/self.endurance)/5
        self.shock += ((dmg*self.limbs[location][1])*100/self.endurance)*self.limbs[location][4]
        if self.health<0:
            self.health=0
        self.mupdate()
    def mupdate(self):
        #does the stuff with wounds and does checks to see if dead
        if self.state == "Normal":
            if self.health*self.endurance/100 < self.wound:
                self.state = "Dead"
                print(self.state)
            elif self.health*self.endurance/100 < self.shock+self.wound*2:
                self.state = "Unconcious"
                print(self.state)
            else:
                pass
        elif self.state == "Unconcious":
            if self.health*self.endurance/100 < self.wound:
                self.state = "Dead"
                print(self.state)
            elif self.health*self.endurance/100 > self.shock*2+self.wound*10:
                self.state = "Normal"
                print(self.name+" wakes up")
            else:
                pass
        self.wound += (self.wounds-1)
        self.shock -= (self.endurance/20)
        if self.wound < 0:
            self.wound = 0
        if self.wound > 100:
            self.wound = 100
        if self.shock < 0:
            self.shock = 0
    def attack(self,hand,who,aimed_location,turns_aimed = 0,dist=0):
        #assuming they aimed it will roll attack and defence and see who wins
        if aimed_location != None:
            wep = self.equipment[hand][0][0]
            if wep == None:
                wep = weepons(0,0,"Fisto","Crushing","Melee",5)
            roll = random.random()*100
            if wep.atktype == "Melee":
                self.margina = self.melee-roll
            elif wep.atktype == "Ranged":
                self.margina = self.ranged-roll
            who.defend()
            if who.margind > self.margina:
                print(self.name+" missed "+who.name)
            else:
                who.get_hit(aimed_location,wep.dmg,wep.dtype)


    def defend(self):
        #when attacked this calc defence roll
        #do only if normal
        roll = random.random()*100
        if self.equipment["Left Hand"] == None and self.equipment["Right Hand"] == None:
            self.margind = self.dodge-roll
        elif self.equipment["Left Hand"] is shield or self.equipment["Right Hand"] is shield:
            if self.equipment["Left Hand"] is weepons or self.equipment["Right Hand"] is weepons:
                block = max(self.shielding,self.parry,self.dodge)
                self.margind = roll - block
            else:
                if self.shielding > self.dodge:
                    self.margind = self.shielding-roll
                else:
                    self.margind = self.dodge-roll
        else:
            if self.parry > self.dodge:
                self.margind = self.parry-roll
            else:
                self.margind = self.dodge-roll
        if self.state != "Normal":
            self.margind =0
                
    def invman(self,what,froms,to):
        #basic inventory management
        if self.equipment[to][0][0] == None:
            self.equipment[to][0] = [self.equipment[froms][what][0]]
        elif len(self.equipment[to][0]) < self.equipment[to][1]:
            self.equipment[to].append(self.equipment[froms][what])
            if len(self.equipment[froms][0]) == 1:
                self.equipment[froms][0] = [None]
            else:
                self.equipment[froms].remove(self.equipment[froms][what])

        else:
            print(to + " full")
    def pick_up(self,what):
        #just places something from floor to hand
        if self.equipment["Left Hand"][0] == [None]:
            self.equipment["Left Hand"][0] = [what]
            what.coords = None
        elif self.equipment["Right Hand"][0] == [None]:
            self.equipment["Right Hand"][0] = [what]
            what.coords = None
        else:
            print(self.name+ " has no free hands")
    def throw(self,withs,what,where):
        #just sets what your thrwoing to none so it falls into the void
        self.equipment[withs][0] = [None]
    def reset(self):
        #redraws the ui
        pygame.draw.polygon(self.screen,(100,100,100),
                            ((self.prop*320+self.delta_x,self.prop*800+self.delta_y),
                             (self.prop*320+self.delta_x,self.prop*700+self.delta_y),
                             (self.prop*960+self.delta_x,self.prop*700+self.delta_y),
                             (self.prop*960+self.delta_x,self.prop*800+self.delta_y))
                            ,0)
        pygame.draw.polygon(self.screen,(50,50,50),
                             ((self.prop*320+self.delta_x,self.prop*800+self.delta_y),
                              (self.prop*320+self.delta_x,self.prop*700+self.delta_y),
                              (self.prop*960+self.delta_x,self.prop*700+self.delta_y),
                              (self.prop*960+self.delta_x,self.prop*800+self.delta_y))
                             ,int(self.prop*5))
        pygame.draw.line(self.screen,(50,50,50),(int(self.prop*420+self.delta_x),int(self.prop*800+self.delta_y)),(int(self.prop*420+self.delta_x),int(self.prop*700+self.delta_y)),int(self.prop*5))
        pygame.draw.line(self.screen,(50,50,50),(int(self.prop*860+self.delta_x),int(self.prop*800+self.delta_y)),(int(self.prop*860+self.delta_x),int(self.prop*700+self.delta_y)),int(self.prop*5))
        pygame.draw.line(self.screen,(50,50,50),(int(self.prop*520+self.delta_x),int(self.prop*800+self.delta_y)),(int(self.prop*520+self.delta_x),int(self.prop*700+self.delta_y)),int(self.prop*5))
        pygame.draw.line(self.screen,(50,50,50),(int(self.prop*520+self.delta_x),int(self.prop*740+self.delta_y)),(int(self.prop*860+self.delta_x),int(self.prop*740+self.delta_y)),int(self.prop*5))
        texts = self.font.render(self.name,False,(0,0,0))
        size  = self.font.size(self.name)
        self.screen.blit(texts,(int(self.prop*530+self.delta_x),int(self.prop*730+self.delta_y)-size[1]))
        if self.vatss:
            self.vats()
        self.draw_box(self.drawing,self.menu)
        self.per_tick()

    def draw_box(self,op,menu=True):
        #draws a menu screen with option specified
        if op != None and menu:
            ops_size_x = []
            ops_size_y = []
            self.options = {}
            for i in [g[0] for g in op] :
                ops_size_x.append(self.font.size(i)[0])
                ops_size_y.append(self.font.size(i)[1])
            width = max(ops_size_x)
            prev=list(self.mpos)
            for i in range(len(op)):
                pygame.draw.polygon(self.screen,(150,150,150),(prev,
                                                              (prev[0]+width+int(self.prop*20),prev[1])
                                                              ,(prev[0]+width+int(self.prop*20),prev[1]-(ops_size_y[i]+int(self.prop*20))),
                                                              (prev[0],prev[1]-(ops_size_y[i]+int(self.prop*20)))),0)
                pygame.draw.polygon(self.screen,(120,120,120),(prev,
                                                      (prev[0]+width+int(self.prop*20),prev[1])
                                                      ,(prev[0]+width+int(self.prop*20),prev[1]-(ops_size_y[i]+int(self.prop*20))),
                                                      (prev[0],prev[1]-(ops_size_y[i]+int(self.prop*20)))),int(self.prop*5))
                self.screen.blit(self.font.render([g[0] for g in op][i],False,(0,0,0)),(prev[0]+int(self.prop*10),prev[1]-int(self.prop*10)-ops_size_y[i]))
                prev = (self.mpos[0],prev[1]-(ops_size_y[i]+int(self.prop*20)))
                self.options[((prev[0],(prev[0]+width+int(self.prop*20))),(prev[1]+(ops_size_y[i]+int(self.prop*20)),prev[1]))]=[g[1] for g in op][i]
            
            
            
            
    def right_click(self,mpos=None):
        #does all the calculation realting to right clicking (oly what weps will do so far)
        self.menu=False
        if mpos != None:
            self.mpos = mpos
        in_box = False
        print(self.mpos[1],int(self.prop*700+self.delta_x),int(self.prop*801+self.delta_y))
        if self.mpos[1] in range(int(self.prop*700+self.delta_y),int(self.prop*801+self.delta_y)):
                if self.mpos[0] in range(int(self.prop*320+self.delta_x),int(self.prop*421+self.delta_x)):
                    self.hand = "Left Hand"
                    in_box = True
                if self.mpos[0] in range(int(self.prop*860+self.delta_x),int(self.prop*961+self.delta_x)):
                    self.hand = "Right Hand"
                    in_box = True
        
        if in_box and not self.vatss and not self.chose_who:
            self.rhold = True
            if self.equipment[self.hand][0] == [None]:
                self.draw_box([["Punch","Attack"]])
                self.drawing = [["Punch","Attack"]]
            elif self.equipment[self.hand][0][0].atktype == "Melee":
                self.draw_box([["Melee Attack","Attack"],["Throw","Throw"]])
                self.drawing = [["Throw","Throw"],["Melee Attack","Attack"]]
            elif self.equipment[self.hand][0][0].atktype == "Ranged":
                self.draw_box([["Ranged Attack","Attack"],["Throw","Throw"]])
                self.drawing = [["Throw","Throw"],["Ranged Attack","Attack"]]
            self.menu = True
        else:
            self.drawing = None
            self.menu =False
    def left_click(self,enemies):
        print("HELLO",self.chose_who)
        #does the calcs for left clicking eg selecting from menu and vats and so on
        mpos = pygame.mouse.get_pos()
        if self.chose_who:
            self.whoo = useful_fucs.Get_target(mpos,enemies,self)
            #print(who)
            if self.whoo != None:
                self.vatss = True
                self.vats()
            self.chose_who = False
        elif self.vatss:
            if self.head_rekt.collidepoint(mpos):
                aimed_location = "Head"
            elif self.torso_rekt.collidepoint(mpos):
                aimed_location = "Torso"
            elif self.legs1_rekt.collidepoint(mpos):
                aimed_location = "Left Leg"
            elif self.legs2_rekt.collidepoint(mpos):
                aimed_location = "Right Leg"
            elif self.feet1_rekt.collidepoint(mpos):
                aimed_location=  "Left Foot"
            elif self.feet2_rekt.collidepoint(mpos):
                aimed_location = "Right Feet"
            elif self.larm_rekt.collidepoint(mpos):
                aimed_location = "Left Arm"
            elif self.rarm_rekt.collidepoint(mpos):
                aimed_location = "Right Arm"
            elif self.hand1_rekt.collidepoint(mpos):
                aimed_location = "Left Hand"
            elif self.hand2_rekt.collidepoint(mpos):
                aimed_location = "Right Hand"
            else:
                aimed_location = None
            
            self.attack(self.hand,self.whoo,aimed_location)
            self.vatss = False
            
        if self.menu and self.state == "Normal":
            for i in list(self.options.keys()):
                print(i)
                print(mpos)
                if mpos[0] >= i[0][0]  and mpos[0] <= i[0][1] and mpos[1] >= i[1][1] and mpos[1] <= i[1][0]:
                    print(self.options[i])
                    if self.options[i] == "Attack":
                        self.chose_who = True
                    else:
                        self.throw(self.hand,0,0)
        self.menu =False
    
    def per_tick(self):
        #the update per_tick on the health bars and such
        pygame.draw.line(self.screen,(50,50,50),(int(self.prop*520+self.delta_x),int(self.prop*760+self.delta_y)),(int(self.prop*860+self.delta_x),int(self.prop*760+self.delta_y)),int(self.prop*5))
        pygame.draw.line(self.screen,(255,0,0),(int(self.prop*523+self.delta_x),int(self.prop*750+self.delta_y)),(int(self.prop*857+self.delta_x),int(self.prop*750+self.delta_y)),int(self.prop*15))
        scale = int(334*self.health/100)
        if self.health>0:
            pygame.draw.line(self.screen,(0,255,0),(int(self.prop*523+self.delta_x),int(self.prop*750+self.delta_y)),(int(self.prop*(523+scale)+self.delta_x),int(self.prop*750+self.delta_y)),int(self.prop*15))
        texts = self.font_small.render(str(int(self.health)),False,(0,0,0))
        size  = self.font_small.size(str(self.health))
        self.screen.blit(texts,(int(self.prop*690+self.delta_x)-size[0]/2,int(self.prop*760+self.delta_y)-size[1]))

        pygame.draw.line(self.screen,(50,50,50),(int(self.prop*520+self.delta_x),int(self.prop*770+self.delta_y)),(int(self.prop*860+self.delta_x),int(self.prop*770+self.delta_y)),int(self.prop*5))
        pygame.draw.line(self.screen,(20,0,0),(int(self.prop*523+self.delta_x),int(self.prop*765+self.delta_y)),(int(self.prop*857+self.delta_x),int(self.prop*765+self.delta_y)),int(self.prop*7))
        scale = int(334*self.wound/100)
        if self.wound>0:
            pygame.draw.line(self.screen,(80,0,0),(int(self.prop*523+self.delta_x),int(self.prop*765+self.delta_y)),(int(self.prop*(523+scale)+self.delta_x),int(self.prop*765+self.delta_y)),int(self.prop*7))
        texts = self.font.render(self.state,False,(0,0,0))
        size  = self.font.size(self.state)
        self.screen.blit(texts,(int(self.prop*850+self.delta_x)-size[0],int(self.prop*730+self.delta_y)-size[1]))
    def resize(self):
        #deals with resizeing screen
        swidth = self.screen.get_width()
        sheight = self.screen.get_height()
        propw = swidth/1280
        proph  = sheight/800
        self.prop = min(propw,proph)
        self.font = pygame.font.SysFont("Palatino Linotype",int(self.prop*20))
        self.font_small = pygame.font.SysFont("Palatino Linotype",int(self.prop*15))
        self.delta_x = 640*(propw-self.prop)
        self.delta_y = 400*(proph-self.prop)
        pygame.draw.line(self.screen,(150,150,150),(self.delta_x,0),(self.delta_x,sheight),2)
        pygame.draw.line(self.screen,(150,150,150),(swidth-self.delta_x,0),(swidth-self.delta_x,sheight),2)
        pygame.draw.line(self.screen,(150,150,150),(0,self.delta_y),(swidth,self.delta_y),2)
        pygame.draw.line(self.screen,(150,150,150),(0,sheight-self.delta_y),(swidth,sheight-self.delta_y),2)
        self.head_rekt.center=(int(self.prop*612+self.delta_x)+self.head_rekt.width/2, int(self.prop*200+self.delta_y)+self.head_rekt.height/2)
        self.head_rekt.inflate(-self.head_rekt.width+int(self.prop*75),int(self.prop*88)-self.head_rekt.height)
        self.torso_rekt.center=(int(self.prop*600+self.delta_x)+self.torso_rekt.width/2, int(self.prop*288+self.delta_y)+self.torso_rekt.height/2)
        self.torso_rekt.inflate(-self.torso_rekt.width+int(self.prop*75),int(self.prop*88)-self.torso_rekt.height)
        self.legs1_rekt.center=(int(self.prop*600+self.delta_x)+self.legs1_rekt.width/2, int(self.prop*422+self.delta_y)+self.legs1_rekt.height/2)
        self.legs1_rekt.inflate(-self.legs1_rekt.width+int(self.prop*75),int(self.prop*88)-self.legs1_rekt.height)
        self.legs2_rekt.center=(int(self.prop*650+self.delta_x)+self.legs2_rekt.width/2, int(self.prop*422+self.delta_y)+self.legs2_rekt.height/2)
        self.legs2_rekt.inflate(-self.legs2_rekt.width+int(self.prop*75),int(self.prop*88)-self.legs2_rekt.height)
        self.feet1_rekt.center=(int(self.prop*560+self.delta_x)+self.feet1_rekt.width/2, int(self.prop*517+self.delta_y)+self.feet1_rekt.height/2)
        self.feet1_rekt.inflate(-self.feet1_rekt.width+int(self.prop*75),int(self.prop*88)-self.feet1_rekt.height)
        self.feet2_rekt.center=(int(self.prop*655+self.delta_x)+self.feet2_rekt.width/2, int(self.prop*517+self.delta_y)+self.feet2_rekt.height/2)
        self.feet2_rekt.inflate(-self.feet2_rekt.width+int(self.prop*75),int(self.prop*88)-self.feet2_rekt.height)
        self.larm_rekt.center=(int(self.prop*695+self.delta_x)+self.larm_rekt.width/2, int(self.prop*288+self.delta_y)+self.larm_rekt.height/2)
        self.larm_rekt.inflate(-self.larm_rekt.width+int(self.prop*75),int(self.prop*88)-self.larm_rekt.height)
        self.rarm_rekt.center=(int(self.prop*526+self.delta_x)+self.rarm_rekt.width/2, int(self.prop*288+self.delta_y)+self.rarm_rekt.height/2)
        self.rarm_rekt.inflate(-self.rarm_rekt.width+int(self.prop*75),int(self.prop*88)-self.rarm_rekt.height)
        self.hand1_rekt.center=(int(self.prop*759+self.delta_x)+self.hand1_rekt.width/2, int(self.prop*390+self.delta_y)+self.hand1_rekt.height/2)
        self.hand1_rekt.inflate(-self.hand1_rekt.width+int(self.prop*75),int(self.prop*88)-self.hand1_rekt.height)
        self.hand2_rekt.center=(int(self.prop*516+self.delta_x)+self.hand2_rekt.width/2, int(self.prop*390+self.delta_y)+self.hand2_rekt.height/2)
        self.hand2_rekt.inflate(-self.hand2_rekt.width+int(self.prop*75),int(self.prop*88)-self.hand2_rekt.height)
    def vats(self):
        #draws video automated targeting system?
        pygame.draw.polygon(self.screen,((100,150,100)),((int(self.prop*500+self.delta_x),int(self.prop*180+self.delta_y))
                                                    ,(int(self.prop*830+self.delta_x),int(self.prop*180+self.delta_y))
                                                    ,(int(self.prop*830+self.delta_x),int(self.prop*560+self.delta_y))
                                                    ,(int(self.prop*500+self.delta_x),int(self.prop*560+self.delta_y))),0)

        self.screen.blit(pygame.transform.scale(self.head_im, (int(self.prop*75),int(self.prop*88))), (int(self.prop*612+self.delta_x), int(self.prop*200+self.delta_y)))
        self.screen.blit(pygame.transform.scale(self.torso_im, (int(self.prop*105),int(self.prop*134))), (int(self.prop*600+self.delta_x), int(self.prop*288+self.delta_y)))
        self.screen.blit(pygame.transform.scale(self.legs1_im, (int(self.prop*54),int(self.prop*95))), (int(self.prop*600+self.delta_x), int(self.prop*422+self.delta_y)))
        self.screen.blit(pygame.transform.scale(self.legs2_im, (int(self.prop*54),int(self.prop*95))), (int(self.prop*650+self.delta_x), int(self.prop*422+self.delta_y)))
        self.screen.blit(pygame.transform.scale(self.feet1_im, (int(self.prop*88),int(self.prop*29))), (int(self.prop*560+self.delta_x), int(self.prop*517+self.delta_y)))
        self.screen.blit(pygame.transform.scale(self.feet2_im, (int(self.prop*88),int(self.prop*29))), (int(self.prop*655+self.delta_x), int(self.prop*517+self.delta_y)))
        self.screen.blit(pygame.transform.scale(self.larm_im, (int(self.prop*84),int(self.prop*102))), (int(self.prop*695+self.delta_x), int(self.prop*288+self.delta_y)))
        self.screen.blit(pygame.transform.scale(self.rarm_im, (int(self.prop*84),int(self.prop*102))), (int(self.prop*526+self.delta_x), int(self.prop*288+self.delta_y)))
        self.screen.blit(pygame.transform.scale(self.hand1_im, (int(self.prop*39),int(self.prop*33))), (int(self.prop*759+self.delta_x), int(self.prop*390+self.delta_y)))
        self.screen.blit(pygame.transform.scale(self.hand2_im, (int(self.prop*39),int(self.prop*33))), (int(self.prop*516+self.delta_x), int(self.prop*390+self.delta_y)))

        
            
        
        

        
        
            
            
 
    
        
        
        
        

        
