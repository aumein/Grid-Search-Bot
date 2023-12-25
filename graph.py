import random
import math
import bot

CLOSED = "\033[93m" + "X" + "\033[0m"
FIRE = "\033[91m" + "F" + "\033[0m"
OPEN = "\033[92m" +"O" + "\033[0m"
BUTTON = "\033[96m" +"B" + "\033[0m"
BOT = "\033[94m" +"A" + "\033[0m"
TRACE = "\033[97m" + "O" + "\033[0m"

OPEN_SQUARES = []
ONE_NEIGHBOR = []
DEAD_ENDS = []

# This is to keep track of all the burning cells
BURNING_NEIGHBOR = []

# q is a parameter between 0 and 1, defining the flammability of the ship.
FLAMMABILITY = 0


#ONLY USED DURING INITIALIZATION
def openRandomInterior(graph,n):
    squareOpened = False
    
    if len(OPEN_SQUARES) == n*n:
        #all squares are open
        return
    
    while not squareOpened:
        a = random.randint(0, n*n-1)
        if a not in range(0, n-1) and a not in range(n*n-n, n*n-1) and a%n != 0 and (a+1)%n != 0:
            OPEN_SQUARES.append(a)
            graph[a] = OPEN
            squareOpened = True

    return

def openSquare(graph, index):
    if index == None:
        return
    
    OPEN_SQUARES.append(index)
    graph[index] = OPEN
    return
    

#Used to ID blocked cells with only one neighbor
def checkForOneAdj(n, index):
    up = index - n
    down = index + n
    left = index - 1
    right = index + 1
    
    count = 0
    
    if up >= 0:
        if up in OPEN_SQUARES:
            count+= 1
        
    if down < n*n:
        if down in OPEN_SQUARES:
            count+= 1
        
    if index%n != 0:
        if left in OPEN_SQUARES:
            count+= 1
    
    if (index+1)%n != 0:
        if right in OPEN_SQUARES:
            count+= 1  
    
    if count == 1:
        return True

    return False

#Actually only returns the index of an open adjacent square to index
#Used for the opening of dead ends
def openOneAdj(index, n):
    up = index - n
    down = index + n
    left = index - 1
    right = index + 1
    
    possible = []
    
    if up >= 0:
        if up not in OPEN_SQUARES:
            possible.append(up)
        
    if down < n*n:
        if down not in OPEN_SQUARES:
            possible.append(down)
        
    if index%n != 0:
        if left not in OPEN_SQUARES:
            possible.append(left)
    
    if (index+1)%n != 0:
        if right not in OPEN_SQUARES:
            possible.append(right)
            
    if len(possible) == 0:
        return None
    
    return random.choice(possible)

    
#Print Function
def printGraph(graph, n):
    print()
    for i in range(0,n*n):
        print(" " + graph[i] + " ", end="")
        if((i+1)%n == 0 and i != 0):
            print()
    return

# Identify all currently blocked cells that have exactly one open neighbor.
# Of these currently blocked cells with exactly one open neighbor, pick one at random.
# Open the selected cell.
# Repeat until you can no longer do so.
def iterateOnInit(graph,n):
    ONE_NEIGHBOR = []
    
    for i in range(0, n*n):
        if checkForOneAdj(n, i) and i not in OPEN_SQUARES:
            ONE_NEIGHBOR.append(i)
    
    if len(ONE_NEIGHBOR) == 0:
        return -1
    
    index = random.choice(ONE_NEIGHBOR)
    openSquare(graph, index)
            
    return index

def deadEnds(n):
    DEAD_ENDS = []
    
    for i in range(0, n*n):
        if checkForOneAdj(n,i) and i in OPEN_SQUARES:
            DEAD_ENDS.append(i)
    
    if len(DEAD_ENDS) == 0:
        DEAD_ENDS.append(-1)

    return DEAD_ENDS

#Initializes a graph of size nxn
#Opens a random interior square to start the iteration function
#Opens about half of the dead ends that were found
def initGraph(n):
    size = n*n
    graph = [CLOSED]*size
    openRandomInterior(graph,n)
    index = 0
    
    #iteration
    while index != -1:
        index = iterateOnInit(graph, n)
    
    DEAD_ENDS = deadEnds(n) 
    
    toRev = math.trunc(0.5*len(DEAD_ENDS))
    
    for i in range(0, toRev):
        index = random.choice(DEAD_ENDS)
        openSquare(graph, openOneAdj(index, n))
        DEAD_ENDS.remove(index)
    
    return graph, n

