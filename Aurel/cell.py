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

    def getX(self):
        return self.__x

    def getY(self):
        return self.__y
    
    def getNum(self):
        return self.__num
    
    def __coorToNum__(self):
        if self.__x == -1 or self.__y == -1:
            self.__num = -1
        else:
            self.__num = self.__x+1 + self.__y*5


    def __numToCoor__(self):
        if self.__num == -1:
            self.__x = -1
            self.__y = -1
        else:
            self.__x = (self.__num-1) % 5
            self.__y = (self.__num-1) // 5

    def setCoor(self, x: int, y: int):
        if x >= 0 and x <= 4 and y >= 0 and y <= 4:
            self.__x = x
            self.__y = y
        else:
            self.__x = -1
            self.__y = -1
        self.__coorToNum__()
        
    def setNum(self, n: int):
        if n >= 1 and n <= 25:
            self.__num = n
        else:
            self.__num = -1
        self.__numToCoor__()
