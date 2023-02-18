from World import World
from Genetic import Genetic
import timeit
import copy
import pygame
import time
import os
import csv
import psutil

process = psutil.Process(os.getpid())
os.environ['SDL_VIDEO_CENTERED'] = '1'


RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

def draw_grid(win, rows, width):			#Dibuja la cuadricula
	gap = width // rows
	for i in range(rows):
		pygame.draw.line(win, GREY, (0, i * gap), (width, i*gap))
	for j in range(rows):
		pygame.draw.line(win, GREY, (j * gap, 0), (j*gap, width))

def draw_pose(win, rows, width, pose, color):
    gap = width//rows
    x = pose[0]
    y = rows - pose[1] - 1
    C_x = x*gap
    C_y = y*gap
    pygame.draw.rect(win, color, (C_x, C_y, gap, gap))
    pygame.display.update()

def draw_mice(win, rows, width, grid, mice, color):
    pose = copy.copy(start)
    print(mice.numberOfSuccessfulMove)
    MOV = {"L": [-1, 0], "R": [1,0], "U": [0,1], "D": [0,-1]}
    draw_pose(win, rows, width, pose, GREEN)
    for i in range(mice.numberOfSuccessfulMove):
        c = mice.dna[i]
        pose = [sum(x) for x in zip(pose, MOV[c])]
        if pose not in grid:
            print("Invalid position by mice")
            break
        draw_pose(win, rows, width, pose, color)
        pygame.event.pump()

def draw_obstacles(win, rows, width, obstacles):
    for i in range(len(obstacles)):
        draw_pose(win, rows, width, obstacles[i], BLACK)
        pygame.event.pump()
      
def draw(win, rows, width, obstacles):
    win.fill(WHITE)
    draw_grid(win, rows, width)
    draw_obstacles(win, rows, width, obstacles)
    pygame.display.update()

def make_grid(w, h):
    X = []
    for x in range(w):
        for y in range(h):
            X.append([x,y])
    return X

def check_pose(start, mice):
    pose = copy.copy(start)
    print(mice.numberOfSuccessfulMove)
    MOV = {"L": [-1, 0], "R": [1,0], "U": [0,1], "D": [0,-1]}
    for i in range(mice.numberOfSuccessfulMove):
        c = mice.dna[i]
        pose = [sum(x) for x in zip(pose, MOV[c])]
    return pose

if __name__ == "__main__":
    starttime = timeit.default_timer()
    population = 60
    LenDNA = 40
    selectionRate = 0.05
    mutationRate = 0.1 #0.01
    distanceMethod = 1   #Euclidian method
    
    rows = 20
    grid = make_grid(rows,rows)
    



    n_generation = 0
    cont_flag = True
    generations = 80

    nmap = 3
    res = 2

    maps = ("Maps/map01.csv", "Maps/map02.csv", "Maps/map03.csv", "Maps/map04.csv")

    obstacles = []
    with open(maps[nmap], newline='') as f:
	    reader = csv.reader(f)
	    data = list(reader)

    data = [list(map(lambda x: int(float(x)), x)) for x in data]  #Transforming all the strings to ints

    for line in data:
        for k in range((line[3]+1)*res - (res-1)):
            for j in range((line[2]+1)*res - (res-1)):
                obs = (line[0]*res+j, line[1]*res+k)
                obstacles.append(obs)
    
    w = World(grid, obstacles)
    start = [1*res,1*res]
    stop = [8*res,8*res]
    w.setStart(start[0],start[1])
    w.setStop(stop[0],stop[1])
    #print(w.obstacles)


    #Graphic
    WIDTH = 800
    WIN = pygame.display.set_mode((WIDTH, WIDTH))
    pygame.display.set_caption("GA path planning")
    draw(WIN, rows, WIDTH, obstacles)

    g = Genetic(population, LenDNA, w, selectionRate, mutationRate, distanceMethod)
    print("Genetic generated")
    g.CalculateFitnessPop()

    while cont_flag:
        n_generation += 1
        print(f"Generation: {n_generation} ")
        #print("Selection...")
        g.selection()
        best_mice = g.miceList[0]
        print(f"bestfit: {best_mice.fitness}")
        #Graphic

        pygame.display.set_caption(f"GA path planning       Generation: {n_generation}      Bestfit: {best_mice.fitness}        Moves: {best_mice.numberOfSuccessfulMove}      time: {timeit.default_timer() - starttime}")
        draw(WIN, rows, WIDTH, obstacles)

        draw_pose(WIN, rows, WIDTH, stop, RED)
        draw_mice(WIN, rows, WIDTH, grid, best_mice, BLUE)
        

        g.crossover()
        g.mutation()
        g.CalculateFitnessPop()
        if n_generation == generations:
            break
    g.CalculateFitnessPop()
    g.miceList.sort(key=lambda x: x.fitness, reverse = True)
    best_mice = g.miceList[0]
    draw(WIN, rows, WIDTH, obstacles)
    
    draw_pose(WIN, rows, WIDTH, stop, RED)
    draw_mice(WIN, rows, WIDTH, grid, best_mice, BLUE)
    draw_pose(WIN, rows, WIDTH, stop, RED)

    print(best_mice.dna, best_mice.fitness)
    print(check_pose(start, g.miceList[0]))

    print("Ruta: ")
    print(best_mice.dna[:best_mice.numberOfSuccessfulMove])
    print("Movimientos: ",best_mice.numberOfSuccessfulMove )

    print(f"Execution time: {timeit.default_timer() - starttime} seconds")
    print((process.memory_info().rss/1024)/1024)  # in bytes 
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
    


