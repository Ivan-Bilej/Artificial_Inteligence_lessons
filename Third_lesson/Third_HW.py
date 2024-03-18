"""
Barvení grafu pomocí lokálního prohledávání
"""
import os
import random as rnd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib
import time


def read_dimacs(filename: str, file_path: str):
    file = open(os.path.join(file_path, filename), 'r')
    lines = file.readlines()

    Gd = nx.Graph()

    for line in lines:
        if line[0] == "e":
            vs = [int(s) for s in line.split() if s.isdigit()]
            Gd.add_edge(vs[0] - 1, vs[1] - 1)
    return Gd


# bere na vstupu pole barev vrcholu poporade, cislum priradi nahodne barvy a vykresli graf
def plot(graph: nx.Graph, cols: list):
    k = np.max(cols)
    symbols = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
    colmap = ["#" + ''.join(rng.choice(symbols, 6)) for i in range(k + 1)]

    colors = [colmap[c] for c in cols]

    nx.draw(graph, node_color=colors, with_labels=True)


def get_biggest_amount_of_edges(graph: nx.Graph):
    highest_number = 0
    highest_edges_node = 0

    for node in range(graph.number_of_nodes()):
        neighbour_count = len(list(graph.neighbors(node)))
        if neighbour_count > highest_number:
            highest_number = neighbour_count
            highest_edges_node = node

    print("Node with highest amount of edges", highest_edges_node)
    print("Highest amount of edges", highest_number)
    return highest_number


def local_coloring(graph: nx.Graph, local_node: int, col: list):
    bad_coloring_count = 0

    for neighbour in graph.neighbors(local_node):
        if col[local_node] == col[neighbour]:
            bad_coloring_count += 1

    if bad_coloring_count > 0:
        return False, bad_coloring_count
    else:
        return True, 0


def is_coloring(graph: nx.Graph, col: list):
    bad_coloring_count = 0

    for local_node in range(graph.number_of_nodes()):
        for neighbour in graph.neighbors(local_node):
            if col[local_node] == col[neighbour]:
                bad_coloring_count += 1

    return False if bad_coloring_count > 0 else True


def color(graph: nx.Graph, k: int, steps: int):
    local_node = 0
    optimum_count = 0

    # Creates color palette
    colors = [x for x in range(k)]
    color_list = [rng.choice(colors) for node in range(graph.number_of_nodes())]
    print(color_list)
    # Draws first graph with colors
    draw_graph(graph, color_list)

    print("Started color list:", color_list)
    while steps != 0:
        #print("Watched node: ", local_node)
        solved, bad_amount = local_coloring(graph, local_node, color_list)

        if not solved and optimum_count < max_optimum_steps:
            temp_bad_amounts = []
            temp_solutions = []

            r = rng.random()
            if r < 0.25:
                temp_color_list[local_node] = rng.choice(colors)
                solved, bad_amount = local_coloring(graph, local_node, temp_color_list)
                temp_bad_amounts.append(bad_amount)
                temp_solutions.append(temp_color_list)

            else:
                for neighbour in graph.neighbors(local_node):
                    temp_color_list = color_list.copy()
                    temp_color_list[local_node] = rng.choice(colors)
                    solved, bad_amount = local_coloring(graph, local_node, temp_color_list)
                    temp_bad_amounts.append(bad_amount)
                    temp_solutions.append(temp_color_list)

            index = temp_bad_amounts.index(min(temp_bad_amounts))
            # print("Possible solutions:", temp_solutions)
            # print("Bad amounts for solutions:", temp_bad_amounts)
            # print("Best solution index:", index)
            color_list = temp_solutions[index].copy()
            optimum_count += 1

        elif local_node < graph.number_of_nodes() - 1:
            local_node += 1
            optimum_count = 0
        else:
            if is_coloring(graph, color_list):
                break
            else:
                local_node = 0

        #draw_graph(graph, color_list)
        if steps % 100 == 0:
            print("Leftover steps:", steps)
            print("New color list:", color_list)
        steps -= 1

    return color_list, is_coloring(graph, color_list)


def draw_graph(graph: nx.Graph, col_list: list):
    nx.draw(graph, pos=nx.circular_layout(graph), node_color=col_list, with_labels=True)
    plt.draw()
    plt.pause(0.02)


def main():
    start = time.time()

    # graph = nx.erdos_renyi_graph(max_graph_size, 0.25)
    graph = read_dimacs(file_path="G:\Můj disk\Škola\Artificial_intelligence\Lesson_3",
                        filename="dsjc250.5.col.txt")

    #color_number = get_biggest_amount_of_edges(graph)
    color_number = max_colors

    color_list, solved = color(graph, color_number, max_steps)
    print("Completed search with colors", color_list, "\n and seach being", solved)
    #draw_graph(graph, color_list)

    end = time.time()
    print("Runtime:", end - start)

    plt.show()


if __name__ == "__main__":
    rng = np.random.default_rng(123456)
    colmap = ['salmon', 'skyblue']
    max_graph_size = 20
    max_colors = 45
    max_optimum_steps = 20
    max_steps = 500000

    # best 250.5: 45 colors
    # best 500.1: 29 colors
    main()
