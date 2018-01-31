#this function takes a txt file map and converts it into
#an array (nested list).

#eg:
#GGGG
#GGGG
#GGGG
# ->
#[['G', 'G', 'G', 'G'], ['G', 'G', 'G', 'G'], ['G', 'G', 'G', 'G']]

def get_map(mapname,m_type =0):
    map_file = open(str(mapname)+".txt","r")
    map_txt = map_file.read()
    map_file.close()
    row_list = map_txt.splitlines()
    count = 0
    map_list = []
    for s in row_list:
        map_list.append([])
    for s in row_list:
        for l in s:
            if m_type == 0:
                map_list[count].append(l)
            elif m_type == 1:
                map_list[count].append(int(l))
        count += 1
    return map_list



