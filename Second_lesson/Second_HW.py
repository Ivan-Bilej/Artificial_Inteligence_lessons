import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import random as rnd


def create_map(max_rows: int, max_cols: int):
    d_map = []

    for i in range(max_rows):
        row_line = rng.integers(0, 3, max_cols)
        d_map.append(row_line)

    return d_map


def agent_unhappy(total_count: int, alike_count: int, tolerance: float):

    if alike_count == 0 or total_count == 0:
        return True
    else:
        return True if alike_count / total_count <= tolerance else False


def get_agent_surroundings(rep: list, row: int, col: int):
    agent = rep[row, col]
    total_agent_count = 0
    alike_agent_count = 0

    min_row = row - 1
    min_col = col - 1
    max_row = row + 2 if row + 2 <= len(rep) else 1
    max_col = col + 2 if col + 2 <= len(rep[row]) else 1

    for surr_row in range(min_row, max_row):
        for surr_col in range(min_col, max_col):
            if rep[surr_row, surr_col] == agent and (surr_row != row or surr_col != col):
                alike_agent_count += 1
            if (rep[surr_row, surr_col] in agent1_list or rep[surr_row, surr_col] in agent2_list) and \
                    (surr_row != row or surr_col != col):
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

    return agents_to_move, free_spaces


def step(rep: list):
    agents_to_move, free_spaces = find_free_space_and_unhappy_agents(rep)

    move_ind = rnd.choice(agents_to_move)
    free_ind = rnd.choice(free_spaces)
    # move_ind = rng.choice(len(agents_to_move), 1, replace=False)[0]
    # free_ind = rng.choice(len(free_spaces), 1, replace=False)[0]

    # print("Before:\n", rep)
    # print("Agent position:", move_ind)
    # print("Free space position:", free_ind)
    rep[free_ind[0], free_ind[1]] = rep[move_ind[0], move_ind[1]]
    rep[move_ind[0], move_ind[1]] = 0

    # print("After:\n", rep)



def plot(rep: list, plot_ax):
    plot_ax.clear()
    plot_ax.imshow(rep, cmap=custom_plot_colors, interpolation="nearest")
    plot_ax.set_aspect("equal")
    plt.draw()
    plt.pause(0.005)


def main():
    start_torus = create_map(max_rows, max_columns)
    numpy_torus = np.array(start_torus, dtype=int)

    unhappy_agents, free_spaces = find_free_space_and_unhappy_agents(numpy_torus)
    while len(unhappy_agents) != 0:
        step(numpy_torus)
        plot(numpy_torus, plot_ax)
        unhappy_agents, free_spaces = find_free_space_and_unhappy_agents(numpy_torus)

    plt.show()


if __name__ == "__main__":
    max_rows = 50
    max_columns = 50
    max_steps = 10
    agent1_list = [1]
    agent1_tolerance = 0.4
    agent2_list = [2]
    agent2_tolerance = 0.4

    rng = np.random.default_rng(123456)
    fig = plt.figure()
    fig, plot_ax = plt.subplots()
    custom_plot_colors = ListedColormap(["white", "green", "orange"])

    main()

