from cell import *

class Board:
    def __init__(self):
        self.__empty = '·'
        self.__grid = [[], [], [], [], []]
        for i in range(5):
            for j in range(5):
                self.__grid[j].append(self.__empty)
                
    def clear(self):
        for i in range(5):
            for j in range(5):
                self.__grid[j][i] = self.__empty

    def getEmpty(self):
        return self.__empty

    def verifCell(self, cell: Cell, c: chr):
        if cell.getNum() == -1:
            return False
        else:
            if self.__grid[cell.getX()][cell.getY()] == c:
                return True
            else:
                return False

    def changeCell(self, cell: Cell, c: chr):
        if cell.getNum() != -1:
            self.__grid[cell.getX()][cell.getY()] = c


    def changeCellList(self, cells: list, c: chr):
        if type(cells[0]) == Cell:
            for i in range(len(cells)):
                self.changeCell(cells[i], c)

    @staticmethod
    def __printNombre__(n: int):
        if n < 10:
            print(" ", end="")
        print(n, end="")

    @staticmethod
    def __printTeeko__(i: int):
        match i:
            case 0:
                print("T", end="")
            case 3:
                print("K", end="")
            case 4:
                print("O", end="")
            case _:
                print("E", end="")

    def print(self):
        print("    ┌───────────┐")
        print("    │ 1 2 3 4 5 │")
        print("┌───┼───────────┼───┐")
        for i in range(5):
            print("│", end="")
            self.__printNombre__(i*5)
            print(" │", end="")
            for j in range(5):
                print("", self.__grid[j][i], end="")
            print(" │ ", end="")
            self.__printTeeko__(i)
            print(" │")
        print("└───┼───────────┼───┘")
        print("    │ T E E K O │")
        print("    └───────────┘")
