# -*- coding: utf-8 -*-
"""
Úkol č.7 pro předmět Umělá Inteligence.
Skoro všechny funkce již byly předpřipravené profesorem.
!!!
    Úkolem je vyplnit funkce a logiku, kde se zoobrazuje komentář s textem "ZDE LOGIKA".
    Části, kterí obsahují jenom komentář "ZDE" lze měnit a nastavovat
!!!
"""
import pygame
import numpy as np
import random
import math
from deap import base
from deap import creator
from deap import tools


pygame.font.init()


# -----------------------------------------------------------------------------
# Parametry hry 
# -----------------------------------------------------------------------------

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
WHITE = (255, 255, 255)

TITLE = "Boom Master"
pygame.display.set_caption(TITLE)

FPS = 80
ME_VELOCITY = 5
MAX_MINE_VELOCITY = 3

BOOM_FONT = pygame.font.SysFont("comicsans", 100)   
LEVEL_FONT = pygame.font.SysFont("comicsans", 20)   

ENEMY_IMAGE = pygame.image.load("mine.png")
ME_IMAGE = pygame.image.load("me.png")
SEA_IMAGE = pygame.image.load("sea.png")
FLAG_IMAGE = pygame.image.load("flag.png")

ENEMY_SIZE = 50
ME_SIZE = 50

ENEMY = pygame.transform.scale(ENEMY_IMAGE, (ENEMY_SIZE, ENEMY_SIZE))
ME = pygame.transform.scale(ME_IMAGE, (ME_SIZE, ME_SIZE))
SEA = pygame.transform.scale(SEA_IMAGE, (WIDTH, HEIGHT))
FLAG = pygame.transform.scale(FLAG_IMAGE, (ME_SIZE, ME_SIZE))


# ----------------------------------------------------------------------------
# třídy objektů 
# ----------------------------------------------------------------------------


# trida reprezentujici minu
class Mine:
    """
    Object representing the MINE in the game field.

    Attributes:
        dirx        The X direction to which Mine will go
        diry        The Y direction to which Mine will go
        rect        The Invisible border for game objects manipulation, specified by ENEMY_SIZE
        velocity    The speed of Mine
    """
    def __init__(self):

        # random x direction
        if random.random() > 0.5:
            self.dirx = 1
        else: 
            self.dirx = -1
            
        # random y direction    
        if random.random() > 0.5:
            self.diry = 1
        else: 
            self.diry = -1

        x = random.randint(200, WIDTH - ENEMY_SIZE) 
        y = random.randint(200, HEIGHT - ENEMY_SIZE) 
        self.rect = pygame.Rect(x, y, ENEMY_SIZE, ENEMY_SIZE)
        
        self.velocity = random.randint(1, MAX_MINE_VELOCITY)

  
# trida reprezentujici me, tedy meho agenta        
class Me:
    """
    Object representing our Agent, in other words ME

    Attributes:
        rect        The Invisible border for game objects manipulation, specified by ME_SIZE
        alive       Controls if our agent is still alive in game
        won         Controls if our agent reached the flag / goal
        timealive   How long our agent was alive
        sequence    Weights sequence, which every agent has unique and uses it for its decisions and movements
        fitness     How well the agent played our game
        dist        Distance ???
    """
    def __init__(self):
        self.rect = pygame.Rect(10, random.randint(1, 300), ME_SIZE, ME_SIZE)
        self.alive = True
        self.won = False
        self.timealive = 0
        self.sequence = []
        self.fitness = 0
        self.dist = 0
    
    
# třída reprezentující cíl = praporek    
class Flag:
    """
    Object representing the Flag (Goal of every round)

    Attributes:
        rect        The Invisible border for game objects manipulation, specified by ME_SIZE
    """
    def __init__(self):
        self.rect = pygame.Rect(WIDTH - ME_SIZE, HEIGHT - ME_SIZE - 10, ME_SIZE, ME_SIZE)
        

