from board import *
from player import *


class Game:
    def __init__(self):
        self.__board = Board()
        self.__player_turn = 0
        self.__player = [Player("X"), Player("O")]

    def game(self):
        i = 0
        stop = False
        while i < 8 and not stop:
            self.__board.print()
            self.__playPlacement__()
            self.updateBoard()
            i += 1
            if self.__win__():
                stop = True
            else:
                self.__changePlayer__()
        
        while not stop:
            go_back = True
            while go_back:
                self.__board.print()
                pawn = self.__pawnChoice__()
                cell = self.__player[self.__player_turn].getPawn(pawn)
                choice_list = self.__movable__(cell)
                self.__board.changeCellList(choice_list, '+')
                self.__board.print()
                move = self.__moveChoice__(pawn, choice_list)
                self.__board.changeCellList(
                    choice_list, self.__board.getEmpty())
                if move.getNum() != -1:
                    cell.setNum(move.getNum())
                    go_back = False
                    self.updateBoard()
                    if self.__win__():
                        stop = True
                    else:
                        self.__changePlayer__()
                        
        self.__board.print()
        print("\nLE JOUEUR", self.__player_turn+1, "(", self.__player[self.__player_turn].getPawnType(), ") A GAGNÉ\n")

    def __textPlayer__(self):
        print(
            "Joueur", self.__player_turn + 1, ": (", self.__player[self.__player_turn].getPawnType(), ") : ", end="")

    def __boxChoice__(self):
        choice = 0
        while choice < 1 or choice > 25:
            self.__textPlayer__()
            answer = input("Choisissez une case (entre 1 et 25) : ")
            if answer.isnumeric():
                choice = int(answer)
        return choice

    def __changePlayer__(self):
        if self.__player_turn == 0:
            self.__player_turn = 1
        else:
            self.__player_turn = 0

    def __registerPawn__(self, cell: Cell):
        n = 0
        while self.__player[self.__player_turn].getPawn(n).getNum() != -1 and n < 3:
            n += 1
        if n <= 3:
            self.__player[self.__player_turn].getPawn(n).setNum(cell.getNum())
        else:
            print("ERROR")

    def __playPlacement__(self):
        cell = Cell()
        while not self.__board.verifCell(cell, self.__board.getEmpty()):
            cell.setNum(self.__boxChoice__())
        self.__registerPawn__(cell)

    def updateBoard(self):
        self.__board.clear()
        for i in range(2):
            for j in range(4):
                self.__board.changeCell(self.__player[i].getPawn(
                    j), self.__player[i].getPawnType())

    def __movable__(self, cell: Cell):
        l = []
        x = cell.getX()
        y = cell.getY()
        if x != -1 and y != -1:
            for i in range(3):
                for j in range(3):
                    if x+j-1 >= 0 and x+j-1 <= 4 and y+i-1 >= 0 and y+i-1 <= 4:
                        if self.__board.verifCell(Cell(x+j-1, y+i-1), self.__board.getEmpty()):
                            l.append(Cell(x+j-1, y+i-1))
        return l

    def __pawnChoice__(self):
        n = 0
        possible = []
        self.__textPlayer__()
        print("")
        for i in range(4):
            if len(self.__movable__(self.__player[self.__player_turn].getPawn(i))) > 0:
                n += 1
                possible.append(self.__player[self.__player_turn].getPawn(i).getNum())
        pawn = 0
        while (pawn in possible) == False:
            print("Quel pion voulez-vous déplacer ( ", end="")
            for i in range(n-1):
                print(possible[i], "/ ", end="")
            print(possible[n-1], ") ? ", end="")
            answer = input()
            if answer.isnumeric():
                pawn = int(answer)
        return self.__player[self.__player_turn].getPawnIndex(pawn)

    def __moveChoice__(self, pawn: int, choice_list: list):
        self.__textPlayer__()
        print("")
        print("Pion sur la case",
              self.__player[self.__player_turn].getPawn(pawn).getNum(), "sélectionné")
        print("Vous pouvez déplacer votre pion sur toutes les cases avec le symbole '+'")
        choice = -1
        while not self.__inCellList__(Cell(choice), choice_list) and choice != 0:
            print("Sur quelle case souhaitez-vous déplacer votre pion ( ", end="")
            for i in range(len(choice_list)):
                print(choice_list[i].getNum(), "/ ", end="")
            print("'r' pour retourner au choix du pion) ? ", end="")
            answer = input()
            if answer.isnumeric():
                choice = int(answer)
            elif answer == 'r':
                choice = 0
        return Cell(choice)

    @staticmethod
    def __inCellList__(cell: Cell, cell_list: list):
        for i in range(len(cell_list)):
            if cell.getNum() == cell_list[i].getNum():
                return True
        return False
    
    def __win__(self):
        px = self.__player[self.__player_turn].getPawn(0).getX()
        py = self.__player[self.__player_turn].getPawn(0).getY()
        p_type = self.__player[self.__player_turn].getPawnType()
        n = 0
        x = -1
        while x <= 1 and n == 0:
            y = -1
            while y <= 1 and n == 0:
                if not ( x == 0 and y == 0):
                    if self.__board.verifCell(Cell(px+x, py+y), p_type):
                        n += 1
                        x_sol = x
                        y_sol = y
                y += 1
            x += 1
        if n != 0:
            for i in range(2):
                m = 2
                while self.__board.verifCell(Cell(px+(x_sol*m), py+(y_sol*m)), p_type):
                    n += 1
                    m += 1
                x_sol = -x_sol
                y_sol = -y_sol
            if n == 3:
                return True
        return False