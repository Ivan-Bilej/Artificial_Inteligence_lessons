import numpy as np


# kreslí hru
def printgame(g):
    for r in g:
        pr = ""
        for i in r:
            if i == 0:
                pr += "."
            elif i == 1:
                pr += "x"
            else:
                pr += "o"
        print(pr)


# říká kdo vyhrál 0=nikdo, 1, 2
def whowon(g):
    # řádek
    if g[0][:] == [1, 1, 1] or g[1][:] == [1, 1, 1] or g[2][:] == [1, 1, 1]:
        return 1

    if g[0][:] == [2, 2, 2] or g[1][:] == [2, 2, 2] or g[2][:] == [2, 2, 2]:
        return 2

    # 1. sloupec
    if g[0][0] == g[1][0] == g[2][0] == 1:
        return 1

    if g[0][0] == g[1][0] == g[2][0] == 2:
        return 2

    # 2. sloupec
    if g[0][1] == g[1][1] == g[2][1] == 1:
        return 1

    if g[0][1] == g[1][1] == g[2][1] == 2:
        return 2

    # 3. sloupec
    if g[0][2] == g[1][2] == g[2][2] == 1:
        return 1

    if g[0][2] == g[1][2] == g[2][2] == 2:
        return 2

    # hlavní diagonála
    if g[0][0] == g[1][1] == g[2][2] == 1:
        return 1

    if g[0][0] == g[1][1] == g[2][2] == 2:
        return 2

    # hlavní anti-diagonála
    if g[0][2] == g[1][1] == g[2][0] == 1:
        return 1

    if g[0][2] == g[1][1] == g[2][0] == 2:
        return 2

    return 0


# vrací prázdná místa na šachovnici
def emptyspots(g):
    emp = []
    for i in range(3):
        for j in range(3):
            if g[i][j] == 0:
                emp.append((i, j))
    return emp


def ttt_move(game, myplayer, otherplayer):
    # todo <--------------------
    possible_games = []
    game_steps = {}
    empty_spaces = emptyspots(game)

    for empty_space in empty_spaces:
        i, j = empty_space
        temp_game = game
        temp_game[i][j] = myplayer
        possible_games.append(temp_game)

    while possible_games:
        played_p1 = True
        played_p2 = False

        for g_index in range(len(possible_games)):
            empty_spaces = emptyspots(possible_games[g_index])

            if played_p1 and not played_p2:
                for empty_space in empty_spaces:
                    i, j = empty_space
                    temp_game = possible_games[g_index]
                    temp_game[i][j] = myplayer

    return game


if __name__ == "__main__":
    play_field = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    game_step = ttt_move(play_field, 1, 2)

    printgame(game_step)