
class World:
    #Grid = Map
    def __init__(self, grid, obstacles):
        self.grid = grid
        self.obstacles = obstacles
        self.h = self.w = 100
        self.isStartSet = False
        self.isSetStop = False

    def getWidth(self):
        return self.w
    
    def getHeight(self):
        return self.h

    def setStart(self, x, y):
        self.start = [x,y]
        self.isStartSet = True

    def setStop(self, x, y):
        self.stop = [x,y]
        self.isStopSet = True
        
    def getStart(self):
        return self.start
    
    def getStop(self):
        return self.stop

    def isObstacle(self, x, y):
        if [x,y] not in self.grid or (x,y) in self.obstacles:
            return True
        else:
            return False
    
    def near_obst(self, x, y):
        U = [[0,1], [1,0], [0,-1], [-1, 0]]
        for u in U:
            if (x + u[0], y + u[1]) in self.obstacles:
                return True
    