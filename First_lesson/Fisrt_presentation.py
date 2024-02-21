import numpy
import math
import random as rnd
import statistics as stat
import timeit


def get_cells_amount_around(row: list, index: int) -> int:
    amount = 0

    for pos in range(1, max_search_pos + 1):
        if (index - pos) >= 0 and row[index - pos] == 1:
            amount += 1

    for pos in range(1, max_search_pos + 1):
        if (index + pos) < len(row) and row[index + pos] == 1:
            amount += 1

    #print(amount)
    return amount


def step(row: list) -> list:
    new_gen = []

    for index in range(0, len(row)):
        cell_around = get_cells_amount_around(row=row, index=index)

        if row[index] == 1 and cell_around in live_list:
            #print("Live")
            new_gen.append(1)
        elif row[index] == 0 and cell_around in birth_list:
            #print("Birth")
            new_gen.append(1)
        elif row[index] == 1 and cell_around in death_list:
            #print("Death")
            new_gen.append(0)
        else:
            #print("Nothing")
            new_gen.append(0)

    return new_gen


def printrow(row: list):
    line_text = ""

    for cell in row:
        if cell == 0:
            line_text += " "
        else:
            line_text += "*"

    print(line_text)


if __name__ == "__main__":
    live_list = [1, 4, 5, 6]
    birth_list = [3]
    death_list = [3]
    max_search_pos = 3
    row_length = 10

    #gen = [rnd.randrange(0, 2) for i in range(row_length)]
    gen = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

    #gen_max_number = rnd.randrange(5, 15)
    gen_max_number = 10
    printrow(row=gen)

    while gen_max_number > 0:
        gen = step(row=gen)
        printrow(row=gen)

        gen_max_number -= 1
