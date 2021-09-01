import random

def MakeGrid(N):
    grid = [] # create a list for the environment
    for i in range(N):
        temp = [] # inside of grid, create a list for each row
        for j in range(N):
            temp.append(['E']) # for each cell create a list which initially has an 'E'
        grid.append(temp)
    return grid

def RandomPerson(grid, P, PersonType, initEnergy): # P is the number of people that you want
    V = len(grid)
    H = len(grid[0])
    k = 0 # k is a counter that counts the number of people you have created
    while k<P:
        v = int(random.random() * V) # get random locations. V and H are the grid size.
        h = int(random.random() * H)
        if grid[v][h][0] == 'E': # if the chosen cell is empty
            newperson = [PersonType, 0, 0, initEnergy, False] # create a new person
            grid[v][h] = newperson # place new person in the cell
            #print('New Person Created')
            k += 1 # increment the counter for new person
            
def MovePerson(grid):
    vgrid_size = len(grid)
    hgrid_size = len(grid[0])
    for v in range(len(grid)):
        for h in range(len(grid[0])):
            if grid[v][h][0] != 'E' and grid[v][h][4] == False:
                #print('Need to move this one')
                ChoosePosition = False
                steps = 0
                while ChoosePosition == False and steps < 10:
                    vpos, hpos = RandomStep2(v,h)
                    steps += 1
                        
                    vpos, hpos = BoundaryTranslate(grid, vpos, hpos)
                        
                    ChoosePosition = CheckPosition(grid,vpos,hpos)
                    if ChoosePosition:
                        #print(grid[v][h], grid[vpos][hpos])
                        grid[vpos][hpos] = grid[v][h]
                        grid[v][h] = ['E']
                        grid[vpos][hpos][4] = True
                        
def ReduceEnergy(grid):
    for v in range(len(grid)):
        for h in range(len(grid[0])):
            if grid[v][h][0] == 'I':
                grid[v][h][3] -= 1
                if grid[v][h][3] == 0: # if energy goes to zero
                    grid[v][h] = ['E'] # The infected Person dies
                    
def Infect(grid, sn):
    for v in range(len(grid)):
        for h in range(len(grid[0])):
            if grid[v][h][0] == 'I':
                # if person in neigboring cell then infect them
                neighbors = ((1,0),(1,1),(0,1),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1))
                for loc in neighbors:
                    bv, bh = BoundaryTranslate(grid, v+loc[0], h+loc[1])
                    if not CheckPosition(grid, bv, bh) and grid[bv][bh][0] == 'U': 
                        #grid[bv][bh] = ['E']
                        #grid[v][h][3] += 1
                        if random.random() < 0.28:
                            grid[bv][bh][0] = 'I'
                            grid[bv][bh][3] = sn
            
def Reset(grid):
    for v in range(len(grid)):
        for h in range(len(grid[0])):
            if grid[v][h][0] != 'E':
                grid[v][h][4] = False
            
def RandomStep(v, h):
    md = random.randint(0, 3)
    #print(md)
    if md == 0:
        vpos = v - 1
        hpos = h
    elif md == 1:
        vpos = v
        hpos = h + 1
    elif md == 2:
        vpos = v + 1
        hpos = h
    elif md == 3:
        vpos = v
        hpos = h - 1
    return vpos, hpos

def RandomStep2(v,h):
    neighbors = ((1,0),(1,1),(0,1),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1))
    md = random.randint(0,7)
    return v + neighbors[md][0], h + neighbors[md][1]
            
def CheckPosition(grid, v, h):
    if grid[v][h][0] == 'E':
        return True
    else:
        return False

def BoundaryTranslate(grid, v, h):
    vgrid_size = len(grid)
    hgrid_size = len(grid[0])
    
    # periodic boundary
    if v < 0:
        v = vgrid_size-1
    elif v > vgrid_size-1:
        v = 0
                        
    if h < 0:
        h = hgrid_size-1
    elif h > hgrid_size-1:
        h = 0
    return v, h
            
def Iterate(grid, sn):
    MovePerson(grid)
    #Age(grid)
    #Birth(grid, fm, sm, sn)
    ReduceEnergy(grid)
    Infect(grid, sn)
    Reset(grid)
    
def Count(grid):
    person = 0
    inperson = 0
    for v in range(len(grid)):
        for h in range(len(grid[0])):
            if grid[v][h][0] == 'U':
                person += 1
            elif grid[v][h][0] == 'I':
                inperson += 1
                
    return person, inperson, person + inperson

def GetPositions(grid):
    for v in range(len(grid)):
        for h in range(len(grid[0])):
            if grid[v][h][0] != 'E':
                print("Positions.. v:%s h:%s",(v,h))