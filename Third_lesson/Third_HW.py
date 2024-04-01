import os
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import time


def read_dimacs(filename: str, file_path: str):
    """
    Reads a graph from a DIMACS formatted file.

    DIMACS is a standard format for specifying graphs, commonly used in graph theory and optimization.
    This function reads the file and creates a graph using networkx.

    :param filename: The name of the file containing the DIMACS graph.
    :param file_path: The path to the directory where the file is located.
    :return: A networkx graph object created from the DIMACS file.
    """
    file = open(os.path.join(file_path, filename), 'r')
    lines = file.readlines()

    Gd = nx.Graph()

    for line in lines:
        if line.startswith("e"):
            vs = [int(s) for s in line.split() if s.isdigit()]
            Gd.add_edge(vs[0] - 1, vs[1] - 1)  # Adjusts for zero-based indexing
    return Gd


def plot(graph: nx.Graph, cols: list):
    """
    Plots a graph with nodes colored according to the given coloring scheme.

    :param graph: The graph to be plotted.
    :param cols: A list of colors for the nodes, where each color is represented by an integer.
    """
    k = np.max(cols)  # Determine the number of colors used
    symbols = '0123456789ABCDEF'
    colmap = ["#" + ''.join(rng.choice(list(symbols), 6)) for i in range(k + 1)]

    colors = [colmap[c] for c in cols]  # Map coloring integers to hexadecimal color codes

    nx.draw(graph, node_color=colors, with_labels=True)


def get_biggest_amount_of_edges(graph: nx.Graph):
    """
    Finds the node with the highest degree (most edges) in the graph.

    :param graph: The graph to be analyzed.
    :return: The degree of the node with the highest degree.
    """
    highest_number = 0
    highest_edges_node = 0

    for node in graph:
        neighbour_count = len(list(graph.neighbors(node)))
        if neighbour_count > highest_number:
            highest_number = neighbour_count
            highest_edges_node = node

    print(f"Node with highest amount of edges: {highest_edges_node}")
    print(f"Highest amount of edges: {highest_number}")
    return highest_number


def local_coloring(graph: nx.Graph, local_node: int, col: list):
    """
    Evaluates if the coloring of a specific node is valid in the local neighborhood.

    :param graph: The graph to be evaluated.
    :param local_node: The node whose coloring is to be evaluated.
    :param col: The current coloring scheme as a list of color integers for each node.
    :return: A tuple of (boolean indicating if coloring is valid, count of conflicts).
    """
    bad_coloring_count = 0

    for neighbour in graph.neighbors(local_node):
        if col[local_node] == col[neighbour]:
            bad_coloring_count += 1

    return (False, bad_coloring_count) if bad_coloring_count > 0 else (True, 0)


def is_coloring(graph: nx.Graph, col: list):
    """
    Checks if the entire graph is validly colored.

    :param graph: The graph to be checked.
    :param col: The coloring scheme as a list of colors for each node.
    :return: True if the coloring is valid, False otherwise.
    """
    for local_node in graph:
        for neighbour in graph.neighbors(local_node):
            if col[local_node] == col[neighbour]:
                return False  # Found two adjacent nodes with the same color

    return True  # No conflicts found


def color(graph: nx.Graph, k: int, steps: int):
    """
    Attempts to color the graph using a local search strategy.

    :param graph: The graph to be colored.
    :param k: The number of colors available.
    :param steps: The maximum number of steps (iterations) to attempt.
    :return: The final coloring scheme and a boolean indicating if a valid coloring was found.
    """
    colors = list(range(k))
    color_list = [rng.choice(colors) for node in graph]

    print(f"Initial color list: {color_list}")
    # Initial plot is commented out; uncomment to visualize
    # draw_graph(graph, color_list)

    for step in range(steps):
        local_node = step % graph.number_of_nodes()
        solved, _ = local_coloring(graph, local_node, color_list)

        if not solved:
            # Try to find a better color for this node
            temp_color_list = color_list.copy()
            temp_color_list[local_node] = rng.choice(colors)
            if local_coloring(graph, local_node, temp_color_list)[0]:
                color_list = temp_color_list  # Update to the better coloring

        # Optional: Add a condition to exit early if a valid coloring is found
        if is_coloring(graph, color_list):
            break  # Found a valid coloring

    return color_list, is_coloring(graph, color_list)


def draw_graph(graph: nx.Graph, col_list: list):
    """
    Draws the graph with the given coloring, using a circular layout.

    :param graph: The graph to draw.
    :param col_list: The list of colors for each node.
    """
    nx.draw(graph, pos=nx.circular_layout(graph), node_color=col_list, with_labels=True)
    plt.draw()
    plt.pause(0.02)  # Pause briefly to allow the plot to update


def main():
    """
    Main function to execute the graph coloring simulation.
    """
    start = time.time()

    # Example usage with a DIMACS file
    graph = read_dimacs(filename="your_file_name.col", file_path="your_file_path")

    color_list, solved = color(graph, max_colors, max_steps)
    print(f"Completed search with colors: {color_list}\nSearch success: {solved}")

    end = time.time()
    print(f"Runtime: {end - start}")

    plt.show()


if __name__ == "__main__":
    rng = np.random.default_rng(123456)  # Initialize random number generator for reproducibility
    max_colors = 45  # Maximum number of colors to try
    max_steps = 500000  # Maximum number of steps in the local search

    main()
