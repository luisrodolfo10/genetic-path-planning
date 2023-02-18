import random as randy

class Mice:
    def __init__(self, LenDNA, world):
        self.LenDNA = LenDNA
        self.world = world
        self.dna = [0]*(LenDNA + 1)
        self.successPath = ""
        self.fitness = int
        self.numberOfSuccessfulMove = int
    
    def createDNA(self, Genetic):
        DNA_genes = [Genetic.GO_LEFT_c, Genetic.GO_UP_c, Genetic.GO_RIGHT_c, Genetic.GO_DOWN_c ]
        for i in range(self.LenDNA):
            choice = randy.randint(0,3)
            self.dna[i] = DNA_genes[choice]

    def showDNA(self):
        print(self.dna)
    
    def compareTo(self, Mice):
        if (self.fitness == Mice.fitness):
            return 0
        elif (self.fitness > Mice.fitness):
            return -1
        else:
            return 1

    # def __cmp__(self, mice2):
    #     if self.fitness < mice2.fitness:
    #         return 1
    #     elif self.fitness > mice2.fitness:
    #         return -1
    #     else:
    #         return 0

    def __lt__(self, other):
        if isinstance(self.fitness, type) == isinstance(other.fitness, type):
            return 0
        else:
            return self.fitness < other.fitness
    
    def __gt__(self, other):
        return self.fitness > other.fitness

    def __eq__(self, other):
        return self.fitness == self.fitness