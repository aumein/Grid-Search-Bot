CLOSED = "\033[93m" + "X" + "\033[0m"
FIRE = "\033[91m" + "F" + "\033[0m"
OPEN = "\033[92m" +"O" + "\033[0m"
BUTTON = "\033[96m" +"B" + "\033[0m"
BOT = "\033[94m" +"A" + "\033[0m"
TRACE = "\033[97m" + "O" + "\033[0m"

class Bot:
    def __init__(self, currIndex, btnIndex):
        self.currIndex = currIndex
        self.btnIndex = btnIndex
        self.failed = False
        self.succeeded = False
        
    def fail(self):
        self.failed = True
    
    def success(self):
        self.succeeded = True
    
    def step(self, graph, newIndex):
        if newIndex == None:
            self.fail()
            return
        
        if graph[newIndex] == FIRE:
            self.fail()
        
        if graph[newIndex] == BUTTON:
            self.success()
        
        graph[newIndex] = BOT
        graph[self.currIndex] = TRACE
        self.currIndex = newIndex
        
    def getAdj(self, graph, n, index):
        up = index - n
        down = index + n
        left = index - 1
        right = index + 1
        
        possible = []
        
        if up >= 0:
            if graph[up] == OPEN or graph[up] == BUTTON:
                possible.append(up)
            
        if down < n*n:
            if graph[down] == OPEN or graph[down] == BUTTON:
                possible.append(down)
            
        if index%n != 0:
            if graph[left] == OPEN or graph[left] == BUTTON:
                possible.append(left)
        
        if (index+1)%n != 0:
            if graph[right] == OPEN or graph[right] == BUTTON:
                possible.append(right)
                
        return possible
    
    def getShortestPath(self, graph, n):
        start = self.currIndex
        target = self.btnIndex
        
        queue = [start]
        parent = {start: None}
        while queue:
            node = queue.pop(0)  
            if node == target:
                path = []
                while node is not None:
                    path.append(node)
                    node = parent[node]
                return list(reversed(path))

            for neighbor in Bot.getAdj(self, graph, n, node):
                if neighbor not in parent:
                    parent[neighbor] = node
                    queue.append(neighbor)
        return None    
        
    
#Bot 1 will plan the shortest route from itself to the 
#button and disregard the spread of fire
#Doesn't have any of its own functions, but still included for consistency 
class Bot1(Bot):
    pass

#Bot 2 will replan the shortest route every step
class Bot2(Bot):
    def replan(self, graph, n):
        newRoute = Bot.getShortestPath(self, graph, n)
        
        if newRoute == None:
            return None
        
        nextMove = newRoute.pop(0)
        if nextMove == self.currIndex:
            nextMove = newRoute.pop(0)
            
        return nextMove
    
#Bot 3 will replan at every step and avoid squares adjacent to fire
class Bot3(Bot):
    def adjToFire(self, graph, n, index):
        up = index - n
        down = index + n
        left = index - 1
        right = index + 1

        if up >= 0:
            if graph[up] == FIRE:
                return True
            
        if down < n*n:
            if graph[down] == FIRE:
                return True
            
        if index%n != 0:
            if graph[left] == FIRE:
                return True
        
        if (index+1)%n != 0:
            if graph[right] == FIRE:
                return True
                
        return False
    
    def getShortestPath(self, graph, n):
        start = self.currIndex
        target = self.btnIndex
        
        queue = [start]
        parent = {start: None}
        while queue:
            node = queue.pop(0)  
            if node == target:
                path = []
                while node is not None:
                    path.append(node)
                    node = parent[node]
                return list(reversed(path))

            for neighbor in Bot.getAdj(self, graph, n, node):
                if neighbor not in parent and not self.adjToFire(graph, n, neighbor):
                    parent[neighbor] = node
                    queue.append(neighbor)

        return None           
    
    def replan(self, graph, n):
        newRoute = Bot.getShortestPath(self, graph, n)
        
        if newRoute == None:
            return None
        
        nextMove = newRoute.pop(0)
        if nextMove == self.currIndex:
            nextMove = newRoute.pop(0)
            
        return nextMove    
    
#Bot 4 will replan if any cell it currently has routed is on fire
class Bot4(Bot):
    def replan(self, graph, n):
        newRoute = Bot.getShortestPath(self, graph,n)
        
        if newRoute == None:
            return None
        
        return newRoute
    
    def checkIfOnFire(self, graph, n, route):
        if not route:
            self.fail()
            return None
        
        for path in route:
            if graph[path]==FIRE:
                return True
        return False