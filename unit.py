import random,math,path_iso,pygame,path_iso_copy,numpy as np,mans
    
def convert_iso(r,mve_vect):
    #converts grid coordinates to a blit friendly set of iso coordinates.
    y = r[1]*32 + mve_vect[1]*16
    x = r[0]*32 + mve_vect[0]*32
    y -= 16
    if (r[0]-(r[0]-int(r[0])))%2 == 0:
        y -= 16

    return (int(x),int(y))

def convert_grid(r):
    #converts iso coordinates to a click detector set of grid coordinates.
    y = int(r[1]/32)
    x = int(r[0]/32)
    if r[0]%2 != 0:
        y -= 0.5

    return [x,y]

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
class Enemy(mans.mans):
    def __init__(self,image,speed,coords,etype,name,screen):
        self.image = pygame.image.load(image).convert()
        self.rect = self.image.get_rect()
        self.rect = coords
        self.speed = speed
        self.move_points = speed
        self.action_points = int(speed/2.0)#number of actions that ca be taken in a turn. this includes attacks.
        self.coords = coords
        self.path = []
        self.stage = 1
        self.move_vector = [0,0]
        self.image.set_colorkey((255,255,255))
        self.etype = etype#0 is melee,1 is ranged
        self.moving = False
        self.ok_to_move = False

        super().__init__(name,screen)

                
    def new_turn(self):
        self.move_points = self.speed

        #Matyas's update method
        self.mupdate()
        
                
    def move_to(self,coords,nodes,distances,units,enemies,tiles):#self,coords,nodes,distances,units,enemies,tiles
        if self.state == "Normal":
            self.path = path_iso_copy.Pathfinding(self.coords,coords,nodes,distances)
            for g in units:
                #print("WTFFFF",self.path[0],tuple(g.coords))
                if self.path[0] == tuple(g.coords):
                    #print("wow")
                    del self.path[0]
            try:
                self.rev_path = []
                for i in self.path:
                    self.rev_path.append(i)
                self.rev_path.reverse()
            except:
                pass
                    
            if self.path == None:
                pass
            else:
                if self.move_points > 0:
                    if len(self.path)>self.move_points:
                        self.ok_to_move = True
                        self.path.reverse()
                        for i in enemies:
                            if i.coords != list(self.path[self.move_points]):
                                #print("Loool",i.coords,list(self.path[self.move_points]))
                                pass
                            else:
                                self.ok_to_move = False
                        #if ok_to_move:
                        #    self.coords = list(self.path[self.move_points])
                        #    self.move_points = 0
                    else:
                        #print(self.path)
                        self.ok_to_move = True
                        for i in enemies:
                            if i.coords != list(self.path[0]):
                                #print("Loool",i.coords,list(self.path[0]))
                                pass
                            else:
                                self.ok_to_move = False
                        #if ok_to_move:
                        #    self.coords = list(self.path[0])
                        #    self.move_points -= len(self.path)-1
                        #print(self.coords)
                    #self.stage = 0
            if self.ok_to_move:
                self.moving = True
        
                    
                    
    def draw_self(self,screen,tiles,prop,delta_x,delta_y):
        for tile in tiles:
            if self.coords == tile.coords:
                if tile.visited == False:
                    pass
                else:
                    blit_coords = convert_iso(self.coords,self.move_vector)
                    screen.blit(pygame.transform.scale(self.image,(int(64*prop),int(64*prop))),(int(blit_coords[0]*prop+delta_x),int(blit_coords[1]*prop+delta_y)))
        
        
    def update(self):
        if self.state == "Normal":
            if self.ok_to_move:
                if self.path != None:
                    #print(self.rev_path)
                    if tuple(self.coords) == self.rev_path[-1]:
                        self.stage = 1
                        self.path = None
                        self.moving = False
                    else:
                        if self.move_points <= 0:
                            self.stage = 1
                            self.path = None
                            self.moving = False
                        else:
                            if self.coords[0]%2 == 0: #for starting on even (un-shifted) tiles.
                                #print(self.rev_path[self.stage])
                                if self.rev_path[self.stage][1] == self.coords[1]:#if they're on the same y...
                                    if self.rev_path[self.stage][0] < self.coords[0]:#if its bottom left...
                                        self.move_vector[0] -= 0.1
                                        self.move_vector[1] += 0.1
                                        self.move_vector[0] = round(self.move_vector[0],1)
                                        self.move_vector[1] = round(self.move_vector[1],1)
                                        
                                        #print("move vector!",self.move_vector)
                                        if math.sqrt(self.move_vector[0]**2) == 1 and math.sqrt(self.move_vector[1]**2) == 1:
                                            self.stage += 1
                                            self.coords[0]-=1
                                            self.move_vector = [0,0]
                                            self.move_points -= 1
                                    elif self.rev_path[self.stage][0] > self.coords[0]:#if its bottom right...
                                        self.move_vector[0] += 0.1
                                        self.move_vector[1] += 0.1
                                        self.move_vector[0] = round(self.move_vector[0],1)
                                        self.move_vector[1] = round(self.move_vector[1],1)
                                        
                                        #print("move vector!",self.move_vector)
                                        if math.sqrt(self.move_vector[0]**2) == 1 and math.sqrt(self.move_vector[1]**2) == 1:
                                            self.stage += 1
                                            self.coords[0]+=1
                                            self.move_vector = [0,0]
                                            self.move_points -= 1
                                elif self.rev_path[self.stage][1] != self.coords[1]:#if they're not on the same y...
                                   # print("CHANGING Y")
                                    if self.rev_path[self.stage][0] < self.coords[0]:#if its top left...
                                        self.move_vector[0] -= 0.1
                                        self.move_vector[1] -= 0.1
                                        self.move_vector[0] = round(self.move_vector[0],1)
                                        self.move_vector[1] = round(self.move_vector[1],1)
                                       # print("move vector!",self.move_vector)
                                        if math.sqrt(self.move_vector[0]**2) == 1 and math.sqrt(self.move_vector[1]**2) == 1:
                                            self.stage += 1
                                            self.coords[0]-=1
                                            self.coords[1]-=1
                                            self.move_vector = [0,0]
                                            self.move_points -= 1
                                    elif self.rev_path[self.stage][0] > self.coords[0]:#if its top right...
                                        self.move_vector[0] += 0.1
                                        self.move_vector[1] -= 0.1
                                        self.move_vector[0] = round(self.move_vector[0],1)
                                        self.move_vector[1] = round(self.move_vector[1],1)
                                       # print("move vector!",self.move_vector)
                                        if math.sqrt(self.move_vector[0]**2) == 1 and math.sqrt(self.move_vector[1]**2) == 1:
                                            self.stage += 1
                                            self.coords[0]+=1
                                            self.coords[1]-=1
                                            self.move_vector = [0,0]
                                            self.move_points -= 1
                            elif self.coords[0]%2 != 0:#for starting on odd (down shifted) tiles.
                                
                               # print(self.rev_path[self.stage])
                                if self.rev_path[self.stage][1] == self.coords[1]:#if they're on the same y...
                                    if self.rev_path[self.stage][0] < self.coords[0]:#if its top left...
                                        self.move_vector[0] -= 0.1
                                        self.move_vector[1] -= 0.1
                                        self.move_vector[0] = round(self.move_vector[0],1)
                                        self.move_vector[1] = round(self.move_vector[1],1)
                                        #print("move vector!",self.move_vector)
                                        if math.sqrt(self.move_vector[0]**2) == 1 and math.sqrt(self.move_vector[1]**2) == 1:
                                            self.stage += 1
                                            self.coords[0]-=1
                                            self.move_vector = [0,0]
                                            self.move_points -= 1
                                    elif self.rev_path[self.stage][0] > self.coords[0]:#if its top right...
                                        self.move_vector[0] += 0.1
                                        self.move_vector[1] -= 0.1
                                        self.move_vector[0] = round(self.move_vector[0],1)
                                        self.move_vector[1] = round(self.move_vector[1],1)
                                        #print("move vector!",self.move_vector)
                                        if math.sqrt(self.move_vector[0]**2) == 1 and math.sqrt(self.move_vector[1]**2) == 1:
                                            self.stage += 1
                                            self.coords[0]+=1
                                            self.move_vector = [0,0]
                                            self.move_points -= 1
                                elif self.rev_path[self.stage][1] != self.coords[1]:#if they're not on the same y...
                                    #print("CHANGING Y")
                                    if self.rev_path[self.stage][0] < self.coords[0]:#if its bottom left...
                                        self.move_vector[0] -= 0.1
                                        self.move_vector[1] += 0.1
                                        self.move_vector[0] = round(self.move_vector[0],1)
                                        self.move_vector[1] = round(self.move_vector[1],1)
                                       # print("move vector!",self.move_vector)
                                        if math.sqrt(self.move_vector[0]**2) == 1 and math.sqrt(self.move_vector[1]**2) == 1:
                                            self.stage += 1
                                            self.coords[0]-=1
                                            self.coords[1]+=1
                                            self.move_vector = [0,0]
                                            self.move_points -= 1
                                    elif self.rev_path[self.stage][0] > self.coords[0]:#if its bottom right...
                                        self.move_vector[0] += 0.1
                                        self.move_vector[1] += 0.1
                                        self.move_vector[0] = round(self.move_vector[0],1)
                                        self.move_vector[1] = round(self.move_vector[1],1)
                                       # print("move vector!",self.move_vector)
                                        if math.sqrt(self.move_vector[0]**2) == 1 and math.sqrt(self.move_vector[1]**2) == 1:
                                            self.stage += 1
                                            self.coords[0]+=1
                                            self.coords[1]+=1
                                            self.move_vector = [0,0]
                                            self.move_points -= 1





