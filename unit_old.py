import math,path_iso,pygame,path_iso_copy
def convert_iso(r):
    #converts grid coordinates to a blit friendly set of iso coordinates.
    y = r[1]*32
    x = r[0]*32
    y -= 16
    if (r[0]-(r[0]-int(r[0])))%2 == 0:
        y -= 16

    return (int(x),int(y))

def convert_iso_dots(r):
    #converts grid coordinates to a blit friendly set of iso coordinates.
    y = r[1]*32
    x = r[0]*32
    x +=32
    #y += 16
    if (r[0]-(r[0]-int(r[0])))%2 == 0:
        y -= 16

    return (int(x),int(y))

def detect_clicked(pos):
    posl = list(pos)
    #first of all make the x an even number, as for odd x, the equation != 0.
    if posl[0]%2 != 0:
        posl[0] += 1
    #now find y2:
    Ytwo_found = False
    while Ytwo_found == False:
        l = ((posl[1]+0.5*posl[0]-16)/32)%1
        if l == 0:
            Ytwo = posl[1]+0.5*posl[0]
            Ytwo_found = True
            left_ytwo = posl[1]
        else:
            posl[1]-=1
    
    #now find y1
    posl[1] = list(pos)[1]
    Yone_found = False
    while Yone_found == False:
        l = ((posl[1]-0.5*posl[0]-16)/32)%1
        if l == 0:
            Yone = posl[1]-0.5*posl[0]
            Yone_found = True
            left_yone = posl[1]
        else:
            posl[1]+=1
    #now check to see if it was on the RHS:
    #print(left_yone-left_ytwo)
    if left_yone-left_ytwo >= 32:
        #if it is, then:
        posl[0] -= left_yone-left_ytwo-34
        #convert x to even again
        if posl[0]%2 != 0:
            posl[0] += 1
        posl[1] = list(pos)[1]
        #now find y2:
        Ytwo_found = False
        while Ytwo_found == False:
            l = ((posl[1]+0.5*posl[0]-16)/32)%1
            if l == 0:
                Ytwo = posl[1]+0.5*posl[0]
                Ytwo_found = True
                left_ytwo = posl[1]
            else:
                posl[1]-=1
        
        #now find y1
        posl[1] = list(pos)[1]
        Yone_found = False
        while Yone_found == False:
            l = ((posl[1]-0.5*posl[0]-16)/32)%1
            if l == 0:
                Yone = posl[1]-0.5*posl[0]
                Yone_found = True
                left_yone = posl[1]
            else:
                posl[1]+=1
        

    one = (Yone-16)/32
    two = (Ytwo-16)/32
    x_coord = two-one
    y_sum = (one+two)/2.0
    if y_sum % 1 != 0:
        y_sum -= 0.5
    y_coord = y_sum
    #print(x_coord,y_coord)
    return [x_coord,y_coord]


#TWO TYPES OF ENEMY. RANGED AND MELEE. MELEE WANTS TO GET UP CLOSE.
#RANGED WANTS TO GET INTO RANGE.
#WILL PRIORITISE LOW HEALTH UNITS.
class enemy:
    def __init__(self,image,speed,coords,etype):
        self.image = pygame.image.load(image).convert()
        self.rect = self.image.get_rect()
        self.rect = coords
        self.speed = speed
        self.move_points = speed
        self.action_points = int(speed/2.0)#number of actions that ca be taken in a turn. this includes attacks.
        self.coords = coords
        self.path = []
        #self.stage = 0
        #self.move_vector = [0,0]
        self.image.set_colorkey((255,255,255))
        self.etype = etype#0 is melee,1 is ranged
        
    def new_turn(self):
        self.move_points = self.speed
        
    def move_to(self,coords,grid,tiles,units):
        print(self.coords)
        self.path = path_iso_copy.Pathfinding(self.coords,coords,grid,tiles)
        del self.path[0]
        if self.path == None:
            pass
        else:
            if self.move_points > 0:
                if len(self.path)>self.move_points:
                    ok_to_move = True
                    self.path.reverse()
                    for i in units:
                        if i.coords != list(self.path[self.move_points]):
                            print("enemy",i.coords,list(self.path[self.move_points]))
                            print("lol")
                            self.coords = list(self.path[self.move_points])
                            
                        else:
                            self.coords = list(self.path[self.move_points-1])
                    
                else:
                    print(self.path)
                    ok_to_move = True
                    for i in units:
                        if i.coords != list(self.path[0]):
                            print("enemy",i.coords,list(self.path[0]))
                            self.coords = list(self.path[0])
                            
                        else:
                            self.coords = list(self.path[0+1])
                    print(self.coords)
                    
                    
    def draw_self(self,screen):
        screen.blit(self.image,convert_iso(self.coords))




