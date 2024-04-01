import numpy  # Unused import, consider removing if not needed elsewhere in your code
import math  # Unused import, consider removing if not needed elsewhere in your code
import random as rnd  # Used for initializing the generation, can be removed if fixed initialization is used
import statistics as stat  # Unused import, consider removing if not needed elsewhere in your code
import timeit  # Unused import, consider removing if not needed elsewhere in your code


def get_cells_amount_around(row: list, index: int) -> int:
    """
    Calculates the number of active (living) cells adjacent to a given cell in the row.

    This function examines cells up to `max_search_pos` positions away from the target cell,
    considering both directions (left and right) within the same row. Only directly adjacent
    cells are considered because `max_search_pos` is set to 1.

    :param row: List representing the current generation of cells (0 for dead, 1 for alive)
    :param index: The position of the target cell within the row
    :return: The count of living cells adjacent to the target cell
    """
    amount = 0
    max_search_pos = 1  # This value should be defined globally if used in multiple functions

    # Check left of the target cell
    for pos in range(1, max_search_pos + 1):
        if (index - pos) >= 0 and row[index - pos] == 1:
            amount += 1

    # Check right of the target cell
    for pos in range(1, max_search_pos + 1):
        if (index + pos) < len(row) and row[index + pos] == 1:
            amount += 1

    return amount


def step(row: list) -> list:
    """
    Generates the next state (generation) of the cell row based on predefined rules.

    The function iterates through each cell in the current generation. For each cell, it:
    - Preserves alive cells (`1`) if they have a number of adjacent alive cells found in `live_list`.
    - Generates a new alive cell (`1`) at the position of a dead cell (`0`) if the number of adjacent alive cells matches `birth_list`.
    - Kills alive cells (`1`) if they have a number of adjacent alive cells found in `death_list`.
    If none of these conditions are met, the cell remains or becomes dead (`0`).

    :param row: The current generation of cells
    :return: The next generation of cells
    """
    new_gen = []
    live_list = [2, 3, 4]  # Criteria for a cell to stay alive
    birth_list = []  # Criteria for a dead cell to become alive (seems unused, consider defining if applicable)
    death_list = []  # Criteria for a cell to die (seems unused, consider defining if applicable)

    for index in range(len(row)):
        cell_around = get_cells_amount_around(row=row, index=index)

        # Determine the new state of the cell based on its neighbors and specific rules
        if row[index] == 1 and cell_around in live_list:
            new_gen.append(1)  # Cell stays alive
        elif row[index] == 0 and cell_around in birth_list:
            new_gen.append(1)  # Cell becomes alive
        elif row[index] == 1 and cell_around in death_list:
            new_gen.append(0)  # Cell dies
        else:
            new_gen.append(0)  # Cell remains dead or dies

    return new_gen


def printrow(row: list):
    """
    Prints the current state of the cell row to the console.

    Converts the cell row list into a string, where alive cells (`1`) are represented by
    '*' and dead cells (`0`) by a space character, for a visual representation of the generation.

    :param row: The current generation of cells to print
    """
    line_text = "".join("*" if cell == 1 else " " for cell in row)
    print(line_text)


if __name__ == "__main__":
    row_length = 10
    gen = [1] * row_length  # Initialize the first generation with all cells alive
    gen_max_number = 20  # Number of generations to simulate

    printrow(row=gen)
