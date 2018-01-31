import math,numpy

def neighbours(node):
    neighbours = []
    if node[0]%2 == 0:
        neighbours.append((node[0]+1,node[1]))
        neighbours.append((node[0]-1,node[1]))
        neighbours.append((node[0]-1,node[1]-1))
        neighbours.append((node[0]+1,node[1]-1))
        neighbours.append((node[0],node[1]-1))
        neighbours.append((node[0],node[1]+1))
        neighbours.append((node[0]+2,node[1]))
        neighbours.append((node[0]-2,node[1]))
        
        
    elif node[0]%2 != 0:
        neighbours.append((node[0]+1,node[1]))
        neighbours.append((node[0]-1,node[1]))
        neighbours.append((node[0]-1,node[1]+1))
        neighbours.append((node[0]+1,node[1]+1))
        neighbours.append((node[0],node[1]-1))
        neighbours.append((node[0],node[1]+1))
        neighbours.append((node[0]+2,node[1]))
        neighbours.append((node[0]-2,node[1]))


    return neighbours




def Pathfinding(start_node,end_node,grid,tiles):
    nodes = []
    i_count = 0
    k_count = 0
    for i in grid:
        for k in i:
            nodes.append((k_count,i_count))
            k_count += 1
        i_count += 1
        k_count = 0
    nodes = tuple(nodes)

    distances = {}
    for node in nodes:
        for tile in tiles:
            if tile.coords==node:
                if tile.is_Passable == False:
                    pass
        vertex_dict = {}
        for neighbour in neighbours(node):
            try:
                vertex_dict[neighbour] = grid[neighbour[0]][neighbour[1]]
                #print(vertex_dict[neighbour])
            except:
                pass
        distances[node] = vertex_dict
    #distances = {
    #    'B': {'A': 5, 'D': 1, 'G': 2},
    #    'A': {'B': 5, 'D': 3, 'E': 12, 'F' :5},
    #    'D': {'B': 1, 'G': 1, 'E': 1, 'A': 3},
    #    'G': {'B': 2, 'D': 1, 'C': 2},
    #    'C': {'G': 2, 'E': 1, 'F': 16},
    #    'E': {'A': 12, 'D': 1, 'C': 1, 'F': 2},
    #    'F': {'A': 5, 'E': 2, 'C': 16}}

    unvisited = {node: None for node in nodes} #using None as +inf
    visited = {}
    current = tuple(start_node)
    currentDistance = 0
    unvisited[current] = currentDistance

    while True:
        for neighbour, distance in distances[current].items():
            if neighbour not in unvisited: continue
            newDistance = currentDistance + distance
            if unvisited[neighbour] is None or unvisited[neighbour] > newDistance:
                unvisited[neighbour] = newDistance
        visited[current] = currentDistance
        if current == tuple(end_node):
            break
        del unvisited[current]
        if not unvisited: break
        candidates = [node for node in unvisited.items() if node[1]]
        current, currentDistance = sorted(candidates, key = lambda x: x[1])[0]

    
    node = tuple(end_node)
    path = [node]
    running = True
    while running:
        for a in visited:
            #print(a)
            if a in neighbours(node):
                #print(a)
                if a in distances[node]:
                    if a not in path:
                        if visited[a]<visited[node]:
                            #print(a)
                            path.append(a)
                            #print(path)
                            node = a
                            #print(start_node)
                            if a == tuple(start_node):
                                #print(a,"=",start_node)
                                running = False
                
    return path
    #print(visited)
            





    
    #val = grid[chosen_node[0]][chosen_node[1]]*(options[chosen_node]+math.sqrt((chosen_node[0]-neighbour[0])**2+(chosen_node[1]-neighbour[1])**2))


            
        
        
    
