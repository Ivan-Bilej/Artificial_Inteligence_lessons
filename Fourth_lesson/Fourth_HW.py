import numpy as np
import random as rnd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from deap import base, creator, tools, algorithms


def plot_terrain(t):
    fig, ax = plt.subplots()

    x = range(len(t))
    sea = [0.5 for i in range(len(t))]

    print(t)
    ax.fill_between(x, sea, color="turquoise")
    ax.fill_between(x, t, color="sandybrown")
    ax.axis("off")
    plt.draw()


def plot_statistics(mean, maximum):
    fig, ax = plt.subplots()

    ax.plot(range(max_generations + 1), mean, label="mean")  # 0.tá generace zvlášť
    ax.plot(range(max_generations + 1), maximum, label="max")

    ax.legend()
    plt.draw()


def count_lakes_and_peaks_and_underwater(terrain: list):
    lake_start = False
    peak_start = False
    lake_count = 0
    peak_count = 0
    underwater_count = 0

    for point in terrain:
        if point < 0.5:
            underwater_count += 1
            if not lake_start:
                lake_start = True
                if peak_start:
                    peak_count += 1
                    peak_start = False

        else:
            if not peak_start:
                peak_start = True
                if lake_start:
                    lake_count += 1
                    lake_start = False

    if lake_start:
        lake_count += 1
    if peak_start:
        peak_count += 1

    return lake_count, peak_count, underwater_count


def evaluate(individual):
    lakes, peaks, underwater_count = count_lakes_and_peaks_and_underwater(individual)
    variability = max(individual) - min(individual)
    underwater_percentage = underwater_count / len(individual)

    fitness = abs(number_of_lakes - lakes) + \
              abs(number_of_peaks - peaks) + \
              abs(terrain_variability - variability) + \
              abs(underwater_perc - underwater_percentage) + \
              abs(lake_size - underwater_count) + \
              abs(lake_depth - min(individual))

    print(1 / fitness + 0.01)
    return (fitness,)


def create_toolbox():
    def custom_attr_float():
        return round(rnd.uniform(0, 1), 1)

    # Sets the fitness weight
    creator.create("FitnessMax", base.Fitness, weights=fitness_weights)
    # Creates an object named Individual that holds list of data about itself
    creator.create("Individual", list, fitness=creator.FitnessMax)

    toolbox = base.Toolbox()
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
    # Registers mutation of the individual with thw lowest and highest possible value % of the mutation
    toolbox.register("mutate", tools.mutPolynomialBounded, eta=1.0, low=0, up=1, indpb=0.05)
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
    print(pop)
    plot_terrain(pop[0])
    finalpop, logbook = algorithms.eaSimple(pop, toolbox,
                                            cxpb=crossover_percent,
                                            mutpb=mutation_percent,
                                            ngen=max_generations,
                                            stats=stats,
                                            halloffame=hof)
    print(finalpop)
    print(logbook)
    print(hof)

    mean, maximum = logbook.select("mean", "max")
    # Ukázka druhé populace

    plot_terrain(finalpop[len(finalpop) - 1])
    plot_statistics(mean, maximum)

    plt.show()


if __name__ == "__main__":
    test_data = [1.0, 0.2, 0.5, 0.6, 0.2, 0.7, 0.8, 0.5, 0.3, 0.5, 0.4, 0.5, 0.8]

    max_generations = 50
    max_data_length = 10
    crossover_percent = 0.5
    mutation_percent = 0.4
    identity_info = 5
    fitness_weights = (1.0,)

    # Criteria
    number_of_lakes = 2
    number_of_peaks = 5
    terrain_variability = 2
    underwater_perc = 0.3
    lake_size = 2
    lake_depth = 0.2
    # ... can be added more later on

    main()
