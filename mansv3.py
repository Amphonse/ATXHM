import numpy as np
import random,pygame

def convert_iso_dots(r):
    #converts grid coordinates to a blit friendly set of iso coordinates.
    y = r[1]*32
    x = r[0]*32
    x +=32
    y += 32
    if (r[0]-(r[0]-int(r[0])))%2 == 0:
        y -= 16

    return (int(x),int(y))

# in general do not need to check if items are in inv due to graphics


class items():
    def __init__(self,cost,weight,name):
        self.name = name
        self.cost = cost
        self.weight = weight 

    def draw_self(self,screen):
        pygame.draw.circle(screen, (255,0,255), convert_iso_dots(self.coords), 3)

class armor(items):
    def __init__(self,cost,weight,name,armor,location,health,cmod):
        super().__init__(cost,weight,name)
        self.armor = armor
        self.location = location
        self.health = health
        self.cmod = cmod
        self.maxhealth = health
#if they're on the ground, they have coords. Otherwise, the coords are = None
class weepons(items):
    def __init__(self,cost,weight,name,dtype,atktype,dmg,ranges=0,coords= None):
        self.ranges = ranges
        super().__init__(cost,weight,name)
        self.dtype = dtype
        self.atktype = atktype
        self.dmg = dmg
        self.coords = coords

class consumables(items):
    def __init__(self,cost,weight,name,charges,types,coords= None):
        super().__init__(cost,weight,name)
        self.charges = charges
        self.coords = coords
        
class shield(weepons):
    def __init_(self,cost,weight,name,dtype,atktype,dmg,shielding):
        super().__init__(cost,weight,name,dtype,atktype,dmg)
        self.shielding = shielding