#Starts the fire on the graph
def startFire(graph, n):
    fireIndex = random.choice(OPEN_SQUARES)
    graph[fireIndex] = FIRE
    BURNING_NEIGHBOR.append(fireIndex)
    #printGraph(graph, n)
 
#Queue to run the fire, should be called at every time advance
def fireTick(graph, n,q):
    updatedCells = []
    for cell in BURNING_NEIGHBOR:
        if((cell - n) >= 0 and (cell - n) in OPEN_SQUARES and (cell - n) not in BURNING_NEIGHBOR):
            graph, addFire = updateFires(graph, cell - n, n,q)
            if addFire: 
                updatedCells.append(cell - n)
        if((cell - 1) >= 0 and (cell - 1) in OPEN_SQUARES and (cell - 1) not in BURNING_NEIGHBOR and (cell) % n != 0):
            graph, addFire = updateFires(graph, cell - 1, n,q)
            if addFire: 
                updatedCells.append(cell - 1)
        if((cell + 1) < len(graph) and (cell + 1) in OPEN_SQUARES and (cell + 1) not in BURNING_NEIGHBOR and (cell + 1) % n != 0):
            graph, addFire = updateFires(graph, cell + 1, n,q)
            if addFire: 
                updatedCells.append(cell + 1)
        if((cell + n) < len(graph) and (cell + n) in OPEN_SQUARES and (cell + n) not in BURNING_NEIGHBOR):
            graph, addFire = updateFires(graph, cell + n, n,q)
            if addFire: 
                updatedCells.append(cell + n)
    BURNING_NEIGHBOR.extend(updatedCells)      
    

# Sets the open cell to burning cell 
def updateFires(graph, node, size,q):
    addFire = False
    count = 0
    if((node - size) in BURNING_NEIGHBOR):
        count+=1
    if((node + size) in BURNING_NEIGHBOR):
        count+=1
    if((node - 1) in BURNING_NEIGHBOR and (node % size) != 0):
        count+=1
    if((node + 1) in BURNING_NEIGHBOR and (node + 1 % size) != 0):
        count+=1
    fire_spread = 1 - (1 - q) ** count
    probability = random.random()
    if(probability <= fire_spread):
        if graph[node] == BOT:
            pass
        graph[node] = FIRE
        addFire = True
    return graph, addFire

def placeBtn(graph, btnIndex):
    graph[btnIndex]=BUTTON
    OPEN_SQUARES.remove(btnIndex)
    
def placeBot(graph, botIndex):
    graph[botIndex] = BOT
    OPEN_SQUARES.remove(botIndex)

def simulateBot1(n,q):
    simulations = n
    success = 0
    failure = 0
    for _ in range(simulations):
        #setup for EVERY bot
        graph, n = initGraph(10)
        startFire(graph, n)
        btnIndex = random.choice(OPEN_SQUARES)
        placeBtn(graph, btnIndex)
        botIndex = random.choice(OPEN_SQUARES)
        placeBot(graph, botIndex)

        #placing bots
        b1 = bot.Bot1(botIndex, btnIndex)
        
        pathOfBot1 = b1.getShortestPath(graph, n)
        if pathOfBot1:
            pathOfBot1.pop(0)
        
        for t in range(0, int(0.5*n*n)):
            if not pathOfBot1:             
                break
            
            b1.step(graph, pathOfBot1.pop(0))
            fireTick(graph, n,q)        

            if b1.failed or b1.succeeded or b1.currIndex in BURNING_NEIGHBOR:
                break
        
        
        if b1.succeeded:
            success += 1
        else:
            printGraph(graph, n)
            print("^BOT 1 FAILURE")
            failure += 1
        OPEN_SQUARES.clear()
        ONE_NEIGHBOR.clear()
        DEAD_ENDS.clear()
        BURNING_NEIGHBOR.clear()
    #print("Bot 1 Stats:")
    #print("Success:", round(success / simulations * 100,2), "%")
    #print("Failure:", round(failure / simulations * 100,2), "%\n") 
    return round(success / simulations * 100,2)   
    
def simulateBot2(n,q):
    simulations = n
    success = 0
    failure = 0
    for _ in range(simulations):
        #setup for EVERY bot
        graph, n = initGraph(10)
        startFire(graph, n)
        btnIndex = random.choice(OPEN_SQUARES)
        placeBtn(graph, btnIndex)
        botIndex = random.choice(OPEN_SQUARES)
        placeBot(graph, botIndex)

        #placing bots
        b2 = bot.Bot2(botIndex, btnIndex)
        
        for t in range(0, int(0.5*n*n)):
            b2.step(graph, b2.replan(graph, n))
            fireTick(graph, n,q)        

            if b2.failed or b2.succeeded or b2.currIndex in BURNING_NEIGHBOR:
                break
        
        if b2.succeeded:
            success += 1
        else:
            printGraph(graph, n)
            print("^BOT 2 FAILURE")
            failure += 1
        OPEN_SQUARES.clear()
        ONE_NEIGHBOR.clear()
        DEAD_ENDS.clear()
        BURNING_NEIGHBOR.clear()
    return round(success / simulations * 100,2)