# třída reprezentující nejlepšího jedince - hall of fame   
class Hof:
    """
    Object representing the best agent / individual of the game

    Attributes:
        sequence    The weights code of the individual
    """
    def __init__(self):
        self.sequence = []

    
# -----------------------------------------------------------------------------    
# nastavení herního plánu    
# -----------------------------------------------------------------------------
    

# rozestavi miny v danem poctu num
def set_mines(num: int) -> list[Mine]:
    """
    Sets up new mines in the game.

    :param int num: Tells how many mines should be created
    :return: List of the Objects Mine
    """
    l = []
    for i in range(num):
        m = Mine()
        l.append(m)
        
    return l
    

# inicializuje me v poctu num na start 
def set_mes(num: int) -> list[Me]:
    """
    Sets up new agents (mes) in the game

    :param int num: Tells how many mes should be created
    :return: List of the Objects Me
    """
    l = []
    for i in range(num):
        m = Me()
        l.append(m)
        
    return l


# zresetuje vsechny mes zpatky na start
def reset_mes(mes: list[Me()], pop: int):
    """
    Resets all mes into default position and alive state to start new round

    :param list[Me()] mes: List of the Objects Me
    :param int pop: Amount of Mes population
    """
    for i in range(len(pop)):
        me = mes[i]
        me.rect.x = 10
        me.rect.y = 10
        me.alive = True
        me.dist = 0
        me.won = False
        me.timealive = 0
        me.sequence = pop[i]
        me.fitness = 0


# -----------------------------------------------------------------------------    
# senzorické funkce 
# -----------------------------------------------------------------------------
def my_senzor(me: Me, flag: Flag, mines: list[Mine], sensor_len: int) -> tuple:
    """
    Seensoric function returning the position of the visible mine, me position and flag position

    :param me: Object Instance of Me
    :param flag: Object instance of Flag
    :param mines: List of Objects Mine
    :param sensor_len: Sensor length, to which every Me can see
    :return: tuple of the values in order: (Mine Y over me, Mine Y below me, Mine X front of me, Mine X behind me,
    my_pos(x,y, flag_pos(x,y)
    """
    # <----- ZDE LOGIKA je prostor pro vlastní senzorické funkce !!!!
    my_pos = (me.rect.x, me.rect.y)
    flag_pos = (flag.rect.x, flag.rect.y)

    for mine in mines:
        mine_pos = (mine.rect.x, mine.rect.y)

        x_difference = my_pos[0] - mine_pos[0]
        y_difference = my_pos[1] - mine_pos[1]

        # (Y over me, Y below me, X front of me, X behind me, flag_diff)
        if 0 < y_difference <= sensor_len:
            if 0 < x_difference <= sensor_len:
                return abs(y_difference), 0, 0, abs(x_difference), my_pos, flag_pos

            elif 0 > x_difference >= -sensor_len:
                return abs(y_difference), 0, abs(x_difference), 0, my_pos, flag_pos

        # (Y over me, Y below me, X front of me, X behind me, flag_diff)
        elif 0 > y_difference >= -sensor_len:
            if 0 < x_difference <= sensor_len:
                return 0, abs(y_difference), 0, abs(x_difference), my_pos, flag_pos
            elif 0 > x_difference >= -sensor_len:
                return 0, abs(y_difference), abs(x_difference), 0, my_pos, flag_pos

    # (Y over me, Y below me, X front of me, X behind me, flag_diff)
    return 0, 0, 0, 0, my_pos, flag_pos


# ---------------------------------------------------------------------------
# funkce řešící pohyb agentů
# ----------------------------------------------------------------------------


# konstoluje kolizi 1 agenta s minama, pokud je kolize vraci True
def me_collision(me: Me, mines: list[Mine]) -> bool:
    """
    Validates if agent Me collided with any mine in game

    :param me: Object Instance of Me
    :param mines: List of the Objects Mine
    :return: Bool if agent collided or not
    """
    for mine in mines:
        if me.rect.colliderect(mine.rect):
            #pygame.event.post(pygame.event.Event(ME_HIT))
            return True
    return False
            
            
