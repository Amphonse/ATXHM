import math

##############################
#                            #
#This version has support for#
#4 and 8 directional movement#
#                            #
#                            #
#                            #
##############################

def neighbours(node,end_node,w_grid,dim = 8): #node is a 2 item list.
    neighbours = []
    if dim == 8:
        try:
            neighbours.append([node[0]+1,node[1], w_grid[node[0]+1][node[1]] + math.sqrt((node[0]+1-end_node[0])**2+(node[1]-end_node[1])**2)])
        except:
            pass
        try:
            neighbours.append([node[0]+1,node[1]+1, w_grid[node[0]+1][node[1]+1] + math.sqrt((node[0]+1-end_node[0])**2+(node[1]+1-end_node[1])**2)])
        except:
            pass
        try:
            neighbours.append([node[0],node[1]+1, w_grid[node[0]][node[1]+1] + math.sqrt((node[0]-end_node[0])**2+(node[1]+1-end_node[1])**2)])
        except:
            pass
        try:
            neighbours.append([node[0]-1,node[1], w_grid[node[0]-1][node[1]] + math.sqrt((node[0]-1-end_node[0])**2+(node[1]-end_node[1])**2)])
        except:
            pass
        try:
            neighbours.append([node[0]-1,node[1]-1, w_grid[node[0]-1][node[1]-1] + math.sqrt((node[0]-1-end_node[0])**2+(node[1]-1-end_node[1])**2)])
        except:
            pass
        try:
            neighbours.append([node[0],node[1]-1, w_grid[node[0]][node[1]-1] + math.sqrt((node[0]-end_node[0])**2+(node[1]-1-end_node[1])**2)])
        except:
            pass
        try:
            neighbours.append([node[0]+1,node[1]-1, w_grid[node[0]+1][node[1]-1] + math.sqrt((node[0]+1-end_node[0])**2+(node[1]-1-end_node[1])**2)])
        except:
            pass
        try:
            neighbours.append([node[0]-1,node[1]+1, w_grid[node[0]-1][node[1]+1] + math.sqrt((node[0]-1-end_node[0])**2+(node[1]+1-end_node[1])**2)])
        except:
            pass
        return neighbours
    elif dim == 4:
        try:
            neighbours.append([node[0]+1,node[1], w_grid[node[0]+1][node[1]] + math.sqrt((node[0]+1-end_node[0])**2+(node[1]-end_node[1])**2)])
        except:
            pass
        try:
            neighbours.append([node[0],node[1]+1, w_grid[node[0]][node[1]+1] + math.sqrt((node[0]-end_node[0])**2+(node[1]+1-end_node[1])**2)])
        except:
            pass
        try:
            neighbours.append([node[0]-1,node[1], w_grid[node[0]-1][node[1]] + math.sqrt((node[0]-1-end_node[0])**2+(node[1]-end_node[1])**2)])
        except:
            pass
        try:
            neighbours.append([node[0],node[1]-1, w_grid[node[0]][node[1]-1] + math.sqrt((node[0]-end_node[0])**2+(node[1]-1-end_node[1])**2)])
        except:
            pass
        return neighbours

def Pathfinding(start_node, end_node,w_grid,dimp = 8):#nodes are a 2 item list.
    current_node = start_node
    final_path = []
    possible_nodes = []
    while True:
        final_path.append(current_node)
        if current_node == end_node:
            break
        if dimp == 8:
            nei = neighbours(current_node,end_node,w_grid)
        elif dimp == 4:
            nei = neighbours(current_node,end_node,w_grid,dim = 4)
        for i in nei:
            x = [i[0],i[1]]
            if x in final_path:
                pass
            elif i[0] < 0 or i[0] >= 9:
                pass
            elif i[1] < 0 or i[1] >= 9:
                pass
            else:
                possible_nodes.append(i)
        possible_nodes.sort(key=lambda node: node[2])

        current_node = [possible_nodes[0][0],possible_nodes[0][1]]
        del possible_nodes[0]

    final_path.reverse()
    current_node = final_path[0]
    really_final_path = []
    possible_nodes = []
    while True:
        really_final_path.append(current_node)
        if current_node == start_node:
            break
        
        if dimp == 8:
            nei = neighbours(current_node,start_node,w_grid)
        elif dimp == 4:
            nei = neighbours(current_node,start_node,w_grid,dim = 4)
        
        for i in nei:
            x = [i[0],i[1]]

            if x in really_final_path:
                pass
            elif i[0] < 0 or i[0] >= 9:
                pass
            elif i[1] < 0 or i[1] >= 9:
                pass
            elif x not in final_path:
                pass
            else:
                possible_nodes.append(i)
        possible_nodes.sort(key=lambda node: node[2])

        current_node = [possible_nodes[0][0],possible_nodes[0][1]]
        del possible_nodes[0]

    really_final_path.reverse()

    return really_final_path
        