class Unit(mans.mans):
    def __init__(self,image,speed,coords,name,screen):
        self.image = pygame.image.load(image).convert()
        self.rect = self.image.get_rect()
        self.rect = coords
        self.speed = speed
        self.move_points = speed
        self.coords = coords
        self.path = []
        self.stage = 1
        self.move_vector = [0,0]
        self.image.set_colorkey((255,255,255))
        self.selected = False
        self.ok_to_move = False
        self.test_path_l = []
        self.moving = False
        super().__init__(name,screen)
        #self.man = mans.mans(name,screen)
        self.old_pos_test = [0,0]

    
                
    def new_turn(self):
        self.move_points = self.speed
        self.path = None
        self.moving = False
        self.actions = 0



        #Matyas's Update method
        self.mupdate()
        
    def move_to(self,coords,nodes,distances,units,enemies,tiles):
        print(self.coords)

        
        
        self.path = path_iso_copy.Pathfinding(self.coords,coords,nodes,distances)
        try:
            self.rev_path = []
            for i in self.path:
                self.rev_path.append(i)
            self.rev_path.reverse()
        except:
            pass
        if self.path != None:
            for i in tiles:
                if i.is_Passable == False:
                    if tuple(i.coords) == tuple(coords):
                        self.path = None
                        self.ok_to_move = False
                        self.moving = False
                            
        if self.path == None:
            self.path = None
            self.ok_to_move = False
            self.moving = False
        else:
            
            if self.move_points > 0:
                if len(self.path)>self.move_points:
                    self.ok_to_move = True
                    self.path.reverse()
                    for i in units:
                        if i.coords != list(self.path[self.move_points]):
                            #print("Loool",i.coords,list(self.path[self.move_points]))
                            pass
                        else:
                            self.ok_to_move = False
                    for i in enemies:
                        if i.coords != list(self.path[self.move_points]):
                            #print("Loool",i.coords,list(self.path[self.move_points]))
                            pass
                        else:
                            self.ok_to_move = False
                    #if ok_to_move:
                    #    self.coords = list(self.path[self.move_points])
                    #    self.move_points = 0
                else:
                    #print(self.path)
                    self.ok_to_move = True
                    for i in units:
                        if i.coords != list(self.path[0]):
                            #print("Loool",i.coords,list(self.path[0]))
                            pass
                            
                        else:
                            self.ok_to_move = False
                    for i in enemies:
                        if i.coords != list(self.path[0]):
                            #print("Loool",i.coords,list(self.path[0]))
                            pass
                        else:
                            self.ok_to_move = False
                    #if ok_to_move:
                    #    self.coords = list(self.path[0])
                    #    self.move_points -= len(self.path)-1
                    print(self.coords)
                #self.stage = 0
        if self.ok_to_move:
            self.moving = True
        else:
            self.moving = False
            

    def draw_self(self,screen,prop,delta_x,delta_y):
        blit_coords = convert_iso(self.coords,self.move_vector)
        screen.blit(pygame.transform.scale(self.image,(int(64*prop),int(64*prop))),(int(blit_coords[0]*prop+delta_x),int(blit_coords[1]*prop+delta_y)))
        if self.selected:
            if self.test_path_l:
                for i in self.test_path_l:
                    if self.moving == False:
                        blit_coords = convert_iso_dots((i[0],i[1]+1))
                        if self.og_len_test_path_l - self.test_path_l.index(i)> self.move_points + 1:
                            pygame.draw.circle(screen, (255,0,0), (int(blit_coords[0]*prop+delta_x),int(blit_coords[1]*prop+delta_y)), 1)
                        else:
                            pygame.draw.circle(screen, (255,255,0), (int(blit_coords[0]*prop+delta_x),int(blit_coords[1]*prop+delta_y)), 1)


    def det_selected(self,pos):
        if self.coords == detect_clicked(pos):
            self.selected = True
        else:
            self.selected = False
            self.path = None
        
    def test_path(self,pos,nodes,distances):
        if self.moving == False:
            if pos != self.old_pos_test:
                #print("We're creating a new test path for some reason")
                
                self.test_path_l = path_iso_copy.Pathfinding(self.coords,pos,nodes,distances)
                try:
                    self.og_len_test_path_l = len(self.test_path_l)
                except:
                    self.og_len_test_path_l = 0
                self.old_pos_test = pos

    def can_shoot(self,target_coords,hand,tiles,enemies):
        can_shoot = True
        iso_target = detect_clicked(target_coords)
        x = iso_target[0]-self.coords[0]
        y = iso_target[1]-self.coords[1]
        if math.sqrt(x**2+y**2) <= self.equipment[str(hand)][0][0].ranges:
            #print(self.coords)
            self_grid = convert_iso(self.coords,[0,0])
            #print(self_grid)
            vect_x = target_coords[0]-self_grid[0]
            vect_y = target_coords[1]-self_grid[1]
            for i in range(50):
                #print(i,"kjlllllllllllllllllllllllllllllllllllllll")
                
                dx = self_grid[0] + int(vect_x*(i/50))
                dy = self_grid[1] + int(vect_y*(i/50))
                #print(dx,dy,self_grid[0],self_grid[1],int(vect_x*(i/50)),int(vect_y*(i/50)))
                test_tile_coords = detect_clicked([dx,dy])

                for t in tiles:
                    #print(t,"ggdhllghfghf")
                    if t.vert == True:
                        if t.coords == test_tile_coords:
                            can_shoot = False
        else:
            can_shoot = False

        if can_shoot:
            for e in enemies:
                if tuple(e.coords) == tuple(iso_target):
                    return e
            #return True
        else:
            return None

    def can_throw(self,target_coords,hand,tiles):
        can_throw = True
        iso_target = detect_clicked(target_coords)
        x = iso_target[0]-self.coords[0]
        y = iso_target[1]-self.coords[1]
        if math.sqrt(x**2+y**2) <= self.equipment[str(hand)][0][0].ranges:
            #print(self.coords)
            self_grid = convert_iso(self.coords,[0,0])
            #print(self_grid)
            vect_x = target_coords[0]-self_grid[0]
            vect_y = target_coords[1]-self_grid[1]
            for i in range(50):
                #print(i,"kjlllllllllllllllllllllllllllllllllllllll")
                
                dx = self_grid[0] + int(vect_x*(i/50))
                dy = self_grid[1] + int(vect_y*(i/50))
                #print(dx,dy,self_grid[0],self_grid[1],int(vect_x*(i/50)),int(vect_y*(i/50)))
                test_tile_coords = detect_clicked([dx,dy])

                for t in tiles:
                    #print(t,"ggdhllghfghf")
                    if t.vert == True:
                        if t.coords == test_tile_coords:
                            can_throw = False
        else:
            can_throw = False

        if can_throw:
            return iso_target
            #return True
        else:
            return None

        
                        
                        
                    

    def discover_tile(self,tiles):
        for n in path_iso_copy.neighbours(self.coords):
            for k in path_iso_copy.neighbours(n):
                for i in tiles:
                    if i.visited == False:
                        if k == tuple(i.coords):
                            i.visited = True
                        if n == tuple(i.coords):
                            i.visited = True
                        elif self.coords == i.coords:
                            i.visited = True
    def update(self,tiles):
        

        if self.ok_to_move:
            if self.path != None:
                #print(self.rev_path)
                if tuple(self.coords) == self.rev_path[-1]:
                    self.stage = 1
                    self.path = None
                    self.moving = False

                
                else:
                    if self.move_points <= 0:
                        self.stage = 1
                        self.path = None
                        self.moving = False

                    else:
                        if self.coords[0]%2 == 0: #for starting on even (un-shifted) tiles.
                            #print(self.rev_path[self.stage])
                            if self.rev_path[self.stage][1] == self.coords[1]:#if they're on the same y...
                                if self.rev_path[self.stage][0] < self.coords[0]:#if its bottom left...
                                    self.move_vector[0] -= 0.1
                                    self.move_vector[1] += 0.1
                                    self.move_vector[0] = round(self.move_vector[0],1)
                                    self.move_vector[1] = round(self.move_vector[1],1)
                                    
                                    #print("move vector!",self.move_vector)
                                    if math.sqrt(self.move_vector[0]**2) == 1 and math.sqrt(self.move_vector[1]**2) == 1:
                                        self.stage += 1
                                        self.coords[0]-=1
                                        self.move_vector = [0,0]
                                        self.move_points -= 1
                                        self.discover_tile(tiles)
                                elif self.rev_path[self.stage][0] > self.coords[0]:#if its bottom right...
                                    self.move_vector[0] += 0.1
                                    self.move_vector[1] += 0.1
                                    self.move_vector[0] = round(self.move_vector[0],1)
                                    self.move_vector[1] = round(self.move_vector[1],1)
                                    
                                    #print("move vector!",self.move_vector)
                                    if math.sqrt(self.move_vector[0]**2) == 1 and math.sqrt(self.move_vector[1]**2) == 1:
                                        self.stage += 1
                                        self.coords[0]+=1
                                        self.move_vector = [0,0]
                                        self.move_points -= 1
                                        self.discover_tile(tiles)
                            elif self.rev_path[self.stage][1] != self.coords[1]:#if they're not on the same y...
                                #print("CHANGING Y")
                                if self.rev_path[self.stage][0] < self.coords[0]:#if its top left...
                                    self.move_vector[0] -= 0.1
                                    self.move_vector[1] -= 0.1
                                    self.move_vector[0] = round(self.move_vector[0],1)
                                    self.move_vector[1] = round(self.move_vector[1],1)
                                    #print("move vector!",self.move_vector)
                                    if math.sqrt(self.move_vector[0]**2) == 1 and math.sqrt(self.move_vector[1]**2) == 1:
                                        self.stage += 1
                                        self.coords[0]-=1
                                        self.coords[1]-=1
                                        self.move_vector = [0,0]
                                        self.move_points -= 1
                                        self.discover_tile(tiles)
                                elif self.rev_path[self.stage][0] > self.coords[0]:#if its top right...
                                    self.move_vector[0] += 0.1
                                    self.move_vector[1] -= 0.1
                                    self.move_vector[0] = round(self.move_vector[0],1)
                                    self.move_vector[1] = round(self.move_vector[1],1)
                                    #print("move vector!",self.move_vector)
                                    if math.sqrt(self.move_vector[0]**2) == 1 and math.sqrt(self.move_vector[1]**2) == 1:
                                        self.stage += 1
                                        self.coords[0]+=1
                                        self.coords[1]-=1
                                        self.move_vector = [0,0]
                                        self.move_points -= 1
                                        self.discover_tile(tiles)
                        elif self.coords[0]%2 != 0:#for starting on odd (down shifted) tiles.
                            
                            #print(self.rev_path[self.stage])
                            if self.rev_path[self.stage][1] == self.coords[1]:#if they're on the same y...
                                if self.rev_path[self.stage][0] < self.coords[0]:#if its top left...
                                    self.move_vector[0] -= 0.1
                                    self.move_vector[1] -= 0.1
                                    self.move_vector[0] = round(self.move_vector[0],1)
                                    self.move_vector[1] = round(self.move_vector[1],1)
                                    #print("move vector!",self.move_vector)
                                    if math.sqrt(self.move_vector[0]**2) == 1 and math.sqrt(self.move_vector[1]**2) == 1:
                                        self.stage += 1
                                        self.coords[0]-=1
                                        self.move_vector = [0,0]
                                        self.move_points -= 1
                                        self.discover_tile(tiles)
                                elif self.rev_path[self.stage][0] > self.coords[0]:#if its top right...
                                    self.move_vector[0] += 0.1
                                    self.move_vector[1] -= 0.1
                                    self.move_vector[0] = round(self.move_vector[0],1)
                                    self.move_vector[1] = round(self.move_vector[1],1)
                                    #print("move vector!",self.move_vector)
                                    if math.sqrt(self.move_vector[0]**2) == 1 and math.sqrt(self.move_vector[1]**2) == 1:
                                        self.stage += 1
                                        self.coords[0]+=1
                                        self.move_vector = [0,0]
                                        self.move_points -= 1
                                        self.discover_tile(tiles)
                            elif self.rev_path[self.stage][1] != self.coords[1]:#if they're not on the same y...
                                #print("CHANGING Y")
                                if self.rev_path[self.stage][0] < self.coords[0]:#if its bottom left...
                                    self.move_vector[0] -= 0.1
                                    self.move_vector[1] += 0.1
                                    self.move_vector[0] = round(self.move_vector[0],1)
                                    self.move_vector[1] = round(self.move_vector[1],1)
                                    #print("move vector!",self.move_vector)
                                    if math.sqrt(self.move_vector[0]**2) == 1 and math.sqrt(self.move_vector[1]**2) == 1:
                                        self.stage += 1
                                        self.coords[0]-=1
                                        self.coords[1]+=1
                                        self.move_vector = [0,0]
                                        self.move_points -= 1
                                        self.discover_tile(tiles)
                                elif self.rev_path[self.stage][0] > self.coords[0]:#if its bottom right...
                                    self.move_vector[0] += 0.1
                                    self.move_vector[1] += 0.1
                                    self.move_vector[0] = round(self.move_vector[0],1)
                                    self.move_vector[1] = round(self.move_vector[1],1)
                                    #print("move vector!",self.move_vector)
                                    if math.sqrt(self.move_vector[0]**2) == 1 and math.sqrt(self.move_vector[1]**2) == 1:
                                        self.stage += 1
                                        self.coords[0]+=1
                                        self.coords[1]+=1
                                        self.move_vector = [0,0]
                                        self.move_points -= 1
                                        self.discover_tile(tiles)

                        

            