class unit:
    def __init__(self,image,speed,coords):
        self.image = pygame.image.load(image).convert()
        self.rect = self.image.get_rect()
        self.rect = coords
        self.speed = speed
        self.move_points = speed
        self.coords = coords
        self.path = []
        #self.stage = 0
        #self.move_vector = [0,0]
        self.image.set_colorkey((255,255,255))
        self.selected = False
        #self.dm = 0
        

    def new_turn(self):
        self.move_points = self.speed
        
    def move_to(self,coords,grid,tiles,units):
        print(self.coords)
        self.path = path_iso_copy.Pathfinding(self.coords,coords,grid,tiles)
        if self.path == None:
            pass
        else:
            if self.move_points > 0:
                if len(self.path)>self.move_points:
                    ok_to_move = True
                    self.path.reverse()
                    for i in units:
                        if i.coords != list(self.path[self.move_points]):
                            print("Loool",i.coords,list(self.path[self.move_points]))
                            
                        else:
                            ok_to_move = False
                    if ok_to_move:
                        self.coords = list(self.path[self.move_points])
                        self.move_points = 0
                else:
                    print(self.path)
                    ok_to_move = True
                    for i in units:
                        if i.coords != list(self.path[0]):
                            print("Loool",i.coords,list(self.path[0]))
                            
                        else:
                            ok_to_move = False
                    if ok_to_move:
                        self.coords = list(self.path[0])
                        self.move_points -= len(self.path)-1
                    print(self.coords)
                #self.stage = 0

    def draw_self(self,screen):
        screen.blit(self.image,convert_iso(self.coords))
        if self.selected:
            if self.path:
                
                for i in self.path:
                    if len(self.path)-self.path.index(i) > self.move_points+1:
                        pygame.draw.circle(screen, (255,0,0), convert_iso_dots((i[0],i[1]+1)), 1)
                    else:
                        pygame.draw.circle(screen, (255,255,0), convert_iso_dots((i[0],i[1]+1)), 1)

    def det_selected(self,pos):
        if self.coords == detect_clicked(pos):
            self.selected = True
        else:
            self.selected = False
            self.path = None
        
    def test_path(self,pos,grid,tiles):
         self.path = path_iso_copy.Pathfinding(self.coords,pos,grid,tiles)
            
    def update(self):
        pass
        
        #if tuple(self.coords) == self.path[-1]:
        #    pass
        #else:
        #    
        #    
            #normaliser = math.sqrt(self.move_vector[0]**2+self.move_vector[1]**2)
        #    try:
        #        self.move_vector[0] = self.move_vector[0]
        #        self.move_vector[1] = self.move_vector[1]
        #    except ZeroDivisionError:
        #        self.move_vector[0] = 0
        #        self.move_vector[1] = 0
        #        
        #    
        #    print(math.sqrt(self.move_vector[0]**2+self.move_vector[1]**2))
        #    self.coords[0] += 0.01*self.move_vector[0]
        #    self.coords[1] += 0.01*self.move_vector[1]
        #    self.coords[0] = round(self.coords[0],11)
        #    self.coords[1] = round(self.coords[1],11)
        #    print(self.coords,self.path[self.stage],self.move_vector)
            
        #    if tuple(self.coords) == self.path[self.stage]:
        #        self.stage += 1
        #        self.move_vector[0] = self.path[self.stage][0]-self.coords[0]
        #        self.move_vector[1] = self.path[self.stage][1]-self.coords[1]
            