class mans():
    def __init__(self,name,screen):
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
        #self.endurance = 100
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
        self.rhold = False
        self.resize()
    def get_hit(self,location,dmg,dtype):
        #print(self.limbs[loc])
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
        #if self.health<0:
        #    self.state = "Dead"
        #    print(self.state)
        #elif self.health<30:
        #    self.state = "Unconcious"
        #    print(self.state)
        #elif (dmg*self.limbs[location][1])*100/self.endurance > 50:
        #    self.state = "Unconcious"
        #    print(self.state)
        if self.health<0:
            self.health=0
        self.mupdate()
    def mupdate(self):
        #self.actions = 0
        if self.state == "Normal":
            if self.health*self.endurance/100 < self.wound:
                self.state = "Dead"
                print(self.state)
            elif self.health*self.endurance/100 < self.shock+self.wound*2:
                self.state = "Unconcious"
                print(self.state)
            else:
                pass
                #print("Awake")
        elif self.state == "Unconcious":
            #print(self.wound)
            #print(self.health*self.endurance/100)
            if self.health*self.endurance/100 < self.wound:
                self.state = "Dead"
                print(self.state)
            elif self.health*self.endurance/100 > self.shock*2+self.wound*10:
                self.state = "Normal"
                print(self.name+" wakes up")
            else:
                pass
                #print("Still Down")
        self.wound += (self.wounds-1)
        self.shock -= (self.endurance/20)
        if self.wound < 0:
            self.wound = 0
        if self.wound > 100:
            self.wound = 100
        if self.shock < 0:
            self.shock = 0
    def attack(self,hand,who,aimed_location,turns_aimed = 0,dist=0):      
        wep = self.equipment[hand][0][0]
        if wep == None:
            wep = weepons(0,0,"Fisto","Crushing","Melee",5)
        roll = random.random()*100
        if wep.atktype == "Melee":
            self.margina = self.melee-roll
        elif wep.atktype == "Ranged":
            #have some mod for dist and turns aimed
            self.margina = self.ranged-roll
        who.defend()
        if who.margind > self.margina:
            print(self.name+" missed "+who.name)
        else:
            who.get_hit(aimed_location,wep.dmg,wep.dtype)


    def defend(self):
        #only if normal
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
                
    def invman(self,what,froms,to):
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
        #print(self.equipment)
    def pick_up(self,what):
        #check if on floor same as below
        if self.equipment["Left Hand"][0] == [None]:
            self.equipment["Left Hand"][0] = [what]
            what.coords = None
        elif self.equipment["Right Hand"][0] == [None]:
            self.equipment["Right Hand"][0] = [what]
            what.coords = None
        else:
            print(self.name+ " has no free hands")
    def throw(self,withs,what,where):
        #accuracy off thrown
        #range off strn
        #do not need to check if on floor as no option should come up if not
        self.equipment[withs][0] = [None]
        #store on appropriate tile
    def reset(self):
        #draws basic self.screen
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
        self.right_click(hold = self.rhold)
        if self.vatss:
            self.vats()
        self.per_tick()

    def draw_box(self,op):
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
            self.options[(prev,(prev[0]+width+int(self.prop*20)),(prev[1],prev[1]-(ops_size_y[i]+int(self.prop*20))))]=[g[1] for g in op][i]
            
            
            
            
    def right_click(self,mpos=None,hold = True):
        #solution is to have a function the draws a box
        #like this currently does but for a more gneral
        #case then call that draw function here then set
        #a var true when rclicked in box flase otherwise
        #false when lclick and draw when var
        #is true but this will take awhile so can do this later
        #what happend when right muse button is clicked
        if mpos != None:
            self.mpos = mpos
        if hold:
            in_box = False
            print(self.mpos[1],int(self.prop*700+self.delta_x),int(self.prop*801+self.delta_y))
            if self.mpos[1] in range(int(self.prop*700+self.delta_y),int(self.prop*801+self.delta_y)):
                    if self.mpos[0] in range(int(self.prop*320+self.delta_x),int(self.prop*421+self.delta_x)):
                        self.hand = "Left Hand"
                        in_box = True
                    if self.mpos[0] in range(int(self.prop*860+self.delta_x),int(self.prop*961+self.delta_x)):
                        self.hand = "Right Hand"
                        in_box = True
            
            if in_box:
                self.rhold = True
                if self.equipment[self.hand][0] == [None]:
                    texts = self.font.render("Punch",False,(0,0,0))
                    size  = self.font.size("Punch")
                    
                    pygame.draw.polygon(self.screen,(150,150,150),(self.mpos,
                                                          (self.mpos[0]+size[0]+int(self.prop*20),self.mpos[1])
                                                          ,(self.mpos[0]+size[0]+int(self.prop*20),self.mpos[1]-(size[1]+int(self.prop*20))),
                                                          (self.mpos[0],self.mpos[1]-(size[1]+int(self.prop*20)))),0)
                    pygame.draw.polygon(self.screen,(120,120,120),(self.mpos,
                                                          (self.mpos[0]+size[0]+int(self.prop*20),self.mpos[1])
                                                          ,(self.mpos[0]+size[0]+int(self.prop*20),self.mpos[1]-(size[1]+int(self.prop*20))),
                                                          (self.mpos[0],self.mpos[1]-(size[1]+int(self.prop*20)))),int(self.prop*5))
                    self.screen.blit(texts,(self.mpos[0]+int(self.prop*10),self.mpos[1]-int(self.prop*10)-size[1]))
                    self.options={ ((self.mpos[0],self.mpos[0]+size[0]+int(self.prop*20)),(self.mpos[1],self.mpos[1]-(size[1]+int(self.prop*20)))) :"Attack"}
                elif self.equipment[self.hand][0][0].atktype == "Melee":
                    op1 = self.font.render("Melee Attack",False,(0,0,0))
                    op2 = self.font.render("Throw",False,(0,0,0))
                    op3 = self.font.render("Drop",False,(0,0,0))
                    
                    size1  = self.font.size("Melee Attack")
                    size2  = self.font.size("Throw")
                    size3  = self.font.size("Drop")
                    heights = size1[1]+size2[1]+size3[1]+int(self.prop*20)
                    widths = max(size1[0],size2[0],size3[0])
                    pygame.draw.polygon(self.screen,(150,150,150),(self.mpos,
                                                          (self.mpos[0]+widths+int(self.prop*20),self.mpos[1])
                                                          ,(self.mpos[0]+widths+int(self.prop*20),self.mpos[1]-(heights+int(self.prop*20))),
                                                          (self.mpos[0],self.mpos[1]-(heights+int(self.prop*20)))),0)
                    pygame.draw.polygon(self.screen,(120,120,120),(self.mpos,
                                                          (self.mpos[0]+widths+int(self.prop*20),self.mpos[1])
                                                          ,(self.mpos[0]+widths+int(self.prop*20),self.mpos[1]-(heights+int(self.prop*20))),
                                                          (self.mpos[0],self.mpos[1]-(heights+int(self.prop*20)))),int(self.prop*5))
                    self.screen.blit(op3,(self.mpos[0]+int(self.prop*10),self.mpos[1]-int(self.prop*10)-size3[1]))
                    self.screen.blit(op2,(self.mpos[0]+int(self.prop*10),self.mpos[1]-int(self.prop*20)-size2[1]-size3[1]))
                    self.screen.blit(op1,(self.mpos[0]+int(self.prop*10),self.mpos[1]-int(self.prop*10)-heights))
                    pygame.draw.line(self.screen,(120,120,120),(self.mpos[0],self.mpos[1]-size1[1]-int(self.prop*17.5)),(self.mpos[0]+widths+int(self.prop*20),self.mpos[1]-size1[1]-int(self.prop*17.5)),int(self.prop*5))
                    pygame.draw.line(self.screen,(120,120,120),(self.mpos[0],self.mpos[1]-heights+int(self.prop*12.5)),(self.mpos[0]+widths+int(self.prop*20),self.mpos[1]-heights+int(self.prop*12.5)),int(self.prop*5))
                    self.options={ ((self.mpos[0],self.mpos[0]+widths+int(self.prop*20)),(self.mpos[1],self.mpos[1]-size1[1]-int(self.prop*17.5))) :"Throw",
                                   ((self.mpos[0],self.mpos[0]+widths+int(self.prop*20)),(self.mpos[1]-size1[1]-int(self.prop*17.5),self.mpos[1]-heights+int(self.prop*12.5))) :"Throw",
                                   ((self.mpos[0],self.mpos[0]+widths+int(self.prop*20)),(self.mpos[1]-heights+int(self.prop*12.5),self.mpos[1]-self.mpos[1]-(heights+int(self.prop*20)))) :"Attack"}
                elif self.equipment[self.hand][0][0].atktype == "Ranged":
                    op1 = self.font.render("Ranged Attack",False,(0,0,0))
                    op2 = self.font.render("Throw",False,(0,0,0))
                    op3 = self.font.render("Drop",False,(0,0,0))
                    
                    size1  = self.font.size("Ranged Attack")
                    size2  = self.font.size("Throw")
                    size3  = self.font.size("Aim")
                    heights = size1[1]+size2[1]+size3[1]+int(self.prop*20)
                    widths = max(size1[0],size2[0],size3[0])
                    pygame.draw.polygon(self.screen,(150,150,150),(mpos,
                                                          (mpos[0]+widths+int(self.prop*20),mpos[1])
                                                          ,(mpos[0]+widths+int(self.prop*20),mpos[1]-(heights+int(self.prop*20))),
                                                          (mpos[0],mpos[1]-(heights+int(self.prop*20)))),0)
                    pygame.draw.polygon(self.screen,(120,120,120),(mpos,
                                                          (mpos[0]+widths+int(self.prop*20),mpos[1])
                                                          ,(mpos[0]+widths+int(self.prop*20),mpos[1]-(heights+int(self.prop*20))),
                                                          (mpos[0],mpos[1]-(heights+int(self.prop*20)))),int(self.prop*5))
                    self.screen.blit(op3,(mpos[0]+int(self.prop*10),mpos[1]-int(self.prop*10)-size3[1]))
                    self.screen.blit(op2,(mpos[0]+int(self.prop*10),mpos[1]-int(self.prop*20)-size2[1]-size3[1]))
                    self.screen.blit(op1,(mpos[0]+int(self.prop*10),mpos[1]-int(self.prop*10)-heights))
                    pygame.draw.line(self.screen,(120,120,120),(mpos[0],mpos[1]-size1[1]-int(self.prop*17.5)),(mpos[0]+widths+int(self.prop*20),mpos[1]-size1[1]-int(self.prop*17.5)),int(self.prop*5))
                    pygame.draw.line(self.screen,(120,120,120),(mpos[0],mpos[1]-heights+int(self.prop*12.5)),(mpos[0]+widths+int(self.prop*20),mpos[1]-heights+int(self.prop*12.5)),int(self.prop*5))
                    self.options={ ((mpos[0],mpos[0]+widths+int(self.prop*20)),(mpos[1],mpos[1]-size1[1]-int(self.prop*17.5))) :"Throw",
                                   ((mpos[0],mpos[0]+widths+int(self.prop*20)),(mpos[1]-size1[1]-int(self.prop*17.5),mpos[1]-heights+int(self.prop*12.5))) :"Throw",
                                   ((mpos[0],mpos[0]+widths+int(self.prop*20)),(mpos[1]-heights+int(self.prop*12.5),mpos[1]-mpos[1]-(heights+int(self.prop*20)))) :"Attack"}
            return True
    def left_click(self,who,menu):
        self.rhold = False
        mpos = pygame.mouse.get_pos()
        if self.vatss:
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
                aimed_location  = "Torso"
            
            self.attack(self.hand,who,aimed_location)
            self.vatss = False
        if menu:
            for i in list(self.options.keys()):
                print(i)
                print(mpos)
                if mpos[0] >= i[0][0]  and mpos[0] <= i[0][1] and mpos[1] >= i[1][1] and mpos[1] <= i[1][0]:
                    #print(self.options[i])
                    if self.options[i] == "Attack":
                        self.vats()
                        self.vatss = True
                    else:
                        self.throw(self.hand,0,0)
    
    def per_tick(self):
        #520,860
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
        #print(self.delta_y)
    def vats(self):#dont call this plz
    #set_colorkey((255,255,255))
    #image.load(name).convert()
    #screen.blit(image,coords)
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
        pygame.display.update()

        
            
        
        

        
        
            
            
 
    
        
        
        
        

        
