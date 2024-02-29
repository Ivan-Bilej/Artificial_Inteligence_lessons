"""
Barvení grafu pomocí lokálního prohledávání
"""
import random as rnd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib


def read_dimacs(filename):
    file = open(filename, 'r')
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


def local_coloring(graph: nx.Graph, local_node: int, col: list):
    good_coloring_count = 0
    bad_coloring_count = 0
    solved_mapping = {local_node: 1}

    for neighbour in graph.neighbors(local_node):
        if col[local_node] == col[neighbour]:
            print("Neighbour", neighbour, "isn't of a different color!")
            bad_coloring_count += 1
            solved_mapping[neighbour] = 0
        else:
            print("Neighbour", neighbour, "is of different color")
            good_coloring_count += 1
            solved_mapping[neighbour] = 1

    if bad_coloring_count > 0:
        return False, bad_coloring_count, good_coloring_count, solved_mapping
    else:
        return True, 0, graph.neighbors(local_node), solved_mapping


def is_coloring(graph: nx.Graph, col: list):
    bad_coloring_count = 0

    for local_node in range(graph.number_of_nodes()):
        for neighbour in graph.neighbors(local_node):
            if col[local_node] == col[neighbour]:
                print("Neighbour", neighbour, "isn't of a different color for local:", local_node)
                bad_coloring_count += 1
            else:
                print("Neighbour", neighbour, "is of different color for local:", local_node)

    if bad_coloring_count > 0:
        return False
    else:
        return True


def color(graph: nx.Graph, k: int, steps: int):
    local_node = 0
    optimum_count = 0

    # Creates color palette
    colors = [x for x in range(k)]
    color_list = [rng.choice(colors) for node in range(graph.number_of_nodes())]

    draw_graph(graph, color_list)
    print("looking with local node:", local_node)


    print("Started color list:", color_list)
    print("Start process of looking for color")
    while steps != 0:
        solved, bad_amount, good_amount, mapping = local_coloring(graph, local_node, color_list)

        if not solved:
            for node in mapping:
                if mapping[node] == 0:
                    print("Changing color of node:", node)
                    temp_colors = colors.copy()
                    print(temp_colors)
                    color_list[node] = rng.choice(temp_colors)
                    print("Changed list:", color_list)
            solved, bad_amount, good_amount, mapping = local_coloring(graph, local_node, color_list)
        elif local_node != graph.number_of_nodes():
            local_node += 1
        else:
            break
        draw_graph(graph, color_list)
        steps -= 1

    return color_list, is_coloring(graph, color_list)


def draw_graph(graph: nx.Graph, col_list: list):
    nx.draw(graph, pos=nx.circular_layout(graph), node_color=col_list, with_labels=True)
    plt.draw()
    plt.pause(0.02)


def main():
    graph = nx.erdos_renyi_graph(10, 0.25)

    color_list, solved = color(graph, color_number, max_steps)
    print("Completed search with colors", color_list, "\n and seach being", solved)
    plt.show()


if __name__ == "__main__":
    rng = np.random.default_rng(123456)
    colmap = ['salmon', 'skyblue']
    color_number = 4
    max_steps = 10

    main()
