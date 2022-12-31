class Cell:

    def __init__(self, orig1=None, orig2=None):
        if orig2 is None:
            if orig1 is None:
                self.__x = -1
                self.__y = -1
                self.__num = -1
            else:
                self.setNum(orig1)
        else:
            self.setCoor(orig1, orig2)

    '''
    :return: la coordonnée x de la cellule
    '''
    def getX(self):

        return self.__x

    '''
    :return: la coordonnée y de la cellule
    '''
    def getY(self):
        return self.__y

    '''
    :return: le numéro de la cellule
    '''
    def getNum(self):
        return self.__num

    '''
    calcule le numéro en fonction des coordonnées
    '''
    def __coorToNum__(self):
        if self.__x == -1 or self.__y == -1:
            self.__num = -1
        else:
            self.__num = self.__x + 1 + self.__y * 5

    '''
    calcule les coordonnées en fonction du numéro
    '''
    def __numToCoor__(self):
        if self.__num == -1:
            self.__x = -1
            self.__y = -1
        else:
            self.__x = (self.__num - 1) % 5
            self.__y = (self.__num - 1) // 5

    '''
    définit les coordonnées et complète le numéro en fonction des coordonnées
    :param x: la coordonnée x de la cellule 
    :param y: le coordonnée y de la cellule
    '''
    def setCoor(self, x: int, y: int):

        if x >= 0 and x <= 4 and y >= 0 and y <= 4:
            self.__x = x
            self.__y = y
        else:
            self.__x = -1
            self.__y = -1
        self.__coorToNum__()

    '''
    définit le numéro et complète les coordonnées en fonction du numéro
    :param n: le numéro de la cellule
    '''
    def setNum(self, n: int):
        if n >= 1 and n <= 25:
            self.__num = n
        else:
            self.__num = -1
        self.__numToCoor__()