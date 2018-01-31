import path_iso_copy

def Detect_clicked(pos):
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

def Get_target(pos,enemies,unit):
    iso_clicked = Detect_clicked(pos)
    for e in enemies:
        if tuple(e.coords) == tuple(iso_clicked):
            print("fukin lol",e.coords)
            if tuple(e.coords) in path_iso_copy.neighbours(unit.coords):
                return e