# kolidujici agenti jsou zabiti, a jiz se nebudou vykreslovat
def mes_collision(mes: list[Me], mines: list[Mine]):
    """
    Verifies every agent if he is collided with mine only when he is still alive and didn't win the round

    :param mes: List of the Objects Me
    :param mines: List of the Objects Mine
    :return: Sets an attribute alive to False for Me, which collided
    """
    for me in mes: 
        if me.alive and not me.won:
            if me_collision(me, mines):
                me.alive = False
            
            
# vraci True, pokud jsou vsichni mrtvi Dave            
def all_dead(mes: list[Me]) -> bool:
    """
    Verifies of agents Me are dead or not

    :param mes: List of the Objects Me
    :return: Bool value if all of them are dead or not (at least one is still alive)
    """
    for me in mes: 
        if me.alive:
            return False
    
    return True


# vrací True, pokud již nikdo nehraje - mes jsou mrtví nebo v cíli
def nobodys_playing(mes: list[Me]) -> bool:
    """
    Verifies if nobody is still playing the game (they are either dead or won the round)

    :param mes: List of the Objects Me
    :return: Bool if nobody is playing the or at least one is still in the game
    """
    for me in mes: 
        if me.alive and not me.won:
            return False
    
    return True


# rika, zda agent dosel do cile
def me_won(me: Me, flag: Flag) -> bool:
    """
    Verifies if agent Me reached the Flag or not

    :param me: Object Instance of Me
    :param flag: Object Instance of Flag
    :return: Bool if agent Me reached the Flag
    """
    if me.rect.colliderect(flag.rect):
        return True
    
    return False


# vrací počet živých mes
def alive_mes_num(mes: list[Me]) -> int:
    """
    Counts how many agents Me are still alive

    :param mes: List of the Objects Me
    :return: Number of alive agents Me
    """
    c = 0
    for me in mes:
        if me.alive:
            c += 1
    return c


# vrací počet mes co vyhráli
def won_mes_num(mes: list[Me]) -> int:
    """
    Counts how many agents Me won the round

    :param mes: List of the Objects Me
    :return: Number of winners
    """
    c = 0
    for me in mes: 
        if me.won:
            c += 1
    return c


# resi pohyb miny        
def handle_mine_movement(mine: Mine):
    """
    Function that handles the Mine movements so when it hits the wall, it jumps of the wall at the same angle

    :param mine: Object Instance of Mine
    :return: Sets up the mine.rect.x and mine.rect.y position by their velocity * x/y direction
    """
    if mine.dirx == -1 and mine.rect.x - mine.velocity < 0:
        mine.dirx = 1
       
    if mine.dirx == 1 and mine.rect.x + mine.rect.width + mine.velocity > WIDTH:
        mine.dirx = -1

    if mine.diry == -1 and mine.rect.y - mine.velocity < 0:
        mine.diry = 1
    
    if mine.diry == 1 and mine.rect.y + mine.rect.height + mine.velocity > HEIGHT:
        mine.diry = -1
         
    mine.rect.x += mine.dirx * mine.velocity
    mine.rect.y += mine.diry * mine.velocity


# resi pohyb min
def handle_mines_movement(mines: list[Mine]):
    """
    Function that is a for cycle for each "handle_mine_movement" function call

    :param mines: List of the Objects Mine
    """
    for mine in mines:
        handle_mine_movement(mine)


#----------------------------------------------------------------------------
# vykreslovací funkce 
#----------------------------------------------------------------------------


