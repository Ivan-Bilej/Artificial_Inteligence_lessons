import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import random as rnd


def create_map(max_rows: int, max_cols: int):
    d_map = []
    # agent_count = 0

    for i in range(max_rows):
        row_line = rng.integers(0, 3, max_cols)
        """
        for agent in row_line:
            if agent != 0:
                agent_count += 1
        """
        d_map.append(row_line)

    return d_map


def agent_unhappy(total_count: int, alike_count: int, free_count: int, tolerance: float):
    if alike_count == 0 or total_count == 0:
        return True
    else:
        return True if alike_count / total_count < tolerance else False


def get_agent_surroundings(rep: list, row: int, col: int):
    agent = rep[row, col]
    total_agent_count = 0
    alike_agent_count = 0
    free_count = 0

    min_row = row - 1
    min_col = col - 1
    max_row = row + 2 if row + 1 < len(rep) else 1
    max_col = col + 2 if col + 1 < len(rep[row]) else 1

    for surr_row in range(min_row, max_row):
        for surr_col in range(min_col, max_col):
            if rep[surr_row, surr_col] == agent and (surr_row != row or surr_col != col):
                alike_agent_count += 1
            if (rep[surr_row, surr_col] in agent1_list or rep[surr_row, surr_col] in agent2_list) and \
                    (surr_row != row or surr_col != col):
                total_agent_count += 1
            elif rep[surr_row, surr_col] == 0:
                free_count += 1

    return alike_agent_count, total_agent_count, free_count


def find_free_space_and_unhappy_agents(rep: list):
    agents_to_move = []
    free_spaces = []

    for row, col in np.ndindex(rep.shape):
        agent = rep[row, col]
        if agent in agent1_list or agent in agent2_list:
            alike_count, total_count, free_count = get_agent_surroundings(rep, row, col)
            tolerance = agent1_tolerance if agent in agent1_list else agent2_tolerance

            if agent_unhappy(total_count, alike_count, free_count, tolerance):
                agents_to_move.append([row, col])

        else:
            free_spaces.append([row, col])

    return agents_to_move, free_spaces


def step(rep: list, agents_to_move: list, free_spaces: list):
    #agents_to_move, free_spaces = find_free_space_and_unhappy_agents(rep)

    move_ind = rnd.choice(agents_to_move)
    free_ind = rnd.choice(free_spaces)

    rep[free_ind[0], free_ind[1]] = rep[move_ind[0], move_ind[1]]
    rep[move_ind[0], move_ind[1]] = 0


def plot(rep, plot_ax):
    plot_ax.clear()
    plot_ax.imshow(rep, cmap=custom_plot_colors, interpolation="nearest")
    plot_ax.set_aspect("equal")
    plt.draw()
    plt.pause(0.02)

def plot_unhappy(unhappy_count, iter_count, plot_ax2):
    plot_ax2.clear()
    plot_ax2.plot(iter_count, unhappy_count, marker="o", ls="-")
    plot_ax2.set_xlabel("Iteration")
    plot_ax2.set_ylabel("Number of Unhappy Agents")
    plot_ax2.grid(True)
    plt.draw()
    plt.pause(0.02)


def main():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    start_torus = create_map(max_rows, max_columns)
    numpy_torus = np.array(start_torus, dtype=int)

    unhappy_agents, free_spaces = find_free_space_and_unhappy_agents(numpy_torus)
    unhappy_count = [len(unhappy_agents)]
    iter_count = [0]

    while len(unhappy_agents) != 0:
        step(numpy_torus, unhappy_agents, free_spaces)
        plot(numpy_torus, ax1)
        plot_unhappy(unhappy_count, iter_count, ax2)

        unhappy_agents, free_spaces = find_free_space_and_unhappy_agents(numpy_torus)
        unhappy_count.append(len(unhappy_agents))
        iter_count.append(iter_count[-1] + 1)
        #print("Unhappy", unhappy_agents)
        #print("next step")

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    max_rows, max_columns = 50, 50
    agent1_list = [1]
    agent1_tolerance = 0.2
    agent2_list = [2]
    agent2_tolerance = 0.2

    rng = np.random.default_rng(123456)
    # Barvy podle hodnoty počínaje 0, tedy:
    # 0 -> white
    # 1 -> black
    # 2 -> red
    custom_plot_colors = ListedColormap(["white", "black", "red"])

    main()

