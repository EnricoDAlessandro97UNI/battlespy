# Legend:
# 'X' for placing ship and hit battleship
# ' ' for available space
# '-' for missed shot
# 'O' for ship placed

import os
import platform
import socket
import threading


ENEMY_BOARD = [[' '] * 8 for x in range(8)]
MY_BOARD = [[' '] * 8 for x in range(8)]

NICKNAME = 'NICKNAME'
FIRST = 'FIRST'
SECOND = 'SECOND'
ATTACK = 'ATTACK'
DEFENCE = 'DEFENCE'
HITTED = 'HITTED'
MISSED = 'MISSED'
SUNK = 'SUNK'

SHIPS = [2,3,4,5]
SHIPS_NAMES = ['incrociatore', 'sottomarino', 'corazzata', 'portaerei']
SHIPS_PLACED = {1:[], 2:[], 3:[], 4:[]}   #   (first coordinate, second coordinate)

letters_to_numbers = {'A': 0, 'B':1, 'C':2, 'D':3, 'E':4, 'F':5, 'G':6, 'H':7}
numbers_to_letters = {0:'A', 1:'B', 2:'C', 3:'D', 4:'E', 5:'F', 6:'G', 7:'H'}

sunk_ships = 0
enemy_sunk_ships = 0


def clear_screen():
    if OS == WINDOWS:
        os.system('cls')
    elif OS == LINUX:
        os.system('clear')
    elif OS == MACOS:
        os.system('clear')
    else:
        print('Sistema operativo non supportato')
        exit(0)


def print_board(board):
    print('\t\t   ---------------')
    print('\t\t   1 2 3 4 5 6 7 8')
    row_number = 1
    for row in range(len(board)):
        print("\t\t%s |" % (numbers_to_letters[row_number-1]), end="")
        for column in range(len(board[0])):
            print(board[row][column] + "|", end="")
        print("\n", end="")
        row_number += 1
    print('\t\t   ---------------')


def print_all_board():
    clear_screen()
    print("\n")
    print("\t\t   GRIGLIA NEMICA")
    print_board(ENEMY_BOARD)
    print("\n\t\t  GRIGLIA PERSONALE")
    print_board(MY_BOARD)


def create_ships(board):
    count = 0
    for ship in SHIPS:
        for _ in range(ship):
            print('\n\t\tPosiziona la nave ' + SHIPS_NAMES[count].upper() + ' (dimensione=' + str(ship) + ')')
            row, column = get_ship_location()
            while board[row][column] == 'O':
                print('\t\tAttenzione, hai già posizionato qualcosa nella coordinata indicata!')
                row, column = get_ship_location()
            board[row][column] = 'O'
            #SHIPS_PLACED[count].append((numbers_to_letters[row], column+1, 'N'))
            SHIPS_PLACED[count+1].append({1:row, 2:column})
            print_all_board()
        count += 1


def get_ship_location():

    # Inserimento riga
    row = input('\n\t\tInserire la riga (A-H): ').upper()
    while (row not in ['A','B','C','D','E','F','G','H'] or row == ''):
        row = input('\t\tAttenzione, inserire una riga valida (A-H): ').upper()
    
    # Inserimento colonna
    column = input('\t\tInserire la colonna (1-8): ')
    while (column not in ['1','2','3','4','5','6','7','8'] or column == ''):
        column = input('\t\tAttenzione, inserire una colonna valida (1-8): ')

    return letters_to_numbers[row], int(column)-1


def enemy_hitted(row, column):
    ENEMY_BOARD[row][column] = 'X'


def enemy_missed(row, column):
    ENEMY_BOARD[row][column] = '-'


def enemy_sunk(row, column):

    global enemy_sunk_ships

    ENEMY_BOARD[row][column] = 'X'
    enemy_sunk_ships += 1
    if (enemy_sunk_ships == len(SHIPS)):
        print("\n\t\tVITTORIA, HAI AFFONDATO TUTTE LE NAVI DELL'AVVERSARIO :)")
        input('\n\t\tPremere INVIO per terminare ...')
        client.close()
        exit(0)


def get_hitted_ship(row, column):
    for ship in SHIPS_PLACED:
        for coord in SHIPS_PLACED[ship]:
            if (coord[1] == row and coord[2] == column):
                return ship
    return None


def check_sunk(row, column):

    global sunk_ships

    ship = get_hitted_ship(row, column)
    for coord in SHIPS_PLACED[ship]: # controllo se ogni coordinata di quella barca è stata colpita
        if (MY_BOARD[coord[1]][coord[2]] == 'O'):
            return 0
    sunk_ships += 1
    return 1        
    

