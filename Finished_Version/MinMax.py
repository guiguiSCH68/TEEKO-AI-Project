from Heuristique import *
import copy

class MinMax:

    def __init__(self, j1, j2, LPIA, LPHUM, matrice_jeu):

        self.liste_pions_IA = LPIA
        self.liste_pions_HUM = LPHUM
        self.taille_mat = 5
        self.heuris = Heuristique(j1, j2, [], [])  # on instancie l'heuristique
        self.jeu_actuel = matrice_jeu
        self.coup_opti = []

    '''
    renvoie le coup optimal à l'issue du minmax()
    :return: le coup optimal
    '''
    def donner_coup_opti(self):
        return self.coup_opti

    '''
    algorithme minmax qui détermine le coup optimal pour l'IA
    :param game_state: le jeu actuel
    :param player_turn: le joueur pour lequel on appelle la fonction ('X' ou 'O')
    :param depth: la profondeur
    :return: la valeur du minmax
    '''
    def minmax(self, game_state, player_turn, depth):

        if depth == 0:  # noeud terminal de minmax ( on est au bout de l'arbre)

            check = self.heuris.HEURISTIQUE(game_state)

            if check == None:
                check = 0
            return check

        else:

            if player_turn == 'O':  # on maximise l'IA

                game_state = copy.deepcopy(self.jeu_actuel)  # on copie tel quel la matrice de jeu actuel (game_state)
                valeur_init = -10
                for pion in self.liste_pions_IA:
                    liste_depl = self.verifier_libre(pion[0], pion[1], game_state)

                    for deplacement in liste_depl:
                        changed_game = self.simuler_deplacement(game_state, pion, deplacement, player_turn)
                        valeur = self.MAX(self.minmax(changed_game, 'X', depth - 1), valeur_init)

                        if valeur <= valeur_init:  # le coup actuel est - bien que le précédent
                            pass  # on récup pas le couple (pion, coos du déplacement du pion)
                        else:
                            self.get_coup_a_jouer(pion, deplacement)

                        game_state = copy.deepcopy(self.jeu_actuel)  # on revient au jeu initial
                        valeur_init = valeur
                    liste_depl.clear()

                return valeur_init

            else:  # player turn = False --> joueur

                valeur_init = 10  #
                save = copy.deepcopy(game_state)

                for pion in self.liste_pions_HUM:
                    liste_depl2 = self.verifier_libre(pion[0], pion[1], game_state)

                    for deplacement in liste_depl2:  # res_list = liste des déplacements possibles autour DU jeton

                        changed_game1 = self.simuler_deplacement(game_state, pion, deplacement, player_turn)
                        valeur = self.MIN(self.minmax(changed_game1, 'O', depth - 1), valeur_init)

                        if valeur == valeur_init:  # le coup actuel est - bien que le précédent
                            pass

                        game_state = copy.deepcopy(save)
                        valeur_init = valeur

                    liste_depl2.clear()

                return valeur_init
        # end ELSE

    '''
    algorithme minmax qui détermine le coup optimal pour l'IA avec un élagage alpha-beta
    :param game_state: le jeu actuel
    :param player_turn: le joueur pour lequel on appelle la fonction ('X' ou 'O')
    :param depth: la profondeur
    :param alpha: la valeur alpha de l'élagage
    :param beta: la valeur beta de l'élagage
    :param type_heuristique: le type de l'heuristique retenue selon la difficulté choisie
    :return: 
    '''
    def minmax_avec_alpha_beta(self, game_state, player_turn, depth, alpha, beta, type_heuristique):

        if depth == 0:  # noeud terminal de minmax ( on est au bout de l'arbre)

            if type_heuristique == 1:

                check = self.heuris.HEURISTIQUE1(game_state)
            else:
                check = self.heuris.HEURISTIQUE(game_state)

            if check == None:
                check = 0
            return check

        else:

            if player_turn == 'O':  # on maximise l'IA

                game_state = copy.deepcopy(self.jeu_actuel)  # on copie tel quel la matrice de jeu actuel (game_state)
                valeur_init = -10
                for pion in self.liste_pions_IA:
                    liste_depl = self.verifier_libre(pion[0], pion[1], game_state)

                    for deplacement in liste_depl:
                        changed_game = self.simuler_deplacement(game_state, pion, deplacement, player_turn)
                        valeur = self.MAX( self.minmax_avec_alpha_beta(changed_game, 'X', depth - 1, alpha, beta, type_heuristique),valeur_init)
                        alpha = valeur

                        if valeur == valeur_init:  # le coup actuel est - bien que le précédent
                            pass  # on récup pas le couple (pion, coos du déplacement du pion)
                        else:
                            self.get_coup_a_jouer(pion, deplacement)

                        if alpha >= beta:
                            return alpha

                        game_state = copy.deepcopy(self.jeu_actuel)  # on revient au jeu initial
                        valeur_init = valeur

                    liste_depl.clear()

                return valeur_init

            else:  # player turn = False --> joueur

                valeur_init = 10
                save = copy.deepcopy(game_state)

                for pion in self.liste_pions_HUM:
                    liste_depl2 = self.verifier_libre(pion[0], pion[1], game_state)

                    for deplacement in liste_depl2:
                        changed_game1 = self.simuler_deplacement(game_state, pion, deplacement, player_turn)
                        valeur = self.MIN(self.minmax_avec_alpha_beta(changed_game1, 'O', depth - 1, alpha, beta, type_heuristique),valeur_init)
                        beta = valeur

                        if valeur == valeur_init:  # le coup actuel est - bien que le précédent
                            pass
                        if beta >= alpha:
                            return beta

                        game_state = copy.deepcopy(save)
                        valeur_init = valeur

                    liste_depl2.clear()

                return valeur_init
        # end ELSE

    '''
    calcule le max entre 2 valeurs
    :param valeur1: la 1ère valeur à comparer
    :param valeur2: la 2ème valeur à comparer
    :return: 
    '''
    def MAX(self, valeur1, valeur2):

        if valeur1 == None:
            valeur1 = 0

        elif valeur2 == None:
            valeur2 = 0

        if valeur1 >= valeur2:
            return valeur1
        else:
            return valeur2

    '''
    calcule le max entre 2 valeurs
    :param valeur1: la 1ère valeur à comparer
    :param valeur2: la 2ème valeur à comparer
    :return: 
    '''
    def MIN(self, valeur1, valeur2):  # a modifier ( regarder precedent et actuel)

        if valeur1 == None:
            valeur1 = 0

        elif valeur2 == None:
            valeur2 = 0

        if valeur1 <= valeur2:
            return valeur1
        else:
            return valeur2

    '''
    récupère le coup optimal lorsqu'elle est appellée
    :param pion: le pion à récupérer
    :param coos_deplacement: où déplacer ce pion
    :return: le coup otpimal
    '''
    def get_coup_a_jouer(self, pion, coos_deplacement):

        self.coup_opti = [(pion), (coos_deplacement)]
        return self.coup_opti

    '''
    simule le déplacement au sein du minmax
    :param matrice: le jeu à considérer
    :param ancienne_coos: les anciennes coordonnées du pion
    :param new_coos: nouvelles coordonnées où placer le pion
    :param player_turn: le joueur pour lequel on appelle la fonction ('X' ou 'O')
    :return: le jeu modifié avec le pion déplacé
    '''
    def simuler_deplacement(self, matrice, ancienne_coos, new_coos, player_turn):

        for i in range(0, self.taille_mat):
            for j in range(0, self.taille_mat):

                if (i, j) == ancienne_coos:
                    matrice[i][j] = '.'
                if (i, j) == new_coos:

                    if player_turn == 'O':
                        matrice[i][j] = 'O'
                    else:

                        matrice[i][j] = 'X'
        return matrice

    '''
    vérfie les positions disponibles autour d'un pion
    :param x: la coordonnée x du pion 'X'
    :param y: la coordonnée y du pion 'X'
    :param game_state: le plateau de jeu actuel
    :return: la liste des positions libres autour du pon 'X'
    '''
    def verifier_libre(self, x, y,game_state):

        res_list = []  # liste des places libres

        for i in range(x - 1, x + 2):

            if i < self.taille_mat:  # évite le dépassement d'indice
                for j in range(y - 1, y + 2):

                    if j < self.taille_mat:

                        if i == x and j == y:
                            pass
                        elif game_state[i][j] == '.' and ((i >= 0)) and ((j >= 0)):

                            res_list.append((i, j))
        return res_list
