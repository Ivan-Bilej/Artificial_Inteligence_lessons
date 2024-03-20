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

    #print(f1.__name__, ":", skore1, f2.__name__, ":", skore2)
    return skore1, skore2


def primitive_strategy(my_history: list, opponent_history: list):
    if len(my_history) == 0:
        return 0

    if opponent_history[-1] == 1:
        return 1
    else:
        return 0


def always_betray(my_history: list, opponent_history: list):
    return 1


def always_cooperate(my_history: list, opponent_history: list):
    return 0


def random_strategy(my_history: list, opponent_history: list):
    return rnd.randint(0, 1)


def individual_strategy(individual: list):
    def betray(my_history: list, opponent_history: list):
        betrayal = 0
        cooperate = 0

        if not my_history:
            return individual[0]

        for x in opponent_history[(len(opponent_history) - 2):]:
            if x == 1:
                betrayal += 1
            else:
                cooperate += 1

        if betrayal == 1 and cooperate == 0:
            return individual[1]
        elif betrayal == 2 and cooperate == 0:
            return individual[2]
        elif betrayal == 0 and cooperate == 1:
            return individual[3]
        elif betrayal == 1 and cooperate == 1:
            return individual[4]
        elif betrayal == 2 and cooperate == 1:
            return individual[5]
        elif betrayal == 0 and cooperate == 2:
            return individual[6]
        elif betrayal == 1 and cooperate == 2:
            return individual[7]
        elif betrayal == 2 and cooperate == 2:
            return individual[8]
        else:
            return individual[9]

    return betray


def evaluate(individual):
    my_strategy = individual_strategy(individual)
    strategies = [always_betray, always_cooperate, random_strategy, primitive_strategy, my_strategy] * 5
    scores = []

    for strategy in strategies:
        score1, _ = play(my_strategy, strategy, max_game_steps)
        scores.append(score1)

    return (sum(scores),)


def create_toolbox():
    # Sets the fitness weight
    creator.create("FitnessMin", base.Fitness, weights=fitness_weights)
    # Creates an object named Individual that holds list of data about itself
    creator.create("Individual", list, fitness=creator.FitnessMin)

    toolbox = base.Toolbox()
    toolbox.register("attr", rnd.randint, 0, 1)
    toolbox.register("individual", tools.initRepeat, creator.Individual,
                     toolbox.attr, n=individual_max_strats)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("evaluate", evaluate)

    # Register crossover (mating) of 2 individuals
    toolbox.register("mate", tools.cxOnePoint)
    # Registers mutation of the individual with thw lowest and highest possible value and % of the mutation
    toolbox.register("mutate", tools.mutUniformInt, low=0, up=1, indpb=0.05)
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

    pop = toolbox.population(n=population_max)
    finalpop, logbook = algorithms.eaSimple(pop, toolbox,
                                            cxpb=crossover_percent,
                                            mutpb=mutation_percent,
                                            ngen=max_generations,
                                            stats=stats,
                                            halloffame=hof)

    print(hof[0])
    mean, maximum = logbook.select("mean", "max")
    plot_statistics(mean, maximum)
    plt.show()


if __name__ == "__main__":
    max_generations = 50000
    individual_max_strats = 10
    population_max = 20
    fitness_weights = (-1.0,)

    # best_500 [1, 0, 1, 1, 0, 0, 1, 0, 0, 1]
    # best 1000 [0, 1, 1, 1, 0, 0, 1, 1, 1, 0]
    # best 1500 [0, 1, 1, 0, 0, 0, 1, 0, 1, 1]

    max_game_steps = 15
    max_turn_search = 2

    crossover_percent = 0.5
    mutation_percent = 0.4


    main()
