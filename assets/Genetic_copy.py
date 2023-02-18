from Mice import Mice
import random as randy
import copy

class Genetic:
    GO_LEFT = "L"
    GO_UP = "U"
    GO_RIGHT = "R"
    GO_DOWN = "D"

    GO_LEFT_c = "L"
    GO_UP_c = "U"
    GO_RIGHT_c = "R"
    GO_DOWN_c = "D"
    
    MAX_POINT = 100
    USE_EUCLIDIAN = 1
    USE_MANHATTAN = 2

    miceList = []
    selectedMice = []


    def __init__(self, population, LenDNA, world, selectionRate, mutationRate, deterministicMode):
        self.population = population
        self.LenDNA = LenDNA
        self.world = world
        self.selectionRate = selectionRate
        self.mutationRate = mutationRate
        self.deterministicMode = deterministicMode

        for i in range(self.population):
            self.miceList.append(Mice(self.LenDNA, self.world))
            self.miceList[i].createDNA(self)
            self.fitnessCalculation(self.miceList[i])

    def isPenalty(self, mice, i):
        if (mice.dna[i-1] == "L" and mice.dna[i] == "R" or
            mice.dna[i-1] == "R" and mice.dna[i] == "L" or
            mice.dna[i-1] == "U" and mice.dna[i] == "D" or
            mice.dna[i-1] == "D" and mice.dna[i] == "U" ):

            return 1
        else:
            return 0
    
    def dnaConflictPenalty(self, mice):
        penalty = 0
        dna = mice.dna
        for i in range(mice.LenDNA):
            if (dna[i-1] == "L" and dna[i] == "R" or
                dna[i-1] == "R" and dna[i] == "L" or
                dna[i-1] == "U" and dna[i] == "D" or
                dna[i-1] == "D" and dna[i] == "U"):

                penalty += 1
        
        return penalty*2
    
    @staticmethod
    def euclidian(x1, y1, x2, y2):
        x_sqr = ((x1-x2)**2)
        y_sqr = ((y1-y2)**2)
        return (x_sqr+y_sqr)**0.5

    @staticmethod
    def manhattan(x1, y1, x2, y2):
        return abs(x1-x2) + abs(y1-y2)

    def deterministic(self, x1, y1, x2, y2):
        if self.deterministicMode == self.USE_EUCLIDIAN:
            return self.euclidian(x1,y1, x2, y2)

        elif self.deterministicMode == self.USE_MANHATTAN:
            return self.manhattan(x1,y1, x2, y2)
        print("Set deterministic Mode")
        return -1
    
    def fitnessCalculation(self, mice):
        ### 1era aplicacion

        # current_x = self.world.getStart()[0]
        # current_y = self.world.getStart()[1]
        # target_x = self.world.getStop()[0]
        # target_y = self.world.getStop()[1]
        # start_x = self.world.getStart()[0]
        # start_y = self.world.getStart()[1]
        # i = 0
        # cont = 1  #Continue variable
        # while i < mice.LenDNA and cont > 0:
        #     c = mice.dna[i]
        #     if c == "L":
        #         current_x -= 1

        #     elif c == "R":
        #         current_x += 1   

        #     elif c == "U":
        #         current_y += 1 #Original code is -=

        #     elif c == "D":
        #         current_y -= 1 #Original code is +=
            
        #     #Target Found
        #     if current_x == target_x and current_y == target_y:
        #         cont = 0
        #     elif self.world.isObstacle(current_x, current_y):
        #         cont = -1
            
        #     i += 1
        # numberOfSuccessfulMove = i - 1
        # mice.numberOfSuccessfulMove = numberOfSuccessfulMove

        # #Target Found
        # if cont == 0:
        #     mice.fitness =self.MAX_POINT
        # else:
        #     maxDistance = self.deterministic(start_x, start_y, target_x, target_y)
        #     #print("max: " ,maxDistance)
        #     currentDistance = self.deterministic(current_x, current_y, target_x, target_y) 
        #     #print("current: ", currentDistance)
        #     mice.fitness = self.MAX_POINT * (1- (currentDistance / maxDistance))

        ### 2da aplicacion

        # target_x = self.world.getStop()[0]
        # target_y = self.world.getStop()[1]
        # start_x = self.world.getStart()[0]
        # start_y = self.world.getStart()[1]
        # mice_mov = self.world.getStart()
        # MOV = {"L": [-1, 0], "R": [1,0], "U": [0,1], "D": [0,-1]}
        # flag_target = 0
        # lenPath = 0
        # for i in range(mice.LenDNA):
        #     c = mice.dna[i]
        #     mice_mov += MOV[c]
        #     lenPath += 1    #Manhattan Distance with resolution of 1:1

        #     if mice_mov == [target_x, target_y]:
        #         flag_target = 1
        #         break
            
        #     elif self.world.isObstacle(mice_mov[0], mice_mov[1]):
        #         flag_target = -1
        #         break
        
        # maxDistance = self.deterministic(start_x, start_y, target_x, target_y)
        # #     #print("max: " ,maxDistance)
        # currentDistance = self.deterministic(mice_mov[0], mice_mov[1], target_x, target_y) 
        # mice.numberOfSuccessfulMove = i
        # mice.fitness = self.MAX_POINT * (1- (currentDistance / maxDistance))

        #### Tercera aplicacion
        target_x = self.world.getStop()[0]
        target_y = self.world.getStop()[1]
        target = self.world.getStop()

        start_x = self.world.getStart()[0]
        start_y = self.world.getStart()[1]
        current = copy.copy(self.world.getStart())
        MOV = {"L": [-1, 0], "R": [1,0], "U": [0,1], "D": [0,-1]}
        for i in range(mice.LenDNA):
            c = mice.dna[i]
            #current[0] += MOV[c][0]
            #current[1] += MOV[c][1]
            current = [sum(x) for x in zip(current, MOV[c])]
            # if current[0]== target_x and current[1] == target_y:
            #     break

            if current == target or self.world.isObstacle(current[0], current[1]):
                break

            # elif self.world.isObstacle(current[0], current[1]):
            #     break
        
        numberOfSuccessfulMove = i
        mice.numberOfSuccessfulMove = numberOfSuccessfulMove

        #Target Found
        maxDistance = self.deterministic(start_x, start_y, target_x, target_y)
        currentDistance = self.deterministic(current[0],current[1], target_x, target_y) 
        mice.fitness = self.MAX_POINT * (1 - (currentDistance / maxDistance))
        mice.fitness *= (1-(numberOfSuccessfulMove/mice.LenDNA)*0.65)


    def showFitness(self):
        for i in range(self.population):
            self.fitnessCalculation(self.miceList[i])
            
            #self.miceList[i].world.drawGen(str(self.miceList[i].dna), self.world.randomColor(), self.miceList[i].numberOfSuccessfulMove)

            # if self.miceList[i].fitness >= self.MAX_POINT:
            #     return 1
        # return 0
    
    def selection(self):
        self.miceList.sort(key=lambda x: x.fitness, reverse = True)
        #self.miceList.sort(reverse = True)
        self.selectedMice = []

        for j in range(int(self.selectionRate*self.population)):
            self.selectedMice.append(self.miceList[j])

    def crossover(self):
        self.miceList = []
        for k in range(int(self.population / 2 + self.population % 2)):
            mice1 = int(randy.uniform(0,1) * self.selectionRate * self.population)
            mice2 = int(randy.uniform(0,1) * self.selectionRate * self.population)
            while mice1 == mice2:
                mice2 = int(randy.uniform(0,1) * self.selectionRate * self.population)
            
            
            crossoverPoint = randy.randint(0, self.LenDNA) + 1
            
            self.miceList.append(Mice(self.LenDNA, self.world))
            self.miceList.append(Mice(self.LenDNA, self.world))

            for j in range(self.LenDNA):
                if j < crossoverPoint:
                    self.miceList[2*k].dna[j] = self.selectedMice[mice1].dna[j]
                    self.miceList[2*k + 1].dna[j] = self.selectedMice[mice2].dna[j]
                else:
                    self.miceList[2*k].dna[j] = self.selectedMice[mice2].dna[j]
                    self.miceList[2*k+1].dna[j] = self.selectedMice[mice1].dna[j]
            
        
    def mutation(self):
        DNA_genes = [self.GO_LEFT_c, self.GO_UP_c, self.GO_RIGHT_c, self.GO_DOWN_c ]
        for i in range(self.population):
            for j in range(self.LenDNA):
                if randy.uniform(0,1) < self.mutationRate:
                    choice = randy.randint(0, 3)
                    self.miceList[i].dna[j] = DNA_genes[choice]
            #self.fitnessCalculation(self.miceList[i])
    
    def CalculateFitnessPop(self):
        for i in range(self.population):
            self.fitnessCalculation(self.miceList[i])



        

