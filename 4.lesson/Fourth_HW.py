import numpy as np
import random as rnd
import matplotlib.pyplot as plt
from deap import base, creator, tools, algorithms


def plot_terrain(t):
    """
    Plots a given terrain profile.

    The terrain is represented as a list of elevations, with the sea level fixed at 0.5. The function plots the terrain
    above and below sea level using different colors.

    :param t: A list of elevation values for the terrain.
    """
    fig, ax = plt.subplots()
    x = range(len(t))
    sea = [0.5 for _ in range(len(t))]

    ax.fill_between(x, sea, color="turquoise", label='Sea')
    ax.fill_between(x, t, color="sandybrown", label='Land')
    ax.axis("off")

    plt.draw()


def plot_statistics(mean, maximum):
    """
    Plots the mean and maximum fitness over generations.

    :param mean: A list of mean fitness values per generation.
    :param maximum: A list of maximum fitness values per generation.
    """
    fig, ax = plt.subplots()

    ax.plot(range(max_generations + 1), mean, label="Mean Fitness")
    ax.plot(range(max_generations + 1), maximum, label="Max Fitness")

    ax.legend()
    plt.draw()


def count_lakes_and_peaks_and_underwater(terrain: list):
    """
    Counts the number of lakes, peaks, and underwater points in a terrain profile.

    :param terrain: A list representing the terrain profile.
    :return: A tuple containing the counts of lakes, peaks, and underwater points.
    """
    lake_start = False
    peak_start = False
    lake_count = 0
    peak_count = 0
    underwater_count = 0

    for point in terrain:
        if point < 0.5:  # Below sea level
            underwater_count += 1
            if not lake_start:
                lake_start = True
                if peak_start:
                    peak_count += 1
                    peak_start = False

        else:  # Above sea level
            if not peak_start:
                peak_start = True
                if lake_start:
                    lake_count += 1
                    lake_start = False

    # Closing open lakes/peaks at the end of the terrain
    lake_count += lake_start
    peak_count += peak_start

    return lake_count, peak_count, underwater_count


def evaluate(individual):
    """
    Evaluates the fitness of a terrain profile based on specified criteria.

    :param individual: A list representing a terrain profile.
    :return: A tuple containing the inverse of the fitness score; higher is better.
    """
    lakes, peaks, underwater_count = count_lakes_and_peaks_and_underwater(individual)
    variability = round(max(individual) - min(individual), 3)
    underwater_percentage = underwater_count / len(individual)

    # Commented code can be deleted or uncommented for further testing
    fitness = abs(number_of_lakes - lakes) + \
              abs(number_of_peaks - peaks) + \
              abs(terrain_variability - variability)
              # abs(underwater_perc - underwater_percentage) + \
              # abs(lake_size - underwater_count) + \
              # abs(lake_depth - min(individual))
              # ... can be added more

    print("Hodnoty:")
    print(lakes, peaks, variability, underwater_percentage, underwater_count, min(individual), fitness)

    adjusted_fitness = 1 / (fitness + 0.0001) # Avoid division by zero
    return (adjusted_fitness,)


def create_toolbox():
    """
    Creates and configures a DEAP toolbox with genetic algorithm operations.

    :return: Configured DEAP toolbox.
    """
    def custom_attr_float():
        float_num = rnd.uniform(0.0, 1.0)
        float_num = round(float_num, 3)
        return float_num

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
    # Registers mutation of the individual with thw lowest and highest possible value and % of the mutation
    toolbox.register("mutate", tools.mutPolynomialBounded, eta=0.8, low=0, up=1, indpb=0.005)
    # Select up to tournsize amount of Individuals via tournament
    toolbox.register("select", tools.selTournament, tournsize=3)

    return toolbox


def set_up_statistics():
    """
    Sets up DEAP statistics to be tracked over generations.

    :return: Configured DEAP statistics object.
    """
    stats = tools.Statistics(key=lambda ind: ind.fitness.values)
    stats.register("mean", np.mean)
    stats.register("max", np.max)

    return stats


def main():
    """
    Main function to execute the genetic algorithm for terrain generation optimization.
    """
    toolbox = create_toolbox()
    stats = set_up_statistics()
    hof = tools.HallOfFame(1)

    pop = toolbox.population(n=20)
    plot_terrain(pop[0])
    finalpop, logbook = algorithms.eaSimple(pop, toolbox,
                                            cxpb=crossover_percent,
                                            mutpb=mutation_percent,
                                            ngen=max_generations,
                                            stats=stats,
                                            halloffame=hof)

    mean, maximum = logbook.select("mean", "max")

    plot_terrain(finalpop[len(finalpop) - 1])
    plot_statistics(mean, maximum)

    plt.show()


if __name__ == "__main__":
    test_data = [1.0, 0.2, 0.5, 0.6, 0.2, 0.7, 0.8, 0.5, 0.3, 0.5, 0.4, 0.5, 0.8]

    max_generations = 500
    max_data_length = 30
    crossover_percent = 0.5
    mutation_percent = 0.6
    fitness_weights = (1.0,)

    # Criteria
    number_of_lakes = 3
    number_of_peaks = 5
    terrain_variability = 0.2
    underwater_perc = 0.0
    lake_size = 0
    lake_depth = 0.4
    # ... can be added more

    main()
