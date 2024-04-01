import numpy as np
import random as rnd
import matplotlib.pyplot as plt
from deap import base, creator, tools, algorithms


def plot_statistics(mean, maximum):
    """
    Plots the evolution of mean and maximum fitness over generations.

    :param mean: A list containing the mean fitness of the population at each generation.
    :param maximum: A list containing the maximum fitness of the population at each generation.
    """
    fig, ax = plt.subplots()
    ax.plot(range(max_generations + 1), mean, label="Mean Fitness")
    ax.plot(range(max_generations + 1), maximum, label="Maximum Fitness")
    ax.legend()
    plt.draw()


def rozdej_skore(tah1, tah2):
    """
    Determines the score for a single round of the IPD based on the actions of two players.

    :param tah1: The action of player 1 (1 for betray, 0 for cooperate).
    :param tah2: The action of player 2 (1 for betray, 0 for cooperate).
    :return: A tuple of scores for player 1 and player 2.
    """
    # 1 = zradi, 0 = nezradi

    scores = (0, 0)

    if (tah1 == 1) and (tah2 == 1):
        scores = (2, 2)
    if (tah1 == 1) and (tah2 == 0):
        scores = (0, 3)
    if (tah1 == 0) and (tah2 == 1):
        scores = (3, 0)
    if (tah1 == 0) and (tah2 == 0):
        scores = (1, 1)

    return scores


def play(f1, f2, stepsnum):
    """
    Simulates a series of rounds between two strategies in the IPD.

    :param f1: A function representing the first player's strategy.
    :param f2: A function representing the second player's strategy.
    :param stepsnum: The number of rounds to be played.
    :return: The total scores of player 1 and player 2.
    """
    skore1, skore2 = 0, 0
    historie1, historie2 = [], []

    for i in range(stepsnum):
        tah1 = f1(historie1, historie2)
        tah2 = f2(historie2, historie1)

        s1, s2 = rozdej_skore(tah1, tah2)
        skore1 += s1
        skore2 += s2

        historie1.append(tah1)
        historie2.append(tah2)

    return skore1, skore2


# Example strategy
def primitive_strategy(my_history: list, opponent_history: list):
    if len(my_history) == 0:
        return 0

    if opponent_history[-1] == 1:
        return 1
    else:
        return 0


# Example strategy
def always_betray(my_history: list, opponent_history: list):
    return 1


# Example strategy
def always_cooperate(my_history: list, opponent_history: list):
    return 0


# Example strategy
def random_strategy(my_history: list, opponent_history: list):
    return rnd.randint(0, 1)


def individual_strategy(individual):
    """
    Wraps an individual's chromosome as a strategy for the IPD.

    :param individual: A list representing the individual's strategy.
    :return: A function that executes the strategy.
    """

    def betray(my_history: list, opponent_history: list):
        """
        Determines the next move in the Iterated Prisoner's Dilemma based on the opponent's recent history and a predefined strategy.

        This function assesses the opponent's last two moves to make a decision for the next round, using a strategy encoded within an individual's chromosome. The individual's chromosome consists of decisions (to betray or cooperate) that correspond to different scenarios based on the opponent's recent actions.

        Parameters:
        - my_history: List of integers representing the player's past actions (1 for betray, 0 for cooperate).
        - opponent_history: List of integers representing the opponent's past actions (1 for betray, 0 for cooperate).

        Returns:
        - An integer representing the player's next action based on the strategy (1 for betray, 0 for cooperate).

        The strategy uses the opponent's last two moves to decide:
        - If the opponent betrayed once or cooperated twice in their last two moves, the player's response is determined by specific elements of the individual's chromosome.
        - The decision is based on the count of betrayals and cooperations in the opponent's last two moves, mapping directly to elements in the individual's chromosome for a response.
        """
        betrayal = 0
        cooperate = 0

        # If it's the first move, return the first element of the individual's strategy.
        if not my_history:
            return individual[0]

        # Count the opponent's betrayals and cooperations in their last two moves.
        for x in opponent_history[(len(opponent_history) - 2):]:
            if x == 1:
                betrayal += 1
            else:
                cooperate += 1

        # Determine the next move based on the opponent's recent actions and the individual's strategy.
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
    """
    Evaluates the fitness of an individual's strategy against a set of opponent strategies.

    :param individual: The individual to evaluate.
    :return: The fitness of the individual.
    """
    my_strategy = individual_strategy(individual)
    strategies = [always_betray, always_cooperate, random_strategy, primitive_strategy, my_strategy] * 5
    # Can add or multiply any strategy for bigger tournament
    scores = []

    for strategy in strategies:
        score1, _ = play(my_strategy, strategy, max_game_steps)
        scores.append(score1)

    return (sum(scores),)


def create_toolbox():
    """
    Creates a DEAP toolbox with the necessary operations for running the genetic algorithm.

    :return: Configured toolbox.
    """
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
    """
    Sets up DEAP statistics to be tracked over generations.

    :return: Configured DEAP statistics object.
    """
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
