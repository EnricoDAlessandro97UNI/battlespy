# Legend:
# 'X' for placing ship and hit battleship
# ' ' for available space
# '-' for missed shot

import os
from random import randint


HIDDEN_BOARD = [[' '] * 8 for x in range(8)]
GUESS_BOARD = [[' '] * 8 for x in range(8)]

letters_to_numbers = {'A': 0, 'B':1, 'C':2, 'D':3, 'E':4, 'F':5, 'G':6, 'H':7}
numbers_to_letters = {0:'A', 1:'B', 2:'C', 3:'D', 4:'E', 5:'F', 6:'G', 7:'H'}


def print_board(board):
    print('\t\t  1 2 3 4 5 6 7 8')
    print('\t\t  ---------------')
    row_number = 1
    for row in range(len(board)):
        print("\t\t%s|" % (numbers_to_letters[row_number-1]), end="")
        for column in range(len(board[0])):
            print(board[row][column] + "|", end="")
        print("\n", end="")
        row_number += 1


def create_ships(board):
    for ship in range(8):
        ship_row, ship_column = randint(0,7), randint(0,7)
        while board[ship_row][ship_column] == 'X':
            ship_row, ship_column = randint(0,7), randint(0,7)
        board[ship_row][ship_column] = 'X'


def get_ship_location():
    row = input('\n\t\tPlease enter a ship row A-H: ').upper()
    while row not in 'ABCDEFGH':
        print('\t\tPlease enter a valid row')
        row = input('\t\tPlease enter a ship row A-H: ').upper()
    column = input('\t\tPlease enter a ship column 1-8: ')
    while column not in '12345678':
        print('\t\tPlease enter a valid column')
        row = input('\t\tPlease enter a ship column 1-8: ')
    return letters_to_numbers[row], int(column)-1


def count_hit_ships(board):
    count = 0
    for row in board:
        for column in row:
            if column == 'X':
                count += 1
    return count


if __name__ == '__main__':
    print('\n')
    create_ships(HIDDEN_BOARD)
    print_board(HIDDEN_BOARD)
    turns = 20
    while turns > 0:
        os.system('clear')
        print('\n\t\tWELCOME TO BATTLESHIP\t\t' + str(turns) + ' turns remaining\n')
        print_board(GUESS_BOARD)
        row, column = get_ship_location()
        if GUESS_BOARD[row][column] == '-':
            print('\n\t\tAttention, you already guessed that')
        elif HIDDEN_BOARD[row][column] == 'X':
            print('\n\t\tCongratulations, you have hit the battleship\n')
            GUESS_BOARD[row][column] = 'X'
            #turns -= 1
        else:
            print('\n\t\tSorry, you missed')
            GUESS_BOARD[row][column] = '-'
            turns -= 1
        if count_hit_ships(GUESS_BOARD) == 5:
            print('\t\tCongratulations, you have sunk all the battleships\n')
            break
        print('\t\tYou have ' + str(turns) + ' turns remaining\n')
        if turns == 0:
            print('\t\tSorry, you ran out of turns, game over\n')
            break
        input('\n\t\tPress enter to continue\n')