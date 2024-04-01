import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import random as rnd


def create_map(max_rows: int, max_cols: int):
    """
    Creates a map of agents where each cell represents an agent or empty space.

    Each cell is initialized with a random value that represents different types of agents or an empty space.
    - 0: Empty space
    - 1: Agent type 1
    - 2: Agent type 2

    :param max_rows: Number of rows in the map.
    :param max_cols: Number of columns in the map.
    :return: A 2D list representing the initial state of the map with agents and empty spaces.
    """
    d_map = []
    for i in range(max_rows):
        # Generate a random row of agents and empty spaces
        row_line = rng.integers(0, 3, max_cols)
        d_map.append(row_line)

    return d_map


def agent_unhappy(total_count: int, alike_count: int, tolerance: float):
    """
    Determines if an agent is unhappy based on the surrounding agents.

    An agent is considered unhappy if the proportion of neighboring agents that are of the same type is less than
    a specified tolerance threshold.

    :param total_count: Total number of neighboring agents (excluding empty spaces).
    :param alike_count: Number of neighboring agents of the same type.
    :param free_count: Number of neighboring empty spaces (unused in this function).
    :param tolerance: The tolerance threshold for an agent to be considered happy.
    :return: True if the agent is unhappy, False otherwise.
    """
    if alike_count == 0 or total_count == 0:
        return True
    else:
        return alike_count / total_count < tolerance


def get_agent_surroundings(rep: list, row: int, col: int):
    """
    Calculates the count of alike, total, and free surrounding agents for a given agent.

    :param rep: The map representation as a numpy array.
    :param row: The row index of the agent.
    :param col: The column index of the agent.
    :return: A tuple containing counts of alike agents, total neighboring agents, and free spaces.
    """
    agent = rep[row, col]
    total_agent_count = 0
    alike_agent_count = 0
    free_count = 0

    # Define the search area, ensuring it does not go out of bounds
    min_row, max_row = max(0, row - 1), min(rep.shape[0], row + 2)
    min_col, max_col = max(0, col - 1), min(rep.shape[1], col + 2)

    for surr_row in range(min_row, max_row):
        for surr_col in range(min_col, max_col):
            if surr_row == row and surr_col == col:
                continue  # Skip the agent itself
            if rep[surr_row, surr_col] == agent:
                alike_agent_count += 1
            if rep[surr_row, surr_col] > 0:
                total_agent_count += 1
            elif rep[surr_row, surr_col] == 0:
                free_count += 1

    return alike_agent_count, total_agent_count, free_count


def find_free_space_and_unhappy_agents(rep: list):
    """
    Identifies all unhappy agents and available free spaces in the map.

    :param rep: The map representation as a numpy array.
    :return: A tuple containing lists of unhappy agents and free spaces.
    """
    agents_to_move = []
    free_spaces = []

    for row, col in np.ndindex(rep.shape):
        agent = rep[row, col]
        if agent > 0:  # If the cell is not empty
            alike_count, total_count, free_count = get_agent_surroundings(rep, row, col)
            tolerance = agent1_tolerance if agent in agent1_list else agent2_tolerance
            if agent_unhappy(total_count, alike_count, free_count, tolerance):
                agents_to_move.append((row, col))
        else:
            free_spaces.append((row, col))

    return agents_to_move, free_spaces


def step(rep: list, agents_to_move: list, free_spaces: list):
    """
    Moves an unhappy agent to a free space.

    :param rep: The map representation as a numpy array.
    :param agents_to_move: A list of coordinates for unhappy agents.
    :param free_spaces: A list of coordinates for free spaces.
    """
    if agents_to_move and free_spaces:
        move_ind = rnd.choice(agents_to_move)
        free_ind = rnd.choice(free_spaces)

        # Swap the unhappy agent with a free space
        rep[free_ind[0], free_ind[1]], rep[move_ind[0], move_ind[1]] = rep[move_ind[0], move_ind[1]], 0


def plot(rep, plot_ax):
    """
    Plots the current state of the map.

    :param rep: The map representation as a numpy array.
    :param plot_ax: The matplotlib axis on which to plot the map.
    """
    plot_ax.clear()
    plot_ax.imshow(rep, cmap=custom_plot_colors, interpolation="nearest")
    plot_ax.set_aspect("equal")
    plt.draw()
    plt.pause(0.02)  # Pause to update the plot


def plot_unhappy(unhappy_count, iter_count, plot_ax2):
    """
    Plots the number of unhappy agents over iterations.

    :param unhappy_count: A list of counts of unhappy agents.
    :param iter_count: A list of iteration numbers.
    :param plot_ax2: The matplotlib axis on which to plot the unhappiness graph.
    """
    plot_ax2.clear()
    plot_ax2.plot(iter_count, unhappy_count, marker="o", ls="-")
    plot_ax2.set_xlabel("Iteration")
    plot_ax2.set_ylabel("Number of Unhappy Agents")
    plot_ax2.grid(True)
    plt.draw()
    plt.pause(0.02)  # Pause to update the plot


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

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    max_rows, max_columns = 50, 50  # Grid size
    agent1_list = [1]  # Agent type 1
    agent1_tolerance = 0.2  # Tolerance threshold for agent type 1
    agent2_list = [2]  # Agent type 2
    agent2_tolerance = 0.2  # Tolerance threshold for agent type 2

    rng = np.random.default_rng(123456)  # Random number generator for reproducibility
    # Barvy podle hodnoty počínaje 0, tedy:
    # 0 -> white
    # 1 -> black
    # 2 -> red
    custom_plot_colors = ListedColormap(["white", "black", "red"]) # Map cell colors: empty, agent type 1, agent type 2

    main()

