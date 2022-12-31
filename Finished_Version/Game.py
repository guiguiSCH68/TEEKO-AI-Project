from Board import *
from Player import *
from MinMax import *
from Placement import *
import random


class Game:

    def __init__(self):
        self.__board = Board()
        self.__player_turn = 0
        self.__player = [Player("X"), Player("O")]

    '''
    tout le processus du jeu dans la console
    '''
    def game(self):
        strength = 1 #force "facile" par défaut
        print("")
        print("Choisissez le mode de jeu : ")
        game = self.__choiceMenu__()
        if game == 2:
            print("")
            print("Choisissez la force de l'IA : ")
            strength = self.__strengthChoice__()
        self.__player_turn = 0
        i = 0
        stop = False
        num_passage = 1
        while i < 8 and not stop:  # phase de placement

            if (game == 1) or (game == 2 and self.__player_turn == 0):  # humain/humain ou tour de l'humain si humain/ia
                self.__playPlacement__()
                self.updateBoard()

            else:
                if num_passage >4:
                    break
                else:
                    self.updateBoard()
                    self.__playPlacementAI__(self.__board.getGrid(),num_passage)
                    num_passage += 1

            self.updateBoard()
            i += 1
            if self.__win__():
                stop = True
            else:
                self.__changePlayer__()

        while not stop:  # phase de déplacement
            go_back = True
            while go_back:
                if (game == 1) or (game == 2 and self.__player_turn == 0):  # humain/humain ou tour de l'humain si humain/ia
                    pawn = self.__pawnChoice__()
                    cell = self.__player[self.__player_turn].getPawn(pawn)
                    choice_list = self.__movable__(cell)
                    self.__board.changeCellList(choice_list, '+')
                    move = self.__moveChoice__(pawn, choice_list)
                    self.__board.changeCellList(choice_list, self.__board.getEmpty())
                else:
                    self.updateBoard()
                    j1 = 'HUM'
                    j2 = 'IA'
                    TEST = Heuristique([], [],[],[])
                    liste_pionsX = TEST.recup_pos_pions(self.__board.getGrid(), j1)
                    liste_pionsO = TEST.recup_pos_pions(self.__board.getGrid(), j2)

                    if strength == 1: #mode facile
                        type_heuristique = 1
                        IA = MinMax(j1, j2, liste_pionsO, liste_pionsX, self.__board.getGrid())
                        IA.minmax_avec_alpha_beta(self.__board.getGrid(), 'O', 3, -100, 100,type_heuristique)  # minmax de profondeur 3 avec heuristique "simple"
                        choice = IA.donner_coup_opti()
                        cell = self.__player[self.__player_turn].getPawn(self.__player[self.__player_turn].getPawnIndex(Cell(choice[0][0], choice[0][1]).getNum()))
                        move = Cell(choice[1][0], choice[1][1])

                    elif strength == 2: #mode modéré
                        type_heuristique =2
                        IA = MinMax(j1, j2, liste_pionsO, liste_pionsX, self.__board.getGrid())
                        IA.minmax_avec_alpha_beta(self.__board.getGrid(), 'O', 2, -100, 100,type_heuristique) #minmax de profondeur 2 avec heuristique complexe
                        choice = IA.donner_coup_opti()
                        cell = self.__player[self.__player_turn].getPawn(self.__player[self.__player_turn].getPawnIndex(Cell(choice[0][0], choice[0][1]).getNum()))
                        move = Cell(choice[1][0], choice[1][1])
                    else: #mode avancé
                        type_heuristique = 2
                        IA = MinMax(j1, j2, liste_pionsO, liste_pionsX, self.__board.getGrid())
                        IA.minmax_avec_alpha_beta(self.__board.getGrid(), 'O', 4, -100, 100,type_heuristique)#minmax de profondeur 4 avec heuristique complexe
                        choice = IA.donner_coup_opti()
                        cell = self.__player[self.__player_turn].getPawn(self.__player[self.__player_turn].getPawnIndex(Cell(choice[0][0], choice[0][1]).getNum()))
                        move = Cell(choice[1][0], choice[1][1])

                if move.getNum() != -1:
                    cell.setNum(move.getNum())
                    go_back = False
                    self.updateBoard()
                    if self.__win__():
                        stop = True
                    else:
                        self.__changePlayer__()

        self.__board.printWin(self.__player_turn, self.__player[self.__player_turn].getPawnType())

    '''
    une boîte indiquant le mode à choisir
    '''
    @staticmethod
    def __startMenu__():
        # os.system("cls")
        print("┌─────────────────────────┐")
        print("│ 1. JOUEUR CONTRE JOUEUR │")
        print("│ 2. JOUEUR CONTRE IA     │")
        print("│ 3. ARRET                │")
        print("├─────────────────────────┤")
        print("│ ENTREZ 1, 2 OU 3        │")
        print("└─────────────────────────┘")

    '''
    une boîte indiquant la force de l'IA à choisir
    '''
    @staticmethod
    def __strengthMenu__():
        # os.system("cls")
        print("┌─────────────────────────┐")
        print("│ 1. LEGER                │")
        print("│ 2. MODERE               │")
        print("│ 3. AVANCE               │")
        print("├─────────────────────────┤")
        print("│ ENTREZ 1, 2 OU 3        │")
        print("└─────────────────────────┘")

    '''
    le choix du joueur concernant le mode
    :return: le choix du mode
    '''
    def __choiceMenu__(self):
        choice = 0
        while choice < 1 or choice > 3:
            self.__startMenu__()
            answer = input()
            if answer.isnumeric():
                choice = int(answer)

            if choice == 3:
                quit()
        return choice

    '''
    le choix du joueur concernant la force de l'IA
    return: le choix de la force
    '''
    def __strengthChoice__(self):
        choice = 0
        while choice < 1 or choice > 3:
            self.__strengthMenu__()
            answer = input()
            if answer.isnumeric():
                choice = int(answer)
        return choice

    '''
    une phrase indiquant quel joueur doit jouer
    '''
    def __textPlayer__(self):
        print(
            "Joueur", self.__player_turn + 1, ": (", self.__player[self.__player_turn].getPawnType(), ") : ", end="")

    '''
    le choix de la case que doit faire l'humain
    :return: le choix de la case
    '''
    def __boxChoice__(self):
        choice = 0
        while choice < 1 or choice > 25:
            self.__board.print()
            self.__textPlayer__()
            answer = input("Choisissez une case (entre 1 et 25) : ")
            if answer.isnumeric():
                choice = int(answer)
        return choice

    '''
    selon le joueur entrant, renvoie la valeur de l'autre
    '''
    def __changePlayer__(self):
        if self.__player_turn == 0:
            self.__player_turn = 1
        else:
            self.__player_turn = 0

    '''
    enregistre la cellule du joueur
    :param cell: la cellule à enregistrer
    '''
    def __registerPawn__(self, cell: Cell):

        n = 0
        while self.__player[self.__player_turn].getPawn(n).getNum() != -1 and n < 3:
            n += 1
        if n <= 3:
            self.__player[self.__player_turn].getPawn(n).setNum(cell.getNum())
        else:
            print("ERROR")

    '''
    le placement effectué par le joueur
    '''
    def __playPlacement__(self):
        cell = Cell()
        while not self.__board.verifCell(cell, self.__board.getEmpty()):
            cell.setNum(self.__boxChoice__())  # boxchoice entre 1 et 25
        self.__registerPawn__(cell)

    '''
    le placement effectué par l'IA
    :param game_state: le plateau de  jeu actuel
    :param num_passage: le numéro du pion à placer
    '''
    def __playPlacementAI__(self,game_state,num_passage):

        Place = Placement()  # instanciation d'une ia
        choice = Place.placement_pion_dans_jeu(game_state,num_passage,'O')
        cell = Cell()
        i = choice[0]
        j = choice[1]
        numero_case_placement = (i + 1) + (5 * j)
        cell.setNum(numero_case_placement)  # boxchoice entre 1 et 25
        print(cell.getNum())
        self.__registerPawn__(cell)

    '''
    acutalisation du jeu
    '''
    def updateBoard(self):
        self.__board.clear()
        for i in range(2):
            for j in range(4):
                self.__board.changeCell(self.__player[i].getPawn(
                    j), self.__player[i].getPawnType())

    '''
    indique les positions oùu le joueur peut déplacer son pion
    :param cell: la cellule du joueur ( = son pion)
    :return: les positions libres
    '''
    def __movable__(self, cell: Cell):

        l = []
        x = cell.getX()
        y = cell.getY()
        if x != -1 and y != -1:
            for i in range(3):
                for j in range(3):
                    if x + j - 1 >= 0 and x + j - 1 <= 4 and y + i - 1 >= 0 and y + i - 1 <= 4:
                        if self.__board.verifCell(Cell(x + j - 1, y + i - 1), self.__board.getEmpty()):
                            l.append(Cell(x + j - 1, y + i - 1))
        return l

    '''
    choix du pion par le joueur
    :return: l'index du pion du joueur
    '''
    def __pawnChoice__(self):
        n = 0
        possible = []
        for i in range(4):
            if len(self.__movable__(self.__player[self.__player_turn].getPawn(i))) > 0:
                n += 1
                possible.append(
                    self.__player[self.__player_turn].getPawn(i).getNum())
        pawn = 0
        while (pawn in possible) == False:
            self.__board.print()
            self.__textPlayer__()
            print("")
            print("Quel pion voulez-vous déplacer ( ", end="")
            for i in range(n - 1):
                print(possible[i], "/ ", end="")
            print(possible[n - 1], ") ? ")
            print("Vous pouvez également appuyer sur 'Q' pour quitter le programme")
            answer = input()
            if answer.isnumeric():
                pawn = int(answer)
            elif answer == 'q' or 'Q':
                quit()
        return self.__player[self.__player_turn].getPawnIndex(pawn)

    '''
    indique le pion sélectionné et les positions où il peut être déplacé
    :param pawn: le pion à déplacer
    :param choice_list: la liste des positions disponibles
    :return: l'actualisation de la position du pion
    '''
    def __moveChoice__(self, pawn: int, choice_list: list):

        self.__board.print()
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

    '''
    vérifie si la cellule est contenue dans la liste de cellules
    :param cell: la cellule à regarder
    :param cell_list: la liste de cellules du joueur
    :return: True ou False selon le cas
    '''
    @staticmethod
    def __inCellList__(cell: Cell, cell_list: list):

        for i in range(len(cell_list)):
            if cell.getNum() == cell_list[i].getNum():
                return True
        return False

    '''
    fonction qui teste la victoire
    :return: True ou False selon le cas
    '''
    def __win__(self):
        px = self.__player[self.__player_turn].getPawn(0).getX()
        py = self.__player[self.__player_turn].getPawn(0).getY()
        p_type = self.__player[self.__player_turn].getPawnType()
        if self.__winLine__(px, py, p_type):
            return True
        elif self.__winSquare__(px, py, p_type):
            return True
        else:
            return False

    '''
    fonction qui teste si une victoire en ligne est détectée
    :param px: 
    :param py: 
    :param p_type: le numéro du joueur
    :return: 
    '''
    def __winLine__(self, px: int, py: int, p_type: chr):

        n = 0
        x = -1
        while x <= 1 and n == 0:
            y = -1
            while y <= 1 and n == 0:
                if not (x == 0 and y == 0):
                    if self.__board.verifCell(Cell(px + x, py + y), p_type):
                        n += 1
                        x_sol = x
                        y_sol = y
                y += 1
            x += 1
        if n != 0:
            m = 2
            for i in range(2):
                while self.__board.verifCell(Cell(px + (x_sol * m), py + (y_sol * m)), p_type):
                    n += 1
                    m += 1
                x_sol = -x_sol
                y_sol = -y_sol
                m = 1
            if n == 3:
                return True
        return False

    '''
    fonction qui teste si une victoire en ligne est détectée
    :param px: 
    :param py: 
    :param p_type: le numéro du joueur
    :return: 
    '''
    def __winSquare__(self, px: int, py: int, p_type: chr):
        n = 0
        x = -1
        y = -1
        while x <= 1 and n == 0:
            if self.__board.verifCell(Cell(px + x, py), p_type):
                n += 1
            else:
                x += 2
        while y <= 1 and n == 1:
            if self.__board.verifCell(Cell(px, py + y), p_type):
                n += 1
            else:
                y += 2
        if n == 2 and self.__board.verifCell(Cell(px + x, py + y), p_type):
            return True
        else:
            return False