# vykresleni okna
def draw_window(mes: list[Me], mines: list[Mine], flag: Flag, level: int, generation: int, timer: int):
    """
    Function that draws the game windows so that player can see what is going on

    :param mes: List of the Objects Me
    :param mines: List of the Objects Me
    :param flag: Object Instance of Flag
    :param level: Number of the level (correlates to the mines amount)
    :param generation: Generation of the agents Me
    :param timer: Passed game time for the round
    :return: Updates the display window
    """
    WIN.blit(SEA, (0, 0))   
    
    t = LEVEL_FONT.render("level: " + str(level), 1, WHITE)   
    WIN.blit(t, (10, HEIGHT - 30))
    
    t = LEVEL_FONT.render("generation: " + str(generation), 1, WHITE)   
    WIN.blit(t, (150, HEIGHT - 30))
    
    t = LEVEL_FONT.render("alive: " + str(alive_mes_num(mes)), 1, WHITE)   
    WIN.blit(t, (350, HEIGHT - 30))
    
    t = LEVEL_FONT.render("won: " + str(won_mes_num(mes)), 1, WHITE)   
    WIN.blit(t, (500, HEIGHT - 30))
    
    t = LEVEL_FONT.render("timer: " + str(timer), 1, WHITE)   
    WIN.blit(t, (650, HEIGHT - 30))

    WIN.blit(FLAG, (flag.rect.x, flag.rect.y))    
         
    # vykresleni min
    for mine in mines:
        WIN.blit(ENEMY, (mine.rect.x, mine.rect.y))
        
    # vykresleni me
    for me in mes: 
        if me.alive:
            WIN.blit(ME, (me.rect.x, me.rect.y))
        
    pygame.display.update()


