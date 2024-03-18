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

        s1, s2 = rozdej_skore(tah1, tah2)
        skore1 += s1
        skore2 += s2

        historie1.append(tah1)
        historie2.append(tah2)

    return skore1, skore2


def decide_turn_answer(my_history: list, other_player_history: list):
    if len(my_history) > 0 and len(other_player_history) > 0:
        if other_player_history[len(other_player_history)-1] == 0:
            return 0
        else:
            return 1
    else:
        return 0


def create_toolbox():
    # Sets the fitness weight
    creator.create("FitnessMin", base.Fitness, weights=fitness_weights)
    # Creates an object named Individual that holds list of data about itself
    creator.create("Individual", list, fitness=creator.FitnessMin)

    toolbox = base.Toolbox()
    toolbox.register("attr", 0)
    toolbox.register("individual", tools.initRepeat, creator.Individual,
                     toolbox.attr, n=max_data_length)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("game", play, toolbox.individual, toolbox.individual, max_game_steps)

    """
    # Generate a random number from 0 to 1
    toolbox.register("attr_float", custom_attr_float)
    # Create an individual containing those numbers. Maximum amount of number mentioned by n
    toolbox.register("individual", tools.initRepeat, creator.Individual,
                     toolbox.attr_float, n=max_data_length)
    # Creates a population from Individuals
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    # Register function evaluate into toolbox
    toolbox.register("evaluate", evaluate)
    # Register crossover (mating) of 2 individuals
    toolbox.register("mate", tools.cxOnePoint)
    # Registers mutation of the individual with thw lowest and highest possible value and % of the mutation
    toolbox.register("mutate", tools.mutPolynomialBounded, eta=0.8, low=0, up=1, indpb=0.005)
    # Select up to tournsize amount of Individuals via tournament
    toolbox.register("select", tools.selTournament, tournsize=3)
    """


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

    mean, maximum = logbook.select("mean", "max")
    plot_statistics(mean, maximum)
    plt.show()


if __name__ == "__main__":
    max_generations = 500
    max_game_steps = 10
    max_data_length = 10
    crossover_percent = 0.5
    mutation_percent = 0.4
    fitness_weights = (-1.0,)

    main()
