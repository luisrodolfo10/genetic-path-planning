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
            #self.fitnessCalculation(self.miceList[i])

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
    
    def fitnessCalculation(self, mice, target, start, MOV):
        current = copy.copy(self.world.getStart())
        # MOV = {"L": [-1, 0], "R": [1,0], "U": [0,1], "D": [0,-1]}
        penalty = 0
        obs_penalty = 0
        near_obst_p = 0
        for i in range(mice.LenDNA):
            if i != 0:
                penalty += self.isPenalty(mice, i)
            c = mice.dna[i]
            current = [sum(x) for x in zip(current, MOV[c])]
            if current == target:
                break
            if self.world.isObstacle(current[0], current[1]):
                #i = 149 #LenDNA - 1
                obs_penalty += 1
            if self.world.near_obst(current[0], current[1]):
                near_obst_p += 1
                
                
        numberOfSuccessfulMove = i + 1 
        mice.numberOfSuccessfulMove = numberOfSuccessfulMove

        #Target Found
        maxDistance = self.deterministic(start[0], start[1], target[0], target[1])
        currentDistance = self.deterministic(current[0],current[1], target[0], target[1]) 
        mice.fitness = self.MAX_POINT * (1 - (currentDistance / maxDistance))
        mice.fitness *= (1 - (obs_penalty/mice.LenDNA) * 0.6)
        mice.fitness *= (1 - (near_obst_p/mice.LenDNA*2) * 0.6)
        mice.fitness *= (1-(numberOfSuccessfulMove/mice.LenDNA)*0.8)  #PB 0.64, 0.75
        mice.fitness -= penalty*0.5  #PB 0.4-0.6


    def showFitness(self):
        for i in range(self.population):
            self.fitnessCalculation(self.miceList[i])
            
    
    def selection(self):
        self.miceList.sort(key=lambda x: x.fitness, reverse = True)
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
        target = self.world.getStop()
        start = self.world.getStart()
        MOV = {"L": [-1, 0], "R": [1,0], "U": [0,1], "D": [0,-1]}
        for i in range(self.population):
            self.fitnessCalculation(self.miceList[i], target, start, MOV)



        

