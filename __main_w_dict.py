import math as m,pygame,mapr,path_iso_copy,numpy,unit,mans

pygame.init()
screen = pygame.display.set_mode((1280, 800))

def resize():
    global prop,delta_x,delta_y,sheight
    swidth = screen.get_width()
    sheight = screen.get_height()
    propw = swidth/1280
    proph  = sheight/800
    prop = min(propw,proph)
    delta_x = 640*(propw-prop)
    delta_y = 400*(proph-prop)

    
def convert_iso(r):
    #converts grid coordinates to a blit friendly set of iso coordinates.
    y = r[1]*32
    x = r[0]*32
    if r[0]%2 != 0:
        y += 16

    return (int(x),int(y))

def convert_grid(r):
    #converts iso coordinates to a click detector set of grid coordinates.
    y = int(r[1]/32)
    x = int(r[0]/32)
    if r[0]%2 != 0:
        y -= 0.5

    return [x,y]

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

class Tile():
    def __init__(self,
                 coords,
                 code):
        self.coords = coords
        self.code = code
        self.is_Passable = False
        self.vert = False
        self.visited = False
        self.throwable = False
        #each tile has a code that defines what type of tile it is.
        if code == "G":         
            self.cost = 1
            self.is_Passable = True
            self.image = pygame.image.load("Grass_Tile.png").convert()
        if code == "W":         
            self.cost = 9
            self.is_Passable = False
            self.image = pygame.image.load("Water_Tile.png").convert()
        if code == "P":         
            self.cost = 9
            self.is_Passable = False
            self.image = pygame.image.load("Wall_Tile.png").convert()
            self.vert = True
        if code == "Q":         
            self.cost = 9
            self.is_Passable = False
            self.image = pygame.image.load("Wall_corner_Tile.png").convert()
            self.vert = True
        if code == "U":         
            self.cost = 9
            self.is_Passable = False
            self.image = pygame.image.load("Wall_Up.png").convert()
            self.vert = True
        if self.is_Passable == False:
            self.cost = 99999999

        self.image.set_colorkey((255,255,255))
        self.undiscovered_image = pygame.image.load("3_black.png").convert()
        self.undiscovered_image.set_colorkey((255,255,255))
        self.no_throw_image = pygame.image.load("No_Throw.png").convert()
        self.no_throw_image.set_colorkey((255,255,255))


    def draw_self(self,is_throwing):
        if self.visited == True:
            if self.vert:
                blit_coords = convert_iso([self.coords[0],self.coords[1]-1])
                screen.blit(pygame.transform.scale(self.image,(int(64*prop),int(64*prop))),(int(blit_coords[0]*prop+delta_x),int(blit_coords[1]*prop+delta_y)))
            else:
                blit_coords = convert_iso(self.coords)
                screen.blit(pygame.transform.scale(self.image,(int(64*prop),int(32*prop))),(int(blit_coords[0]*prop+delta_x),int(blit_coords[1]*prop+delta_y)))
            if is_throwing == True:
                #print("drawwwwwwwwww")
                if self.throwable != True:
                    
                    blit_coords = convert_iso(self.coords)
                    screen.blit(pygame.transform.scale(self.no_throw_image,(int(64*prop),int(32*prop))),(int(blit_coords[0]*prop+delta_x),int(blit_coords[1]*prop+delta_y)))
        else:
            blit_coords = convert_iso(self.coords)
            screen.blit(pygame.transform.scale(self.undiscovered_image,(int(64*prop),int(32*prop))),(int(blit_coords[0]*prop+delta_x),int(blit_coords[1]*prop+delta_y)))
            
        #if self.visited == 3:
        #    screen.blit(pygame.image.load("3_black.png"),convert_iso(self.coords))
        #elif self.visited == 2:
        #    screen.blit(pygame.image.load("2_black.png"),convert_iso(self.coords))
        #elif self.visited == 1:
        #    screen.blit(pygame.image.load("1_black.png"),convert_iso(self.coords))
        #elif self.visited == 0:
        #    pass

    def print_self(self):
        print(self.coords)



class Controler:
    def __init__(self,turn):
        self.turn = turn

    def new_turn(self,units,enemies):
        #have it run all the enemy stuff here too!!
        
        for i in units.values():
            i.new_turn()
        for i in enemies.values():
            if i.etype == 0:
                #we want this to move towards the one with the lowest % total health.
                #however, because we dont have health yet, we'll just make it go to the
                #first unit in units.
                try:
                    if i.state == "Normal":
                        i.new_turn()
                        i.move_to(units[0].coords,pf_info[0],pf_info[1],units,enemies,tiles)
                        #\/ very rough attacking logic.
                        for coord in path_iso_copy.neighbours(i.coords):
                            for u in units:
                                if tuple(u.coords) == tuple(coord):
                                    i.attack("Left Hand",u,"Torso")
                except:
                    pass
                
                    

#Load the map text that you want.
t_map = mapr.get_map("map")

