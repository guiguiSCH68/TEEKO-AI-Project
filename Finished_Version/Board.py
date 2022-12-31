from Cell import *
import os


class Board:

    def __init__(self):
        self.__empty = '.'
        self.__grid = [[],
                       [],
                       [],
                       [],
                       []]
        for i in range(5):
            for j in range(5):
                self.__grid[j].append(self.__empty)

    '''
    le plateau de jeu  est vidé
    '''
    def clear(self):

        for i in range(5):
            for j in range(5):
                self.__grid[j][i] = self.__empty

    '''
    :return: le plateau de jeu
    '''
    def getGrid(self):
        return self.__grid

    '''
    :return: le caractère utilisé pour définir une case 'libre'
    '''
    def getEmpty(self):
        return self.__empty

    '''
    vérifie si dans la matrice il y a, à l'emplacement donné par le paramètre 'cell', un char égal au paramètre c
    :param cell: la cellule à vérifier
    :param c:  le caractère de vérification 
    :return: True ou False selon le cas
    '''
    def verifCell(self, cell: Cell, c: chr):

        if cell.getNum() == -1:
            return False
        else:
            if self.__grid[cell.getX()][cell.getY()] == c:
                return True
            else:
                return False

    '''
    modifie la matrice à l'emplacement de cell avec le paramètre c
    :param cell: la cellule à modifier
    :param c: le caractère remplaçant la caractère indiquant la place libre
    '''
    def changeCell(self, cell: Cell, c: chr):

        if cell.getNum() != -1:
            self.__grid[cell.getX()][cell.getY()] = c

    '''
    pareil que changeCell mais sur plusieurs emplacments
    :param cells: une liste de cellules
    :param c: le caractère remplaçant la caractère indiquant la place libre
    '''
    def changeCellList(self, cells: list, c: chr):

        if type(cells[0]) == Cell:
            for i in range(len(cells)):
                self.changeCell(cells[i], c)

    '''
    affiche les numéros autour du plateau de jeu
    :param n: le numéro à afficher
    :return: le numéro affiché sur l'écran
    '''
    @staticmethod
    def __printNombre__(n: int):

        if n < 10:
            print(" ", end="")
        print(n, end="")

    '''
    affiche le mot "Teeko" autour du plateau de je
    :param i: l'index de la lettre à afficher
    :return: la lettre relaitev à l'index ( T, K , O ou E)
    '''
    @staticmethod
    def __printTeeko__(i: int):

        
            if i == 0:
                print("T", end="")
            elif i == 3:
                print("K", end="")
            elif i == 4:
                print("O", end="")
            else:
                print("E", end="")

    '''
    s'occupe de l'affichage du jeu dans la console
    '''
    def print(self):

        # os.system("cls")
        print("    ┌───────────┐")
        print("    │ 1 2 3 4 5 │")
        print("┌───┼───────────┼───┐")
        for i in range(5):
            print("│", end="")
            self.__printNombre__(i * 5)
            print(" │", end="")
            for j in range(5):
                print("", self.__grid[j][i], end="")
            print(" │ ", end="")
            self.__printTeeko__(i)
            print(" │")
        print("└───┼───────────┼───┘")
        print("    │ T E E K O │")
        print("    └───────────┘")

    '''
    affiche le jeu avec le gagnant dans la console
    :param p_turn: le numéro du joueur
    :param p_type:  le type du joueur ( 'X' ou  'O' dans notre cas )
    '''
    def printWin(self, p_turn: int, p_type: chr):

        # os.system("cls")
        print("    ┌───────────┐")
        print("    │ 1 2 3 4 5 │")
        print("┌───┼───────────┼───┐")
        for i in range(5):
            print("│", end="")
            self.__printNombre__(i * 5)
            print(" │", end="")
            for j in range(5):
                print("", self.__grid[j][i], end="")
            print(" │ ", end="")
            self.__printTeeko__(i)
            print(" │", end="")
            self.__printWinner__(i, p_turn, p_type)
        print("└───┼───────────┼───┘")
        print("    │ T E E K O │")
        print("    └───────────┘")

    '''
    affiche une boîte indiquant le gagnant
    :param i: l'index de la ligne à afficher
    :param p_turn: le numéro du joueur
    :param p_type: le type du joueur ( 'X' ou  'O' dans notre cas )

    '''
    @staticmethod
    def __printWinner__(i: int, p_turn: int, p_type: chr):

        
            if i == 1:
                print("  ┌───────────────────────────┐")
            elif i == 2:
                print("  │ LE JOUEUR", p_turn + 1, "(",
                      p_type, ") A GAGNÉ │")
            elif i == 3:
                print("  └───────────────────────────┘")
            else :
                print("")