import numpy as np
import matplotlib.pyplot as plt
import math
import random as rnd
from collections import deque
import statistics as stat


def agent_unhappy(total_count: int, alike_count: int, tolerance: float):
    return True if np.round(alike_count / total_count, 1) < tolerance else False


def get_agent_surroundings(rep: list, row: int, col: int):
    agent = rep[row, col]
    total_agent_count = 0
    alike_agent_count = 0

    min_row = row - 1
    min_col = col - 1
    max_row = row + 1 if row + 1 <= len(rep) else 0
    max_col = col + 1 if col + 1 <= len(rep[row]) else 0

    for surr_row in range(min_row, max_row):
        for surr_col in range(min_col, max_col):
            if rep[surr_row, surr_col] == agent and surr_row != row and surr_col != col:
                alike_agent_count += 1
            total_agent_count += 1

    return alike_agent_count, total_agent_count


def find_free_space_and_unhappy_agents(rep: list):
    agents_to_move = []
    free_spaces = []

    for row, col in np.ndindex(rep.shape):
        agent = rep[row, col]
        if agent in agent1_list or agent in agent2_list:
            alike_count, total_count = get_agent_surroundings(rep, row, col)
            tolerance = agent1_tolerance if agent in agent1_list else agent2_tolerance

            if agent_unhappy(total_count, alike_count, tolerance):
                agents_to_move.append([row, col])

        else:
            free_spaces.append([row, col])

    print("Agents to move positions:", agents_to_move, "\nFree spaces position:", free_spaces)
    return agents_to_move, free_spaces


def step(rep: list):
    agents_to_move, free_spaces = find_free_space_and_unhappy_agents(rep)

    print(agents_to_move[0])
    move_ind = rng.choice(len(agents_to_move), 1, replace=False)[0]
    free_ind = rng.choice(len(free_spaces), 1, replace=False)[0]

    print("Before:\n", rep)
    print("Agent position:", move_ind, agents_to_move[move_ind])
    print("Free space position:", free_ind, free_spaces[free_ind])
    rep[free_ind] = rep[move_ind]
    #rep[agent_to_move] = 0

    print("After:\n", rep)


def plot(rep: list):
    pass


if __name__ == "__main__":
    start_torus = []
    max_rows = 3
    max_columns = 4
    agent1_list = [1]
    agent1_tolerance = 0.4
    agent2_list = [2]
    agent2_tolerance = 1.6

    rng = np.random.default_rng(123456)
    fig = plt.figure()
    fig, plot_ax = plt.subplots()
    plot_ax.set_aspect("equal")

    for i in range(max_rows):
        row_line = rng.integers(0, 3, max_columns)
        start_torus.append(row_line)
    start_torus = [[0, 1, 2, 0],
                   [1, 1, 2, 2],
                   [0, 0, 0, 0]]
    numpy_torus = np.array(start_torus, dtype=int)


    print(numpy_torus)
    print(type(numpy_torus))
    print(numpy_torus.ndim)
    print(numpy_torus.shape[0])
    print(numpy_torus.size)
    step(numpy_torus)


    """
    plot_ax.scatter(10, 10, s=50,
                    fc="blue", ec="k")

    x = np.linspace(0, 2 * np.pi)
    fx = np.sin(x)
    plt.plot(x, fx)
    """