#take the map text and convert it into a list of tile objects.
tiles = {}
row_count = 0
col_count = 0
for i in t_map:
    col_count = 0
    for k in i:
        #print([col_count,row_count])
        tiles[(col_count,row_count)]=(Tile([col_count,row_count],str(k)))
        col_count += 1
    row_count += 1

C = Controler(0)
barry = unit.Unit("unit.png",5,[11,1],"barry",screen)
gerald = unit.Unit("unit.png",5,[11,3],"gerald",screen)

STEPHEN = unit.Enemy("enemy.png",4,[3,2],0,"STEPHEN",screen)
units = {}
enemies = {}
enemies[tuple(STEPHEN.coords)] = (STEPHEN)
units[tuple(barry.coords)] = (barry)
units[tuple(gerald.coords)] = (gerald)
#units.append(barry)
#units.append(gerald)
selected = []
floor_items = [mans.weepons(0,0,"Sword","Cutting","Melee",200,coords = [11,1])]
#print(path_iso_copy.Pathfinding([0,0],[3,2],tiles))
clock = pygame.time.Clock()
not_moving = True
is_moving_counter = 0
pf_info = path_iso_copy.convert_to_dict(t_map,tiles.values())

tall_tiles = []
for tile in tiles.values():
    if tile.vert:
        tall_tiles.append(tile)


#blit_things = []
#for i in tiles:
#    blit_things.append(i)
#for i in units:
#    blit_things.append(i)
#for i in enemies:
#    blit_things.append(i)

#first_blit = []
#second_blit = []
#for i in blit_things:
#    if i.coords[0]%2==0:
#        if type(i) is Tile:
#            first_blit.append(i)
#for i in blit_things:
#    if i.coords[0]%2==0:
#        if type(i) is unit.Unit:
#            first_blit.append(i)
#for i in blit_things:
#    if i.coords[0]%2==0:
#        if type(i) is unit.Enemy:
#            first_blit.append(i)
#for i in blit_things:
#    if i.coords[0]%2!=0:
#        if type(i) is Tile:
#            second_blit.append(i)
#for i in blit_things:
#    if i.coords[0]%2!=0:
#        if type(i) is unit.Unit:
#            second_blit.append(i)
#for i in blit_things:
#    if i.coords[0]%2!=0:
#        if type(i) is unit.Enemy:
#            second_blit.append(i)
#blit_list = []
#for i in range(len):
#    for k in range(len[0])):
#        for j in blit_things:
#            if j.coords[1] == k:
#                blit_list.append(j)
    
    
            

while True:
        resize()
        new_turn = False
        is_moving = False
        choosing_throwing = False
        
        for i in units.values():
            if i.moving == True:
                is_moving = True
                #print("moving")
        for i in enemies.values():
            if i.moving == True:
                is_moving = True
                #print("moving")
        if is_moving == True:
            if is_moving_counter == 1:
                pass
            
            is_moving_counter += 1
            
        clock.tick(60)
        pos = list(pygame.mouse.get_pos())
        pos[0] = int((pos[0]-delta_x)/prop)
        pos[1] = int((pos[1]-delta_y)/prop)
        iso_clicked = detect_clicked(pos)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h),
                                                  pygame.RESIZABLE)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if new_turn == False:
                        if is_moving == False:
                            C.new_turn(units,enemies)
                            new_turn = True
                #if event.key == pygame.K_1:#Melee Attack
                #    #print("1")
                #    if new_turn == False:
                #        if is_moving == False:
                #            for i in units:
                #                if i.selected:
                #                    if i.state == "Normal":
                #                        if i.actions < i.attacks:
                #                            #print("hi")
                #                            i.actions += 1
                #                            if tuple(STEPHEN.coords) in path_iso_copy.neighbours(i.coords):
                #                                i.attack("Left Hand",STEPHEN.man)
                if event.key == pygame.K_r:
                    for i in tiles.values():
                        i.visited = True

            if event.type == pygame.MOUSEBUTTONUP:
                for tile in tiles.values():
                    tile.throwable = False
                choosing_attack = False
                choosing_menu = False
                choosing_loc = False
                choosing_throwing = False
                other_mode = False
                #for the map bit
                pos = list(pygame.mouse.get_pos())
                pos[0] = int((pos[0]-delta_x)/prop)
                pos[1] = int((pos[1]-delta_y)/prop)
                if pos[1] < ((800*prop)*7/8)-delta_y:
                #print("llleeeellelee")
                    for u in selected:
                        if u.chose_who:
                            choosing_attack = True
                        elif u.menu:
                            choosing_menu = True
                        elif u.vatss:
                            choosing_loc = True
                        if u.selected == True:
                            if u.stats_page == True:
                                if u.st_x < pos[0] and pos[0] <u.st_x + 300:
                                    if u.st_y-30 < pos[1] and pos[1]< u.st_y +315:
                                        other_mode = True
                                    else:
                                        other_mode = False
                                else:
                                    other_mode = False
                            elif u.inv_pg == True:
                                if u.in_x+10 < pos[0] and pos[0] <u.in_x + 290:
                                    if u.in_y-15 < pos[1] and pos[1]< u.in_y +300:
                                        other_mode = True
                                    else:
                                        other_mode = False
                                else:
                                    other_mode = False
                        #if u.throwing:
                        #    print("We ARE throwing!")
                        #    choosing_throwing = True
                            
                    if other_mode == False:        
                        if choosing_attack==False and choosing_menu ==False and choosing_loc == False and choosing_throwing == False:
                            iso_clicked = detect_clicked(pos)
                            if event.button == 1:
                                if new_turn == False:
                                    tiles[tuple(iso_clicked)].print_self()
                                    units[tuple(iso_clicked)].selected = True
                                    #for i in units:
                                    #    if is_moving == False:
                                    #        i.det_selected(pos)
                            elif event.button == 3:
                                #print(selected)
                                if new_turn == False:
                                    for i in selected:
                                        #print("hey")
                                        if i.moving == False:
                                            if is_moving == False:
                                                if i.state == "Normal":
                                                    if tuple(iso_clicked) != tuple(i.coords):
                                                    
                                                        i.move_to(iso_clicked,pf_info[0],pf_info[1],units,enemies,tiles)
                        else:
                            #if choosing_throwing:
                            for u in selected:
                                for tile in tiles.keys():