def draw_text(text: str):
    """
    Function that draws the text into the game window

    :param text: Text we want to draw into the window
    :return: Updates the window to show text
    """
    t = BOOM_FONT.render(text, 1, WHITE)   
    WIN.blit(t, (WIDTH // 2, HEIGHT // 2))
    
    pygame.display.update()
    pygame.time.delay(1000)


#-----------------------------------------------------------------------------
# funkce reprezentující neuronovou síť, pro inp vstup a zadané váhy wei, vydá
# čtveřici výstupů pro nahoru, dolu, doleva, doprava    
#----------------------------------------------------------------------------


# <----- ZDE LOGIKA je místo pro  vlastní funkci !!!!


# funkce reprezentující výpočet neuronové funkce
# funkce dostane na vstupu vstupy neuronové sítě inp, a váhy hran wei
# vrátí seznam hodnot výstupních neuronů
def nn_function(inp: list, wei: list) -> list:
    """
    Function tha represents the neurons of the agents

    :param inp: Inputs saved from the sensor function
    :param wei: Weights of each action, represented by sequence attribute of object Me
    :return: List of the actions that represents going [up, down, left, right]
    """
    # < ------ ZDE LOGIKA funkce neuronové sítě
    # (Y over me, Y below me, X front of me, X behind me, my_pos(x, y), flag_pos(x, y))
    # [(0, 0, 0, 0, (840, 430), (500, 400))]

    # [Go down, Go up, Go left, Go right]
    output = [0, 0, 0, 0]

    #print(inp)
    #print(wei)

    # Write if ME must go some way because of MINE DANGER
    # Go DOWN from MINE
    output[0] = inp[0] * wei[0]
    # Go UP from MINE
    output[1] = inp[1] * wei[1]
    # Go LEFT from MINE
    output[2] = inp[2] * wei[2]
    # Go RIGHT from MINE
    output[3] = inp[3] * wei[3]

    # Adjusting movement based on flag position
    # Y axis adjustment
    if inp[4][1] < inp[5][1]:
        # Go down
        output[0] += wei[4]
    elif inp[4][1] > inp[5][1]:
        # Go up
        output[1] += wei[5]

    # X axis adjustment
    if inp[4][0] > inp[5][0]:
        # Go left
        output[2] += wei[6]
    elif inp[4][0] < inp[5][0]:
        # Go right
        output[3] += wei[7]

    return output


# naviguje jedince pomocí neuronové sítě a jeho vlastní sekvence v něm schované
def nn_navigate_me(me: Me, inp: list):
    """
    Function that uses neuron output as a inputs for its movement action

    :param me: Object Instance of Me
    :param inp: inputs for the specified agent Me
    :return: Change in the agents x/y position by its velocity
    """
    # <------ ZDE LOGIKA - čtení výstupu z neuronové sítě
    out = np.array(nn_function(inp, me.sequence))
    ind = np.where(out == max(out))[0][0]

    # dolu, pokud není zeď
    if out[0] > 0 and ind == 0 and me.rect.y + me.rect.height + ME_VELOCITY < HEIGHT:
        me.rect.y += ME_VELOCITY
        me.dist += ME_VELOCITY

    # nahoru, pokud není zeď
    if out[1] > 0 and ind == 1 and me.rect.y - ME_VELOCITY > 0:
        me.rect.y -= ME_VELOCITY
        me.dist += ME_VELOCITY

    # doleva, pokud není zeď
    if out[2] > 0 and ind == 2 and me.rect.x - ME_VELOCITY > 0:
        me.rect.x -= ME_VELOCITY
        me.dist += ME_VELOCITY
        
    # doprava, pokud není zeď    
    if out[3] > 0 and ind == 3 and me.rect.x + me.rect.width + ME_VELOCITY < WIDTH:
        me.rect.x += ME_VELOCITY
        me.dist += ME_VELOCITY


# updatuje, zda me vyhrali 
def check_mes_won(mes: list[Me], flag: Flag):
    """
    Verifies if any agent Me won the round

    :param mes: List of the Objects Me
    :param flag: Object Instance Flag
    :return: Sets up Me attribute won to True
    """
    for me in mes: 
        if me.alive and not me.won:
            if me_won(me, flag):
                me.won = True


# resi pohyb mes
def handle_mes_movement(mes: list[Me], mines: list[Mine], flag: Flag, senzor_length: int):
    """
    Function that handles the movement of Me agents

    :param mes: List of the Objects Me
    :param mines: List of the Objects Mine
    :param flag: Objects Instance Flag
    :param senzor_length: Length of the sensor to which agents can see
    :return: Uses function nn_navigate_me for each agent Me
    """
    for me in mes:
        if me.alive and not me.won:
            # <----- ZDE LOGIKA sbírání vstupů ze senzorů !!!
            # naplnit vstup in vstupy ze senzorů
            inp = []
            
            for x in my_senzor(me, flag, mines, senzor_length):
                inp.append(x)

            nn_navigate_me(me, inp)


# updatuje timery jedinců
def update_mes_timers(mes: list[Me], timer: int):
    """
    Updates attribute alivetime for each agent Me

    :param mes: List of the Objects Me
    :param timer: Alive time
    :return: Updates the alivetime attribute
    """
    for me in mes:
        if me.alive and not me.won:
            me.timealive = timer


# ---------------------------------------------------------------------------
# fitness funkce výpočty jednotlivců
#----------------------------------------------------------------------------


# funkce pro výpočet fitness všech jedinců
def handle_mes_fitnesses(mes: list[Me], flag: Flag):
    """
    Function to calculate the fitness of each agent Me

    :param mes: List of the Objects Me
    :param flag: Object Instance Flag
    :return: Sets up the attribute fitness of each agent Me
    """
    # na základě informací v nich uložených, či jiných vstupů
    for me in mes:
        my_number_pos = me.rect.x + me.rect.y
        flag_num_pos = flag.rect.x + flag.rect.y
        #print("Fitness:", flag_num_pos - my_number_pos)
        me.fitness = flag_num_pos - my_number_pos
        # me.timealive + (flag_num_pos - my_number_pos)


# uloží do hof jedince s nejlepší fitness
def update_hof(hof: Hof, mes: list[Me]):
    """
    Function that copies the best agent Me into the Hall of Fame

    :param hof: Object Instance Hof
    :param mes: List of the Objects Me
    :return: Saves the best agent Me into HoF
    """
    l = [me.fitness for me in mes]
    ind = np.argmax(l)
    hof.sequence = mes[ind].sequence.copy()
    

# ----------------------------------------------------------------------------
# main loop 
# ----------------------------------------------------------------------------

def main():
    # =====================================================================
    # <----- ZDE Parametry nastavení evoluce !!!!!
    VELIKOST_POPULACE = 10
    EVO_STEPS = 5        # pocet kroku evoluce
    DELKA_JEDINCE = 8    # <--------- záleží na počtu vah a prahů u neuronů !!!!!
    NGEN = 10            # počet generací
    CXPB = 0.6           # pravděpodobnost crossoveru na páru
    MUTPB = 0.2          # pravděpodobnost mutace+
    DELKA_SENZORU = 100  # vzdálenost, kterou prohledává senzor

    SIMSTEPS = 1000

    creator.create("FitnessMax", base.Fitness, weights=(-1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)
    
    toolbox = base.Toolbox()

    toolbox.register("attr_rand", random.random)
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_rand, DELKA_JEDINCE)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    # vlastni random mutace
    # <----- ZDE vlastní mutace
    def mutRandom(individual, indpb):
        for i in range(len(individual)):
            if random.random() < indpb:
                individual[i] = random.random()
        return individual,

    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", mutRandom, indpb=0.05)
    toolbox.register("select", tools.selRoulette)
    toolbox.register("selectbest", tools.selBest)
    
    pop = toolbox.population(n=VELIKOST_POPULACE)
        
    # =====================================================================
    
    clock = pygame.time.Clock()

    # =====================================================================
    # testování hraním a z toho odvození fitness
    mines = []
    mes = set_mes(VELIKOST_POPULACE)    
    flag = Flag()
    
    hof = Hof()
    print("Hall of Fame:", hof)

    run = True

    level = 1   # <--- ZDE nastavení obtížnosti počtu min !!!!!
    generation = 0
    
    evolving = True
    evolving2 = False
    timer = 0
    
    while run:  
        
        clock.tick(FPS)
        
               
        # pokud evolvujeme pripravime na dalsi sadu testovani - zrestartujeme scenu
        if evolving:           
            timer = 0
            generation += 1
            reset_mes(mes, pop) # přiřadí sekvence z populace jedincům a dá je na start !!!!
            mines = set_mines(level) 
            evolving = False
            
        timer += 1    
            
        check_mes_won(mes, flag)
        handle_mes_movement(mes, mines, flag, DELKA_SENZORU)

        handle_mines_movement(mines)
        
        mes_collision(mes, mines)
        
        if all_dead(mes):
            evolving = True
            #draw_text("Boom !!!")"""
            
        update_mes_timers(mes, timer)        
        draw_window(mes, mines, flag, level, generation, timer)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        # ---------------------------------------------------------------------
        # <---- Druhá část evoluce po simulaci  !!!!!
        
        # druhá část evoluce po simulaci, když všichni dohrají, simulace končí 1000 krocích

        if timer >= SIMSTEPS or nobodys_playing(mes): 
            
            # přepočítání fitness funkcí, dle dat uložených v jedinci
            handle_mes_fitnesses(mes, flag)   # <--------- funkce výpočtu fitness !!!!
            
            update_hof(hof, mes)
            
            
            #plot fitnes funkcí
            ff = [me.fitness for me in mes]

            #print(ff)
            
            # přiřazení fitnessů z jedinců do populace
            # každý me si drží svou fitness, a každý me odpovídá jednomu jedinci v populaci
            for i in range(len(pop)):
                ind = pop[i]
                me = mes[i]
                ind.fitness.values = (me.fitness, )
            
            # selekce a genetické operace
            offspring = toolbox.selectbest(pop, len(pop))
            offspring = list(map(toolbox.clone, offspring))

            for child1, child2 in zip(offspring[::2], offspring[1::2]):
                if random.random() < CXPB:
                    toolbox.mate(child1, child2)

            for mutant in offspring:
                if random.random() < MUTPB:
                    toolbox.mutate(mutant)  
            
            pop[:] = offspring
            evolving = True

        if generation == NGEN:
            level += 1
            generation = 0
            reset_mes(mes, pop)  # přiřadí sekvence z populace jedincům a dá je na start !!!!
            mines = set_mines(level)
            timer = 0

            # po vyskočení z cyklu aplikace vytiskne DNA sekvecni jedince s nejlepší fitness
    # a ukončí se
    
    pygame.quit()    


if __name__ == "__main__":
    main()