def simulateBot3(n,q):
    simulations = n
    success = 0
    failure = 0
    for _ in range(simulations):
        #setup for EVERY bot
        graph, n = initGraph(10)
        startFire(graph, n)
        btnIndex = random.choice(OPEN_SQUARES)
        placeBtn(graph, btnIndex)
        botIndex = random.choice(OPEN_SQUARES)
        placeBot(graph, botIndex)

        #placing bots
        b3 = bot.Bot3(botIndex, btnIndex)
        
        for t in range(0, int(0.5*n*n)):
            b3.step(graph, b3.replan(graph, n))
            fireTick(graph, n,q)        

            if b3.failed or b3.succeeded or b3.currIndex in BURNING_NEIGHBOR:
                break
        
        if b3.succeeded:
            success += 1
        else:
            printGraph(graph, n)
            print("^BOT 3 FAILURE")
            failure += 1
        OPEN_SQUARES.clear()
        ONE_NEIGHBOR.clear()
        DEAD_ENDS.clear()
        BURNING_NEIGHBOR.clear()
    return round(success / simulations * 100,2) 

def simulateBot4(n,q):
    simulations = n
    success = 0
    failure = 0
    for _ in range(simulations):
        #setup for EVERY bot
        graph, n = initGraph(10)
        startFire(graph, n)
        btnIndex = random.choice(OPEN_SQUARES)
        placeBtn(graph, btnIndex)
        botIndex = random.choice(OPEN_SQUARES)
        placeBot(graph, botIndex)

        #placing bots
        b4 = bot.Bot4(botIndex, btnIndex)
        
        pathOfBot4 = b4.getShortestPath(graph, n)
        if pathOfBot4:
            pathOfBot4.pop(0)
        
        for t in range(0, int(0.5*n*n)):
            if b4.checkIfOnFire(graph, n, pathOfBot4):
                pathOfBot4 = b4.replan(graph, n)
                if pathOfBot4:
                    pathOfBot4.pop(0)
                else:
                    b4.fail()
                    break
            if pathOfBot4:   
                b4.step(graph, pathOfBot4.pop(0))
                fireTick(graph, n,q)        

            if b4.failed or b4.succeeded or b4.currIndex in BURNING_NEIGHBOR:
                break
        
        if b4.succeeded:
            success += 1
        else:
            printGraph(graph, n)
            print("^BOT 4 FAILURE")
            failure += 1
        OPEN_SQUARES.clear()
        ONE_NEIGHBOR.clear()
        DEAD_ENDS.clear()
        BURNING_NEIGHBOR.clear()
    return round(success / simulations * 100,2)  




#Moving testing to driver.py bc this file is getting too crowded lol
#TESTING ONLY THIS FILE
def main():
    print("TESTING IN GRAPH.PY")
    simulations = 200
    success = 0
    failure = 0
    for _ in range(simulations):
        #setup for EVERY bot
        graph, n = initGraph(10)
        startFire(graph, n)
        btnIndex = random.choice(OPEN_SQUARES)
        placeBtn(graph, btnIndex)
        botIndex = random.choice(OPEN_SQUARES)
        placeBot(graph, botIndex)

        #placing bots
        b1 = bot.Bot1(botIndex, btnIndex)
        
        pathOfBot1 = b1.getShortestPath(graph, n)
        if pathOfBot1:
            pathOfBot1.pop(0)
        
        for t in range(0, int(0.5*n*n)):
            if not pathOfBot1:             
                break
            
            b1.step(graph, pathOfBot1.pop(0))
            fireTick(graph, n)        

            if b1.failed or b1.succeeded or b1.currIndex in BURNING_NEIGHBOR:
                break
        
        if b1.succeeded:
            success += 1
        else:
            failure += 1
        OPEN_SQUARES.clear()
        ONE_NEIGHBOR.clear()
        DEAD_ENDS.clear()
        BURNING_NEIGHBOR.clear()
    print("Success:", success / simulations * 100, "%")
    print("Failure:", failure / simulations * 100, "%")
    
if __name__ == "__main__":
    main()
    