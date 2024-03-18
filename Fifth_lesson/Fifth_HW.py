import numpy as np
import random as rnd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from deap import base, creator, tools, algorithms


def plot_statistics(mean, maximum):
    fig, ax = plt.subplots()

    ax.plot(range(max_generations + 1), mean, label="mean")  # 0.tá generace zvlášť
    ax.plot(range(max_generations + 1), maximum, label="max")

    ax.legend()
    plt.draw()


def rozdej_skore(tah1, tah2):
    # 1 = zradi, 0 = nezradi

    skores = (0, 0)

    if (tah1 == 1) and (tah2 == 1):
        skores = (2, 2)

    if (tah1 == 1) and (tah2 == 0):
        skores = (0, 3)

    if (tah1 == 0) and (tah2 == 1):
        skores = (3, 0)

    if (tah1 == 0) and (tah2 == 0):
        skores = (1, 1)

    return skores


def play(f1, f2, stepsnum):
    skore1 = 0
    skore2 = 0

    historie1 = []
    historie2 = []

    for i in range(stepsnum):
        tah1 = f1(historie1, historie2)
        tah2 = f2(historie2, historie1)
        #print("Tah hráče 1:", tah1)
        #print("Tah hráče 2:", tah2)

        s1, s2 = rozdej_skore(tah1, tah2)
        skore1 += s1
        skore2 += s2

        historie1.append(tah1)
        historie2.append(tah2)

    return skore1, skore2


def individual_strategy(individual):
    #print(individual)

    def strategy(my_history: list, opponent_history: list):
        betrayals = 0
        saves = 0

        if len(my_history) == 0:
            return individual[0]

        for turn in opponent_history[(len(opponent_history)-max_turn_search):]:
            if turn == 1:
                betrayals += 1
            else:
                saves += 1

        if betrayals == 2:
            return 1
        else:
            return individual[len(my_history) % len(individual)]

    return strategy


def evaluate(individual):
    random_opponent = [rnd.randint(0, 1) for _ in range(max_game_steps)]
    opponent_strategy = individual_strategy(random_opponent)
    my_strategy = individual_strategy(individual)
    score, _ = play(my_strategy, opponent_strategy, max_game_steps)
    return (score,)


def create_toolbox():
    # Sets the fitness weight
    creator.create("FitnessMin", base.Fitness, weights=fitness_weights)
    # Creates an object named Individual that holds list of data about itself
    creator.create("Individual", list, fitness=creator.FitnessMin)

    toolbox = base.Toolbox()
    toolbox.register("attr", rnd.randint, 0, 1)
    toolbox.register("individual", tools.initRepeat, creator.Individual,
                     toolbox.attr, n=max_game_steps)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("evaluate", evaluate)

    # Register crossover (mating) of 2 individuals
    toolbox.register("mate", tools.cxOnePoint)
    # Registers mutation of the individual with thw lowest and highest possible value and % of the mutation
    toolbox.register("mutate", tools.mutUniformInt, low=0, up=1, indpb=0.005)
    # Select up to tournsize amount of Individuals via tournament
    toolbox.register("select", tools.selTournament, tournsize=3)

    return toolbox


def set_up_statistics():
    stats = tools.Statistics(key=lambda ind: ind.fitness.values)
    stats.register("mean", np.mean)
    stats.register("max", np.max)

    return stats


def main():
    toolbox = create_toolbox()
    stats = set_up_statistics()
    hof = tools.HallOfFame(1)

    pop = toolbox.population(n=20)
    finalpop, logbook = algorithms.eaSimple(pop, toolbox,
                                            cxpb=crossover_percent,
                                            mutpb=mutation_percent,
                                            ngen=max_generations,
                                            stats=stats,
                                            halloffame=hof)

    print(finalpop[-1])
    mean, maximum = logbook.select("mean", "max")
    plot_statistics(mean, maximum)
    plt.show()


if __name__ == "__main__":
    max_generations = 500
    max_game_steps = 5
    max_turn_search = 1
    crossover_percent = 0.5
    mutation_percent = 0.4
    fitness_weights = (-1.0,)

    main()
