# -*- coding: utf-8 -*-
import pygame
import random
import numpy as np
from collections import deque


BLOCKTYPES = 5


# třída reprezentující prostředí
class Env:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.arr = np.zeros((height, width), dtype=int)
        self.startx = 0
        self.starty = 0
        self.goalx = width-1
        self.goaly = height-1
        
    def is_valid_xy(self, x, y):      
        if x >= 0 and x < self.width and y >= 0 and y < self.height and self.arr[y, x] == 0:
            return True
        return False 
        
    def set_start(self, x, y):
        if self.is_valid_xy(x, y):
            self.startx = x
            self.starty = y
            
    def set_goal(self, x, y):
        if self.is_valid_xy(x, y):
            self.goalx = x
            self.goaly = y
               
        
    def is_empty(self, x, y):
        if self.arr[y, x] == 0:
            return True
        return False

    def add_block(self, x, y):
        if self.arr[y, x] == 0:
            r = random.randint(1, BLOCKTYPES)
            self.arr[y, x] = r
                
    def get_neighbors(self, x, y):
        l = []
        if x-1 >= 0 and self.arr[y, x-1] == 0:
            l.append((x-1, y))
        
        if x+1 < self.width and self.arr[y, x+1] == 0:
            l.append((x+1, y))
            
        if y-1 >= 0 and self.arr[y-1, x] == 0:
            l.append((x, y-1))
        
        if y+1 < self.height and self.arr[y+1, x] == 0:
            l.append((x, y+1))
        
        return l

    def get_tile_type(self, x, y):
        return self.arr[y, x]
    
    
    # vrací dvojici 1. frontu dvojic ze startu do cíle, 2. seznam dlaždic
    # k zobrazení - hodí se např. pro zvýraznění cesty, nebo expandovaných uzlů
    # start a cíl se nastaví pomocí set_start a set_goal
    # <------    ZDE vlastní metoda
    def path_planner(self):
        # přímo zadrátovaná cesta z bodu (1, 0) do (9, 7)
        def easy_path():
            d = deque()

            d.appendleft((9, 7))
            d.appendleft((9, 6))
            d.appendleft((9, 5))
            d.appendleft((9, 4))
            d.appendleft((9, 3))
            d.appendleft((9, 2))
            d.appendleft((9, 1))
            d.appendleft((9, 0))
            d.appendleft((8, 0))
            d.appendleft((7, 0))
            d.appendleft((6, 0))
            d.appendleft((5, 0))
            d.appendleft((4, 0))
            d.appendleft((3, 0))
            d.appendleft((2, 0))
            d.appendleft((1, 0))

            print(d)
            return d

        def greedy_search():
            d = deque()
            walked_path = []
            heuristic_length = (self.startx - self.goalx) ** 2 + (self.starty - self.goaly) ** 2
            ufo_x, ufo_y = self.startx, self.starty

            d.append((ufo_x, ufo_y))
            walked_path.append((ufo_x, ufo_y))

            while heuristic_length != 0:
                possible_closer_paths = {}
                print("Ufo position:", ufo_x, ufo_y)

                for neigh in self.get_neighbors(ufo_x, ufo_y):
                    if self.is_empty(neigh[0], neigh[1]) and (neigh[0], neigh[1]) not in d:
                        temp_heur = (neigh[0] - self.goalx) ** 2 + (neigh[1] - self.goaly) ** 2
                        if temp_heur <= heuristic_length:
                            possible_closer_paths[temp_heur] = (neigh[0], neigh[1])

                if possible_closer_paths:
                    shortest_heur_path = min(possible_closer_paths.keys())
                    shortest_neigh = possible_closer_paths[shortest_heur_path]
                    ufo_x, ufo_y = shortest_neigh
                    heuristic_length = shortest_heur_path
                    d.append((ufo_x, ufo_y))
                    walked_path.append((ufo_x, ufo_y))
                else:
                    walked_path.pop()
                    ufo_x, ufo_y = walked_path[-1]
                    heuristic_length = (ufo_x - self.goalx) ** 2 + (ufo_y - self.goaly) ** 2

            print(d)
            return d

        def dijkstr_search():
            d = deque()
            visited = set()
            step_by_step_path = {}
            ufo_x, ufo_y = self.startx, self.starty

            queue = [(0, (ufo_x, ufo_y))]
            costs = {(ufo_x, ufo_y): 0}

            while queue:
                queue.sort()
                cost, (ufo_x, ufo_y) = queue.pop(0)

                for neighboor in self.get_neighbors(ufo_x, ufo_y):
                    if self.is_empty(neighboor[0], neighboor[1]) and neighboor not in visited:
                        if neighboor not in costs or costs[neighboor] > cost + 1:
                            costs[neighboor] = cost + 1
                            queue.append((cost + 1, neighboor))
                            step_by_step_path[neighboor] = (ufo_x, ufo_y)

                visited.add((ufo_x, ufo_y))

            if (self.goalx, self.goaly) in step_by_step_path:
                step = (self.goalx, self.goaly)
                while step != (self.startx, self.starty):
                    d.appendleft(step)
                    step = step_by_step_path[step]

            print(d)
            return d

        def a_star_search():
            d = deque()
            visited = set()
            ufo_x, ufo_y = self.startx, self.starty
            step_by_step_path = {}

            heuristic = (ufo_x - self.goalx) ** 2 + (ufo_y - self.goaly) ** 2
            g_cost = {(ufo_x, ufo_y): 0}
            f_cost = {(ufo_x, ufo_y): heuristic + g_cost[(ufo_x, ufo_y)]}
            queue = [(f_cost[(ufo_x, ufo_y)], (ufo_x, ufo_y))]

            while queue:
                queue.sort()
                current_heuristic, (ufo_x, ufo_y) = queue.pop(0)
                current_walk_length = g_cost[(ufo_x, ufo_y)]

                for neigh in self.get_neighbors(ufo_x, ufo_y):
                    if self.is_empty(neigh[0], neigh[1]) and neigh not in visited:
                        if neigh not in g_cost or g_cost[neigh] > current_walk_length + 1:
                            g_cost[neigh] = current_walk_length + 1
                            heuristic = (neigh[0] - self.goalx) ** 2 + (neigh[1] - self.goaly) ** 2
                            f_cost[neigh] = heuristic + g_cost[neigh]

                            queue.append((f_cost[neigh], neigh))
                            step_by_step_path[neigh] = (ufo_x, ufo_y)

            # Reconstruct the path
            if (self.goalx, self.goaly) in step_by_step_path:
                step = (self.goalx, self.goaly)
                while step != (self.startx, self.starty):
                    d.appendleft(step)
                    step = step_by_step_path[step]

            return d

        #d = easy_path()
        d = greedy_search()
        #d = dijkstr_search()
        #d = a_star_search()

        return d, list(d)
    
       
        
