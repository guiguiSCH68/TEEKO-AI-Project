from cell import *


class Player:
    def __init__(self, c: chr):
        self.__pawn_type = c
        self.__pawn = [Cell(), Cell(), Cell(), Cell()]

    def getPawn(self, n: int):
        if n >= 0 and n <= 3:
            return self.__pawn[n]
        else:
            return Cell()
        
    def getPawnIndex(self, num: int):
        for i in range(4):
            if self.__pawn[i].getNum() == num:
                return i
        return -1

    def getPawnType(self):
        return self.__pawn_type