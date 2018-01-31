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
    def __init__(self,cost,weight,name,dtype,atktype,dmg,coords= None):
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
    def __init__(self,name):
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
        self.equipment = {"Left Hand":[[None],1],"Right Hand":[[weepons(0,0,"The pow bow wow","Impaling","Ranged",20)],1],"Back":[[consumables(0,0,"Arrers",10,"Ammo")],5],"Belt":[[weepons(0,0,"Dagger","Cutting","Melee",10)],2]}
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
    def mupdate(self):
        self.actions = 0
        if self.state == "Normal":
            roll = random.random()*100
            if self.health*self.endurance/100 < self.shock+self.wound*2:
                self.state = "Unconcious"
                print(self.state)
            elif self.health*self.endurance/100 < self.wound:
                self.state = "Dead"
                print(self.state)
            else:
                print("Awake")
        elif self.state == "Unconcious":
            #print(self.wound)
            #print(self.health*self.endurance/100)
            roll = random.random()*100
            if self.health*self.endurance/100 < self.wound:
                self.state = "Dead"
                print(self.state)
            elif self.health*self.endurance/100 > self.shock*2+self.wound*10:
                self.state = "Normal"
                print(self.name+" wakes up")
            else:
                print("Still Down")
        self.wound += (self.wounds-1)
        self.shock -= (self.endurance/20)
        if self.wound < 0:
            self.wound = 0
        if self.shock < 0:
            self.shock = 0
    def attack(self,hand,who,aimed_location = "Torso",turns_aimed = 0,dist=0):
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
        self.equipment["Left Hand"][0] = [None]
        #store on appropriate tile
        
        
            
            
        
    
    
        
        
        
        

        