def check_attack(row, column):
    # Check MY_BOARD
    if MY_BOARD[row][column] == 'O':
        MY_BOARD[row][column] = 'X' # aggiorno lo stato della barca in colpita nella coordinata (row, column)
        if (check_sunk(row, column)):
            return -1 # nave affondata
        return 1 # nave colpita, ma sopravvissuta
    else:
        MY_BOARD[row][column] = '-'
        return 0 # nave mancata


def handle_attack():

    # Inserisci la coordinata da attaccare
    row, column = get_ship_location()
    if ENEMY_BOARD[row][column] != ' ':
        print("\t\tAttenzione, coordinata nemica già attaccata")
        row, column = get_ship_location()

    # Comunica l'attacco
    msg = DEFENCE + "-" + str(row) + "-" + str(column)
    client.send(msg.encode('ascii'))

    # Attesa dell'esito dell'attacco (colpito, non colpito, colpito ed affondato)
    msg = client.recv(1024).decode('ascii')
    results = msg.split("-")
    result = results[0]
    row = int(results[1])
    column = int(results[2])
    if result == HITTED: # nemico colpito
        enemy_hitted(row, column)
    elif result == MISSED: # nemico mancato
        enemy_missed(row, column)
    elif result == SUNK: # nemico colpito ed affondato
        enemy_sunk(row, column)

    print_all_board()

    # Comunica all'avversario la fine dell'attacco
    msg = ATTACK
    client.send(msg.encode('ascii'))

    if (result == HITTED):
        print("\n\t\tNAVE NEMICA COLPITA")
    elif (result == MISSED):
        print("\n\t\tNAVE NEMICA MANCATA")
    else:
        print("\n\t\tNAVE NEMICA COLPITA ED AFFONDATA")


def handle_defence(msg):

    # Coordinata del nemico
    msg_received = msg.split("-")
    row = int(msg_received[1])
    column = int(msg_received[2])

    # Controlla esito attacco
    result = check_attack(row, column)

    print_all_board()

    if (result == 1): # colpito
        msg = HITTED + "-" + str(row) + "-" + str(column)
        client.send(msg.encode('ascii'))
    elif (result == 0): # mancato
        msg = MISSED + "-" + str(row) + "-" + str(column)
        client.send(msg.encode('ascii'))
    else: # nave colpita ed affondata
        msg = SUNK + "-" + str(row) + "-" + str(column)
        client.send(msg.encode('ascii'))
        if (sunk_ships == len(SHIPS)):
            print("\n\t\tSCONFITTA, HAI PERSO TUTTE LE NAVI :(")
            input('\n\t\tPremere INVIO per terminare ...')
            client.close()
            exit(0)
    

def receive():
    
    global enemy_sunk_ships 

    while True:
        try:
            # Receive message from server
            msg = client.recv(1024).decode('ascii')
            actions = msg.split("-")

            if actions[0] == NICKNAME:
                client.send(nickname.encode('ascii'))

            elif actions[0] == FIRST:
                print_all_board()
                create_ships(MY_BOARD)
                print("\n\t\t" + nickname + ", giochi per primo")
                handle_attack()
                print("\n\t\tIn attesa della mossa dell'avversario ...")

            elif actions[0] == SECOND:
                print_all_board()
                create_ships(MY_BOARD)
                print("\n\t\t" + nickname + ", giochi per secondo")
                print("\n\t\tIn attesa della mossa dell'avversario ...")

            elif actions[0] == ATTACK:
                print("\n\t\t" + nickname + " tocca a te!")
                handle_attack()   
                print("\n\t\tIn attesa della mossa dell'avversario ...")             

            elif actions[0] == DEFENCE:
                handle_defence(msg)

            else:
                print(msg)

        except KeyboardInterrupt:
            # Close connection when error
            print("Ctrl+C premuto")
            client.close()
            break


if __name__ == '__main__':

    # Server connection data
    SERVER = ''
    PORT = 55555

    WINDOWS = "windows"
    LINUX = "linux"
    MACOS = "darwin"
    OS = platform.system().lower()

    clear_screen()

    # Server's IP
    SERVER = input("Inserire l'IP del server: ")

    # Choosing nickname
    nickname = input("Scegli il tuo nickname: ")

    # Connecting to server
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER, PORT))

    # Starting threads for listening and writing
    receive_thread = threading.Thread(target=receive)
    receive_thread.start()