# třída reprezentující ufo        
class Ufo:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.path = deque()
        self.tiles = []

    # přemístí ufo na danou pozici - nejprve je dobré zkontrolovat u prostředí, 
    # zda je pozice validní
    def move(self, x, y):
        self.x = x
        self.y = y
    
    # reaktivní navigace <------------------------ !!!!!!!!!!!! ZDE DOPLNIT
    def reactive_go(self, env):
        r = random.random()
        
        dx = 0
        dy = 0
        
        if r > 0.5: 
            r = random.random()
            if r < 0.5:
                dx = -1
            else:
                dx = 1
            
        else:
            r = random.random()
            if r < 0.5:
                dy = -1
            else:
                dy = 1
        
        return (self.x + dx, self.y + dy)
        
    
    # nastaví cestu k vykonání 
    def set_path(self, p, t=[]):
        self.path = p
        self.tiles = t
   
    
    # vykoná naplánovanou cestu, v každém okamžiku na vyzvání vydá další
    # way point 
    def execute_path(self):
        if self.path:
            return self.path.popleft()
        return (-1, -1)
       




# definice prostředí -----------------------------------

TILESIZE = 50



#<------    definice prostředí a překážek !!!!!!

WIDTH = 15
HEIGHT = 15

env = Env(WIDTH, HEIGHT)

env.add_block(1, 1)
env.add_block(2, 2)
env.add_block(3, 3)
env.add_block(4, 4)
env.add_block(5, 5)
env.add_block(6, 6)
env.add_block(7, 7)
env.add_block(8, 8)
env.add_block(9, 9)
#env.add_block(10, 10)
env.add_block(0, 8)

env.add_block(11, 1)
env.add_block(11, 6)
env.add_block(1, 3)
env.add_block(2, 4)
env.add_block(4, 5)
env.add_block(2, 6)
env.add_block(3, 7)
env.add_block(4, 8)
env.add_block(0, 8)


env.add_block(1, 8)
env.add_block(2, 8)
env.add_block(3, 5)
env.add_block(4, 8)
env.add_block(5, 6)
env.add_block(6, 4)
env.add_block(9, 2)
env.add_block(8, 1)

