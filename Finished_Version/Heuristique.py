class Heuristique:

    def __init__(self, j1, j2, LPJ1, LPJ2):
        self.joueur1 = j1
        self.joueur2 = j2
        self.liste_pions_joueur1 = LPJ1
        self.liste_pions_joueur2 = LPJ2
        self.liste_positions_connus_joueur1 = []
        self.liste_positions_connus_joueur2 = []
        self.taille_mat = 5

#-----première heuristique-----

    '''
    renvoie la valeur du jeu actuel
    :param matrice: le jeu actuel
    :return: la valeur du jeu
    '''
    def HEURISTIQUE(self,matrice):
        valeur_calculee = 0
        valeur_calculee_j1 = 0
        valeur_calculee_j2 = 0

        liste_val_j1 = []
        liste_val_j2 = []

        idx_j1 = 0
        idx_j2 = 0

        # on récupère les positions des pions des 2 joueurs
        liste_pions_1er_joueur = self.recup_pos_pions(matrice, self.joueur1)  # on récupère les positions des pions du joueur1
        liste_pions_2eme_joueur = self.recup_pos_pions(matrice,self.joueur2)  # on récupère les positions des pions du joueur2

        holding = []  # liste qui stocke les alliés du pion initial

        while idx_j1 < len(liste_pions_1er_joueur):  # pour chaque pion

            self.liste_positions_connus_joueur1.clear()

            temp_coos_joueur1 = liste_pions_1er_joueur[idx_j1]
            x_ref_j1 = temp_coos_joueur1[0]
            y_ref_j1 = temp_coos_joueur1[1]

            self.liste_positions_connus_joueur1.append(temp_coos_joueur1)

            temp_value_j1 = self.heuristique(temp_coos_joueur1[0], temp_coos_joueur1[1], x_ref_j1, y_ref_j1, 0, holding,matrice, self.joueur1)

            if temp_value_j1 == temp_coos_joueur1:  # pas de jeton similaire autour

                idx_j1 += 1  # on se place au jeton suivant pour voir s'il y en a

            else:
                valeur_calculee_j1 = self.calculer_valeur_heuristique(x_ref_j1, x_ref_j1, temp_value_j1)
                idx_j1 += len(temp_value_j1)
                liste_val_j1.append(valeur_calculee_j1)

        while idx_j2 < len(liste_pions_2eme_joueur):

            self.liste_positions_connus_joueur2.clear()

            temp_coos_joueur2 = liste_pions_2eme_joueur[idx_j2]
            x_ref_j2 = temp_coos_joueur2[0]
            y_ref_j2 = temp_coos_joueur2[1]

            self.liste_positions_connus_joueur2.append(temp_coos_joueur2)

            temp_value_j2 = self.heuristique(temp_coos_joueur2[0], temp_coos_joueur2[1], x_ref_j2, y_ref_j2, 0, holding,matrice, self.joueur2)

            if temp_value_j2 == temp_coos_joueur2:  # pas de jeton similaire autour

                idx_j2 += 1  # on se place au jeton suivant pour voir s'il y en a

            else:

                valeur_calculee_j2 = self.calculer_valeur_heuristique(x_ref_j2, y_ref_j2, temp_value_j2)
                idx_j2 += len(temp_value_j2)
                liste_val_j2.append(valeur_calculee_j2)

        liste_val_j1.sort()
        valeur_calculee_j1 = liste_val_j1[-1]

        liste_val_j2.sort()
        valeur_calculee_j2 = liste_val_j2[-1]

        if valeur_calculee_j1 == 4:
            return -valeur_calculee_j1

        elif valeur_calculee_j2 == 4:
            return valeur_calculee_j2
        else:
            valeur_calculee = valeur_calculee_j2 - valeur_calculee_j1
            # IA - Joueur

        return valeur_calculee  # valeur du jeu actuel

    '''
    récupère la position de tous les pions du joueur
    :param matrice: le jeu actuel
    :param player: le joueur pour lequel onva chercher les pions
    :return: la liste des positions des pions
    '''
    def recup_pos_pions(self, matrice, player):  # dans minmax, retourne la liste des pions du joueurdans le jeu actuel

        if player == 'IA':

            player_value = 'O'
        else:

            player_value = 'X'

        temp_list = []
        for i in range(0, self.taille_mat):
            for j in range(0, self.taille_mat):

                if matrice[i][j] == player_value:
                    temp_list.append((i, j))

        return temp_list

    '''
    fonction récursive qui va chercher tous les pions du même type autour d'un pion initial
    :param x: la coordonnée x du pion actuel
    :param y: la coordonnée y du pion actuel
    :param x_ref: la coordonnée x du pion initialement examiné
    :param y_ref: la coordonnée y du pion initialement examiné
    :param count: un compteur qui vérifie le numéro de l'appel de la fonction
    :param stocking: le stockage des pions du même type du pion initial 
    :param game: le jeu actuel
    :param player: le joueur pour lequel on appelle la fonction
    :return: la liste des pions connexes du joueur
    '''
    def heuristique(self, x, y, x_ref, y_ref, count, stocking, game, player):  # OK, ne pas y toucher !

        positions = self.calculer_position_amis(x, y, game, player)

        if player == self.joueur1:  # 1er joueur
            self.update_liste_positions_connus(self.liste_positions_connus_joueur1, positions)

        else:  # 2ème joueur
            self.update_liste_positions_connus(self.liste_positions_connus_joueur2, positions)

        temp = positions
        self.save_original_list(count, temp, stocking)

        if positions != []:

            for (i, j) in positions:
                self.heuristique(i, j, x_ref, y_ref, 10, [], game, player)
        else:
            pass  # plus de "nouveaux" jetons autour

        if player == self.joueur1:  # 1er joueur
            liste_generale = self.liste_positions_connus_joueur1

        else:  # 2ème joueur
            liste_generale = self.liste_positions_connus_joueur2

        return liste_generale

    '''
    fonction qui cherche les pions du même type dans un rayon de 1 case autour d'un pion
    :param x: la coordonnée x du pion 
    :param y: la coordonnée y du pion 
    :param matrice: le jeu actuel
    :param player: le joueur pour lequel on appelle la fonction
    :return: la liste des pions du même type dans ce rayon
    '''
    def calculer_position_amis(self, x, y, matrice,player):

        liste_positions = []
        if player == 'IA':

            player_value = 'O'
        else:

            player_value = 'X'

        for i in range(x - 1, x + 2):

            if i < self.taille_mat:
                for j in range(y - 1, y + 2):

                    if j < self.taille_mat:

                        if i == x and j == y:  # position du jeton actuel
                            pass

                        elif matrice[i][j] == player_value and (i >= 0) and (j >= 0):
                                liste_positions.append((i, j))

        return liste_positions

    '''
    fonction qui s'occupe de calculer la valeur d'un joueur
    :param x: la coordonnée x du pion de référence
    :param y: la coordonnée y du pion de référence
    :param liste_positions: la liste des positions relatives aux pions du même type ( 'X' ou 'O' )
    :return: la valeur du jeu pour le joueur
    '''
    def calculer_valeur_heuristique(self, x, y, liste_positions):

        # -> process propre au cas "carré"
        carre_haut_gauche = [(x, y), (x - 1, y - 1), (x - 1, y), (x, y - 1)]
        carre_haut_droit = [(x, y), (x - 1, y), (x - 1, y + 1), (x, y + 1)]
        carre_bas_gauche = [(x, y), (x, y - 1), (x + 1, y - 1), (x + 1, y)]
        carre_bas_droit = [(x, y), (x, y + 1), (x + 1, y), (x + 1, y + 1)]

        if (liste_positions == carre_haut_gauche) or (liste_positions == carre_haut_droit) or (liste_positions == carre_bas_gauche) or ( liste_positions == carre_bas_droit):  # disposition en carré avec un coin étant (x,y) en paramètre
            value = 5
            return value

        # -> process propre aux "angles droits"
        AD_haut_gauche = [(x, y), (x - 1, y), (x, y - 1)]
        AD_haut_droit = [(x, y), (x - 1, y), (x, y + 1)]
        AD_bas_gauche = [(x, y), (x, y - 1), (x + 1, y)]
        AD_bas_droit = [(x, y), (x, y + 1), (x + 1, y)]

        temp = liste_positions[:-1]  # [:-1] => on retire le dernier élément avec la méthode de slicing

        if (temp == AD_haut_gauche) or (temp == AD_haut_droit) or (temp == AD_bas_gauche) or (temp == AD_bas_droit):  # disposition en carré avec un coin étant (x,y) en paramètre
            value = -5
            return value

        valeur = self.check_orientation_allies(liste_positions)
        return valeur

    '''
    fonction qui met à jour la liste des positions des pions déjà examinées 
    :param liste_positions_connus: la liste des positions déjà examinées
    :param nouveaux_allies: la liste des nouvelles positions qui n'ont pas encore été examinées
    :return: 'liste_positions_connus' avec les nouvelles positions non examinées 
    '''
    def update_liste_positions_connus(self, liste_positions_connus,nouveaux_allies):

        idx = 0

        while idx < len(liste_positions_connus):

            if liste_positions_connus[idx] in nouveaux_allies:
                nouveaux_allies.remove(liste_positions_connus[idx])
            idx += 1
        # end WHILE

        for elem in nouveaux_allies:  # on ajoute les inconnus à la liste des connus
            liste_positions_connus.append(elem)

        # ici on retire des occurences ( s'il y en a)
        for elem in liste_positions_connus:
            while (liste_positions_connus.count(elem) > 1):
                liste_positions_connus.remove(elem)

    '''
    sauvegarde une liste si on passe avec '0' comme numéro d'appel
    :param n: le numéro d'appel de la fonction
    :param list: la liste à stocker
    :param stock: le stock à remplir
    '''
    def save_original_list(self, n, list, stock):

        if n == 0:  # 1ère passe dans la fonction
            for elem in list:
                stock.append(elem)

    '''
    regarde comment sont orientés les pions du même type
    :param liste_positions: la liste des pions à examiner 
    :return: le nombre maximal de pions qu isont dans la même direction
    '''
    def check_orientation_allies(self, liste_positions):

        idx = 1

        compteur_carre = 0
        compteur_vertical = 1
        compteur_horizontal = 1
        compteur_diago_montante = 1
        compteur_diago_descendante = 1

        liste_orientation_valeur = []

        couple_initial = liste_positions[0]
        while idx < len(liste_positions):

            temp_couple = liste_positions[idx]
            # check horizontal ET vertical

            if temp_couple[0] == couple_initial[ 0]:
                compteur_horizontal += 1

            elif temp_couple[1] == couple_initial[1]:
                compteur_vertical += 1
            # end IF

            if ((temp_couple[0] - 1) == (couple_initial[0]) and (temp_couple[1] + 1) == (couple_initial[1])) or (temp_couple[0] + 1) == (couple_initial[0]) and (temp_couple[1] - 1) == (couple_initial[1]):  # on check (x-1,y+1) ou (x+1,y-1)
                compteur_diago_montante += 1  # diagonale qui monte comme ca: "/"

            elif ((temp_couple[0] - 1) == (couple_initial[0]) and (temp_couple[1] - 1) == (couple_initial[1])) or ((temp_couple[0] + 1) == (couple_initial[0]) and (temp_couple[1] + 1) == (couple_initial[1])):compteur_diago_descendante += 1  # diagonale qui descend comme ca: "\"

            # end IF

            couple_initial = temp_couple
            idx += 1
        # end WHILE

        liste_longueurs = [compteur_vertical, compteur_horizontal, compteur_diago_descendante, compteur_diago_montante]
        liste_longueurs.sort()

        return liste_longueurs[-1]

#-----deuxième heuristique-----

    '''
    deuxième heuristique basé sur des "poids"
    :param matrice: le jeu actuel
    :return: la valeur du jeu
    '''
    def HEURISTIQUE1(self, matrice):

        poids = [
            [0, 1, 0, 1, 0],
            [1, 2, 2, 2, 1],
            [0, 2, 3, 2, 0],
            [1, 2, 2, 2, 1],
            [0, 1, 0, 1, 0]
        ]
        heur_val = 0
        for x in range(5):
            for y in range(5):
                val_mat = self.valeur(matrice[x][y])
                if val_mat != 0:
                    heur_val = heur_val + val_mat * poids[x][y]
        return heur_val

    '''
    calcule la valeur selon le type du pion
    :param c: le pion ( 'X' , 'O' ou '.' )
    :return: la valeur
    '''
    def valeur(self, c: chr):

        if c == 'X':
            val = -1
        elif c == 'O':
            val = 1
        else:
            val = 0
        return val
