from Cell import *


class Player:

    def __init__(self, c: chr):
        self.__pawn_type = c
        self.__pawn = [Cell(), Cell(), Cell(), Cell()]

    '''
    récupère un pion
    :param n: le numéro du pion à récupérer
    :return:le pion 
    '''
    def getPawn(self, n: int):

        if n >= 0 and n <= 3:
            return self.__pawn[n]
        else:
            return Cell()

    '''
    récupère l'index d'un pion
    :param num: le numéro de la case du pion 
    :return: l'index
    '''
    def getPawnIndex(self, num: int):

        for i in range(4):
            if self.__pawn[i].getNum() == num:
                return i
        return -1

    '''
    retourne le type du pion
    :return: le type du pion
    '''
    def getPawnType(self):
        return self.__pawn_type