#
                                    #non_screen_coords = detect_clicked(tile.coords) 
                                    a = u.can_throw(convert_iso(tile),tiles)
                                    if a!= None:
                                        print(tile[0]-1,a[0],tile[1],a[1])
                                        if tile[0]-1 == a[0] and tile[1] == a[1]:
                                            tiles[tile].throwable = True

                            if event.button == 1:
                                for i in selected:
                                    i.left_click(enemies,tiles,floor_items)
                                    i.reset()
                            elif event.button == 3:
                                for i in selected:
                                    i.right_click(list(pygame.mouse.get_pos()))
                    else:#simulating the tooltip bit for matyas' other windows
                        
                        if event.button == 1:
                            if new_turn == False:
                                for i in selected:
                                    #print("hey")
                                    if i.moving == False:
                                        if is_moving == False:
                                            if i.state == "Normal":
                                                i.left_click(enemies,tiles,floor_items)
                                                    
                                                i.reset()
                        if event.button == 3:
                            if new_turn == False:
                                for i in selected:
                                    #print("hey")
                                    if i.moving == False:
                                        if is_moving == False:
                                            if i.state == "Normal":
                                                i.right_click(list(pygame.mouse.get_pos()))
                        
                            
                #for the tooltip bit
                else:
                    for u in selected:
                        for tile in tiles.keys():
                            
                            a = u.can_throw(convert_iso(tile),tiles)
                            if a!= None:
                                print(tile[0]-1,a[0],tile[1],a[1])
                                if tile[0]-1 == a[0] and tile[1] == a[1]:
                                    tiles[tile].throwable = True

                    if event.button == 1:
                        if new_turn == False:
                            for i in selected:
                                #print("hey")
                                if i.moving == False:
                                    if is_moving == False:
                                        if i.state == "Normal":
                                            i.left_click(enemies,tiles,floor_items)
                                                
                                            i.reset()
                    if event.button == 3:
                        if new_turn == False:
                            for i in selected:
                                #print("hey")
                                if i.moving == False:
                                    if is_moving == False:
                                        if i.state == "Normal":
                                            i.right_click(list(pygame.mouse.get_pos()))
                                            

 
                    
        screen.fill((0,0,0))


        for i in units.values():
            
            if i.throwing:
                #print("We ARE throwing!")
                choosing_throwing = True
            
        for tile in tiles.values():
            if tile not in tall_tiles:
                tile.draw_self(choosing_throwing)

        for i in floor_items:
            if i.coords != None:
                i.draw_self(screen)
                
        for i in enemies.values():
            i.draw_self(screen,tiles,prop,delta_x,delta_y)
            i.update()

        for i in tall_tiles:
            i.draw_self(choosing_throwing)
            
        for i in units.values():
            i.draw_self(screen,prop,delta_x,delta_y)

            
            
            i.update(tiles)
            if i.selected:
                i.resize()
                i.reset()
                if i.state == "Normal":
                    i.test_path(iso_clicked,pf_info[0],pf_info[1])
                if i not in selected:
                    #print(i)
                    selected.append(i)
            else:
                if i in selected:
                    selected.remove(i)
            try:
                pass
                #if choosing_throwing:
                #    for tile in tiles:
                #        if i.can_throw(convert_iso(tile.coords),i.hand,tiles):
                            
                        
                #add a function to show all the available throwing tiles.
                #this function will use a circle to reduce the number of
                #tiles it needs to cycle through. All tiles within this
                #circle that can_throw = True will be left unchanged. All others
                #will have a red hash tile drawn on top of them.
            except:
                pass
        
        
                    
        

        
        
        
        pygame.display.flip()