env.add_block(11, 8)
env.add_block(12, 8)
env.add_block(13, 8)
env.add_block(14, 8)

env.add_block(9, 11)
env.add_block(9, 12)
env.add_block(9, 13)


# pozice ufo <--------------------------
ufo = Ufo(env.startx, env.starty)

WIN = pygame.display.set_mode((env.width * TILESIZE, env.height * TILESIZE))

pygame.display.set_caption("Block world")

pygame.font.init()

WHITE = (255, 255, 255)



FPS = 2



# pond, tree, house, car

BOOM_FONT = pygame.font.SysFont("comicsans", 100)   
LEVEL_FONT = pygame.font.SysFont("comicsans", 20)   


TILE_IMAGE = pygame.image.load("tile.jpg")
MTILE_IMAGE = pygame.image.load("markedtile.jpg")
HOUSE1_IMAGE = pygame.image.load("house1.jpg")
HOUSE2_IMAGE = pygame.image.load("house2.jpg")
HOUSE3_IMAGE = pygame.image.load("house3.jpg")
TREE1_IMAGE  = pygame.image.load("tree1.jpg")
TREE2_IMAGE  = pygame.image.load("tree2.jpg")
UFO_IMAGE = pygame.image.load("ufo.jpg")
FLAG_IMAGE = pygame.image.load("flag.jpg")


TILE = pygame.transform.scale(TILE_IMAGE, (TILESIZE, TILESIZE))
MTILE = pygame.transform.scale(MTILE_IMAGE, (TILESIZE, TILESIZE))
HOUSE1 = pygame.transform.scale(HOUSE1_IMAGE, (TILESIZE, TILESIZE))
HOUSE2 = pygame.transform.scale(HOUSE2_IMAGE, (TILESIZE, TILESIZE))
HOUSE3 = pygame.transform.scale(HOUSE3_IMAGE, (TILESIZE, TILESIZE))
TREE1 = pygame.transform.scale(TREE1_IMAGE, (TILESIZE, TILESIZE))
TREE2 = pygame.transform.scale(TREE2_IMAGE, (TILESIZE, TILESIZE))
UFO = pygame.transform.scale(UFO_IMAGE, (TILESIZE, TILESIZE))
FLAG = pygame.transform.scale(FLAG_IMAGE, (TILESIZE, TILESIZE))




        
        
        

def draw_window(ufo, env):

    for i in range(env.width):
        for j in range(env.height):
            t = env.get_tile_type(i, j)
            if t == 1:
                WIN.blit(TREE1, (i*TILESIZE, j*TILESIZE))
            elif t == 2:
                WIN.blit(HOUSE1, (i*TILESIZE, j*TILESIZE))
            elif t == 3:
                WIN.blit(HOUSE2, (i*TILESIZE, j*TILESIZE))
            elif t == 4:
                WIN.blit(HOUSE3, (i*TILESIZE, j*TILESIZE))  
            elif t == 5:
                WIN.blit(TREE2, (i*TILESIZE, j*TILESIZE))     
            else:
                WIN.blit(TILE, (i*TILESIZE, j*TILESIZE))
    
        
    for (x, y) in ufo.tiles:
        WIN.blit(MTILE, (x*TILESIZE, y*TILESIZE))
        
    
    WIN.blit(FLAG, (env.goalx * TILESIZE, env.goaly * TILESIZE))        
    WIN.blit(UFO, (ufo.x * TILESIZE, ufo.y * TILESIZE))
        
    pygame.display.update()
    
    
    

def main():
    goal_printed = False
    
    #  <------------   nastavení startu a cíle prohledávání !!!!!!!!!!
    env.set_start(0, 0)
    env.set_goal(12, 12)
    
    p, t = env.path_planner()   # cesta pomocí path_planneru prostředí
    print("Ufo parth:", p, t)
    ufo.set_path(p, t)
    # ---------------------------------------------------
    
    clock = pygame.time.Clock()
    run = True
    go = False
    
    while run:

        clock.tick(FPS)
        
        # <---- reaktivní pohyb dokud nedojde do cíle 
        if (ufo.x != env.goalx) or (ufo.y != env.goaly):        
            #x, y = ufo.reactive_go(env)

            x, y = ufo.execute_path()
            
            if env.is_valid_xy(x, y):
                ufo.move(x, y)
            else:
                print('[', x, ',', y, ']', "wrong coordinate !")
        elif not goal_printed:
            print("Goal reached!!!")
            goal_printed = True

        draw_window(ufo, env)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

    pygame.quit()    


if __name__ == "__main__":
    main()