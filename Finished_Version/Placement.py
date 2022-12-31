import random


class Placement:

    def __init__(self):

        self.taille_mat = 5

    '''
    s'occupe du placement des pions de l'IA dans le jeu
    :param jeu_actuel: le plateau de jeu actuel, lors de l'appel de la fonction
    :param num_pion: le numéro du pion à placer ( de 1 à 4 )
    :param player: le joueur pour lequel on appelle la fonction, dans notre cas on notera 'O'  pour placer les pions 'O' de l'IA
    :return: la position où il faut placer le pion
    '''
    def placement_pion_dans_jeu(self, jeu_actuel, num_pion, player):

        if player == 'O':
            autre_player = 'X'
        else:
            autre_player = 'O'

        if num_pion == 1:

                liste_pos_occupee = self.determiner_prises(jeu_actuel, autre_player)  # on regarde où le 1er pion a été placé
                position = liste_pos_occupee[0]
                positions_potentielles = self.verifier_libre(position[0], position[1],jeu_actuel)  # donne les cases autour du pion qui a été placé
                pos_random = random.randint(0, (len(positions_potentielles) - 1))  # random sur les index 0 à "longueur de la liste-1"
                position_ou_placer = positions_potentielles[pos_random]

                return position_ou_placer  # on retourne le jeu avec le pion placé

        elif num_pion == 2:

                liste_pos_potentielles = []
                liste_pos_occupee = self.determiner_prises(jeu_actuel, autre_player)

                for occupe in liste_pos_occupee:  # on fait une liste de toutes les positions potentielles pour le pion 'O'
                    pos_potentielles = self.verifier_libre(occupe[0], occupe[1], jeu_actuel)
                    for elem in pos_potentielles:
                        liste_pos_potentielles.append(elem)

                liste_pos_potentielles = self.suppr_occurences(liste_pos_potentielles)  # on retire les occurences
                orient = self.get_orientation(liste_pos_occupee)  # on récup l'orientation
                position_ou_placer = self.process_orientation(orient, liste_pos_occupee, liste_pos_potentielles,2)

                #cas de la position déjà occupée
                liste_pos_occupee_O = self.determiner_prises(jeu_actuel, player)

                while position_ou_placer in liste_pos_occupee_O:

                    pos_random = random.randint(0, (len(liste_pos_potentielles) - 1) )
                    position_ou_placer = liste_pos_potentielles[pos_random]
                   

                # dépassement d'indices
                position_ou_placer = list(position_ou_placer) # on transforme le 'tuple' en liste

                if position_ou_placer[0] < 0:
                    position_ou_placer[0] = position_ou_placer[0] + 1

                elif position_ou_placer[0] > 4:
                    position_ou_placer[0] = position_ou_placer[0] - 1

                elif position_ou_placer[1] < 0:
                    position_ou_placer[1] = position_ou_placer[1] + 1

                elif position_ou_placer[1] > 4:
                    position_ou_placer[1] = position_ou_placer[1] - 1
                else:
                    pass
                return position_ou_placer

        elif num_pion == 3:

                liste_pos_potentielles = []
                liste_pos_occupeeX = self.determiner_prises(jeu_actuel, autre_player)

                for occupe in liste_pos_occupeeX:  # on fait une liste de toutes les positions potentielles pour le pion 'O'
                    pos_potentielles = self.verifier_libre(occupe[0], occupe[1], jeu_actuel)
                    for elem in pos_potentielles:
                        liste_pos_potentielles.append(elem)

                liste_pos_potentielles = self.suppr_occurences(liste_pos_potentielles)  # on retire les occurences

                orient = self.get_orientation(liste_pos_occupeeX)  # on récup l'orientation

                if orient != True:

                    position_ou_placer = self.process_orientation(orient, liste_pos_occupeeX, liste_pos_potentielles,3)  # on place,selon l'orientation, soit avant le début soit après la fin de la succession de pions 'X'
                    liste_pos_occupee_O = self.determiner_prises(jeu_actuel, player)

                    while position_ou_placer in liste_pos_occupee_O:  # si le pion veut se mettre sur une place deja prise on fait une placement aléatoire du coup

                        pos_random = random.randint(0, (len(liste_pos_potentielles) - 1))  # random sur les index 0 à "longueur de la liste-1"
                        position_ou_placer = liste_pos_potentielles[pos_random]
                        

                    position_ou_placer = list(position_ou_placer)
                    # dépassement d'indices
                    if position_ou_placer[0] < 0:
                        position_ou_placer[0] = position_ou_placer[0] + 1
                        position_ou_placer[1] = position_ou_placer[1] + 1

                    elif position_ou_placer[0] > 4:
                        position_ou_placer[0] = position_ou_placer[0] - 1
                        position_ou_placer[1] = position_ou_placer[1] - 1

                    elif position_ou_placer[1] < 0:
                        position_ou_placer[1] = position_ou_placer[1] + 1
                        position_ou_placer[0] = position_ou_placer[0] + 1

                    elif position_ou_placer[1] > 4:
                        position_ou_placer[1] = position_ou_placer[1] - 1
                        position_ou_placer[0] = position_ou_placer[0] + 1
                    else:
                        pass
                    return position_ou_placer

                elif orient == True:  # process en "angle droit"
                    position_ou_placer = self.process_angle_droit(liste_pos_occupeeX)

                    liste_pos_occupee_O = self.determiner_prises(jeu_actuel, player)

                    while position_ou_placer in liste_pos_occupee_O:  # si le pion veut se mettre sur une place deja prise on fait une placement aléatoire du coup

                        pos_random = random.randint(0, (len(liste_pos_potentielles) - 1))  # random sur les index 0 à "longueur de la liste-1"
                        position_ou_placer = liste_pos_potentielles[pos_random]
                    return position_ou_placer

        elif num_pion == 4:

                idx = 0
                liste_pos_potentielles = []
                liste_pos_occupee = self.determiner_prises(jeu_actuel, autre_player)

                for occupe in liste_pos_occupee:  # on fait une liste de toutes les positions potentielles pour le pion 'O'
                    pos_potentielles = self.verifier_libre(occupe[0], occupe[1], jeu_actuel)
                    for elem in pos_potentielles:
                        liste_pos_potentielles.append(elem)

                liste_pos_potentielles = self.suppr_occurences(liste_pos_potentielles)  # on retire les occurences
                '''
                while idx < len(liste_pos_occupee):
                    temp_liste = liste_pos_occupee
                    print("temp",temp_liste)
                    temp_liste.remove(liste_pos_occupee[idx])
                    
                    orient = self.get_orientation(temp_liste)
                    print("orient",orient)

                    if orient == True:  # angle  droit détecté
                        position_ou_placer = self.process_angle_droit(temp_liste)
                        print("la",position_ou_placer)
                        return position_ou_placer
                    else:
                        idx += 1
                '''
                # si aucun angle droit trouvé à la fin, placer de façon random
                pos_random = random.randint(0, (len(liste_pos_potentielles) - 1))  # random sur les index 0 à "longueur de la liste-1"
                position_ou_placer = liste_pos_potentielles[pos_random]
                print("ici",position_ou_placer)
                return position_ou_placer  # on retourne le jeu avec le pion placé
        else:
            pass



    '''
    retourne l'orientation d'une liste de pions
    :param liste_positions: la liste  des positions, dans notre cas, des pions 'X' de l'humain
    :return: l'orientation ( H,V,DM,DD ou 'True' lorsque l'on est dans une configuration dite "d'angle droit")
    '''
    def get_orientation(self, liste_positions):

        idx = 1
        compteur_vertical = 1
        compteur_horizontal = 1
        compteur_diago_montante = 1
        compteur_diago_descendante = 1

        angle_droit = False

        liste_orientation_valeur = []

        couple_initial = liste_positions[0]
        while idx < len(liste_positions):
            temp_couple = liste_positions[idx]

            # check horizontal ET vertical
            if temp_couple[0] == couple_initial[0]:
                compteur_horizontal += 1
            elif temp_couple[1] == couple_initial[1]:
                compteur_vertical += 1
            # end IF

            if ((temp_couple[0] - 1) == (couple_initial[0]) and (temp_couple[1] + 1) == (couple_initial[1])) or (temp_couple[0] + 1) == (couple_initial[0]) and (temp_couple[1] - 1) == (couple_initial[1]):  # on check (x-1,y+1) ou (x+1,y-1)
                compteur_diago_montante += 1  # diagonale qui monte comme ca: "/"

            elif ((temp_couple[0] - 1) == (couple_initial[0]) and (temp_couple[1] - 1) == (couple_initial[1])) or ((temp_couple[0] + 1) == (couple_initial[0]) and (temp_couple[1] + 1) == (couple_initial[1])):
                compteur_diago_descendante += 1  # diagonale qui descend comme ca: "\"
            # end IF

            couple_initial = temp_couple
            idx += 1
        # end WHILE

        liste_compteurs = [compteur_vertical, compteur_horizontal, compteur_diago_montante, compteur_diago_descendante]
        liste_orientations = ['V', 'H', 'DM', 'DD']
        print(liste_compteurs)
        check = max(liste_compteurs)
        idx_liste = liste_compteurs.index(check)
        orient = liste_orientations[idx_liste]

        if compteur_vertical == compteur_horizontal and compteur_vertical >= 2:
            angle_droit = True
            return angle_droit

        return orient

    '''
    donne la position de placement du pion selon l'orientation des pions de l'autre joueur
    :param orient: l'orientation retournée par 'get_orientation()
    :param liste_pos_occupee: liste des positions des pions 'X'
    :param liste_potentielles: liste des positions potentielles pour le pion 'O'
    :param num_passage: le numéro du pion à placer
    :return: la position où placer le pion
    '''
    def process_orientation(self, orient, liste_pos_occupee, liste_potentielles, num_passage):

        if orient == 'H':
            # on met à gauche ou a droite
            ou_placer = random.randint(0, 1)

            pion_ref_g = liste_pos_occupee[0]  # 1er élément
            coos_placement_g = (pion_ref_g[0], pion_ref_g[1] - 1)

            pion_ref_d = liste_pos_occupee[-1]  # dernier élément
            coos_placement_d = (pion_ref_d[0], pion_ref_d[1] + 1)

            if num_passage == 2:
                if ou_placer == 0 and (coos_placement_g in liste_potentielles):
                    return coos_placement_g
                elif ou_placer == 1 and (coos_placement_d in liste_potentielles):
                    return coos_placement_d
                else:
                    return liste_potentielles[0]  # on prends la 1ère position trouvée car les 2 autres proposées ne vont pas
            else:
                if coos_placement_g != '.':
                    return coos_placement_d
                elif coos_placement_d != '.':
                    return coos_placement_g
                else:
                    pass

        elif orient == 'V':
            # au dessus ou en dessous
            ou_placer = random.randint(0, 1)

            pion_ref_h = liste_pos_occupee[0]  # 1er élément
            coos_placement_h = (pion_ref_h[0] - 1, pion_ref_h[1])

            pion_ref_b = liste_pos_occupee[-1]  # dernier élément
            coos_placement_b = (pion_ref_b[0] + 1, pion_ref_b[1])

            if num_passage == 2:
                if ou_placer == 0 and (coos_placement_h in liste_potentielles):
                    return coos_placement_h
                elif ou_placer == 1 and (coos_placement_b in liste_potentielles):
                    return coos_placement_b
                else:
                    return liste_potentielles[0]  # on prends la 1ère position trouvée car les 2 autres proposées ne vont pas
            else:
                if coos_placement_h != '.':
                    return coos_placement_b
                elif coos_placement_b != '.':
                    return coos_placement_h
                else:
                    pass

        elif orient == 'DM':
            # haut droit ou bas gauche
            ou_placer = random.randint(0, 1)

            pion_ref_hd = liste_pos_occupee[0]  # 1er élément
            coos_placement_hd = (pion_ref_hd[0] - 1, pion_ref_hd[1] + 1)

            pion_ref_bg = liste_pos_occupee[-1]  # dernier élément
            coos_placement_bg = (pion_ref_bg[0] + 1, pion_ref_bg[1] - 1)

            if num_passage == 2:
                if ou_placer == 0 and (coos_placement_hd in liste_potentielles):
                    return coos_placement_hd
                elif ou_placer == 1 and (coos_placement_bg in liste_potentielles):
                    return coos_placement_bg
                else:
                    return liste_potentielles[0]  # on prends la 1ère position trouvée car les 2 autres proposées ne vont pas
            else:
                if coos_placement_hd != '.':
                    return coos_placement_bg
                elif coos_placement_bg != '.':
                    return coos_placement_hd
                else:
                    pass
        else:  # DD
            # haut gauche ou bas droit
            ou_placer = random.randint(0, 1)

            pion_ref_hg = liste_pos_occupee[0]  # 1er élément
            coos_placement_hg = (pion_ref_hg[0] - 1, pion_ref_hg[1] - 1)

            pion_ref_bd = liste_pos_occupee[-1]  # 1er élément
            coos_placement_bd = (pion_ref_bd[0] + 1, pion_ref_bd[1] + 1)

            if num_passage == 2:
                if ou_placer == 0 and (coos_placement_hg in liste_potentielles):
                    return coos_placement_hg
                elif ou_placer == 1 and (coos_placement_bd in liste_potentielles):
                    return coos_placement_bd
                else:
                    return liste_potentielles[0]  # on prends la 1ère position trouvée car les 2 autres proposées ne vont pas
            else:
                if coos_placement_hg != '.':
                    return coos_placement_bd
                elif coos_placement_bd != '.':
                    return coos_placement_hg
                else:
                    pass

    '''
    s'occupe de donner la position manquante pour terminer une disposition en carré
    :param liste_positions: la liste des positions qui contiennent un 'X' ( pion humain)
    :return: les coordonnées manquantes pour finir le carré
    '''
    def process_angle_droit(self, liste_positions):

        couple_init = liste_positions[0]  # 1er élem
        x = couple_init[0]
        y = couple_init[1]

        AD_haut_gauche1 = [(x, y), (x - 1, y), (x, y - 1)]  # _|
        AD_haut_gauche2 = [(x, y), (x - 1, y - 1), (x - 1, y)]  #
        AD_haut_gauche3 = [(x, y), (x - 1, y - 1), (x, y - 1)]  # |_

        AD_haut_droit1 = [(x, y), (x - 1, y), (x, y + 1)]  # |_
        AD_haut_droit2 = [(x, y), (x - 1, y), (x - 1, y + 1)]
        AD_haut_droit3 = [(x, y), (x - 1, y + 1), (x, y + 1)]

        AD_bas_gauche1 = [(x, y), (x, y - 1), (x + 1, y)]
        AD_bas_gauche2 = [(x, y), (x, y - 1), (x + 1, y - 1)]
        AD_bas_gauche3 = [(x, y), (x + 1, y), (x + 1, y - 1)]

        AD_bas_droit1 = [(x, y), (x, y + 1), (x + 1, y)]
        AD_bas_droit2 = [(x, y), (x, y + 1), (x + 1, y + 1)]
        AD_bas_droit3 = [(x, y), (x + 1, y), (x + 1, y + 1)]

        idx = 0
        if liste_positions == AD_haut_gauche1:
            coos_manquante_AD_haut_gauche = (x - 1, y - 1)
            return coos_manquante_AD_haut_gauche

        elif liste_positions == AD_haut_gauche2:
            coos_manquante_AD_haut_gauche = (x, y - 1)
            return coos_manquante_AD_haut_gauche

        elif liste_positions == AD_haut_gauche3:
            coos_manquante_AD_haut_gauche = (x - 1, y)
            return coos_manquante_AD_haut_gauche

        elif liste_positions == AD_haut_droit1:
            coos_manquante_AD_haut_droit = (x - 1, y + 1)
            return coos_manquante_AD_haut_droit

        elif liste_positions == AD_haut_droit2:
            coos_manquante_AD_haut_droit = (x, y + 1)
            return coos_manquante_AD_haut_droit

        elif liste_positions == AD_haut_droit3:
            coos_manquante_AD_haut_droit = (x - 1, y)
            return coos_manquante_AD_haut_droit

        elif liste_positions == AD_bas_gauche1:
            coos_manquante_AD_bas_gauche = (x + 1, y - 1)
            return coos_manquante_AD_bas_gauche

        elif liste_positions == AD_bas_gauche2:
            coos_manquante_AD_bas_gauche = (x + 1, y)
            return coos_manquante_AD_bas_gauche

        elif liste_positions == AD_bas_gauche3:
            coos_manquante_AD_bas_gauche = (x, y - 1)
            return coos_manquante_AD_bas_gauche

        elif liste_positions == AD_bas_droit1:
            coos_manquante_AD_bas_droit = (x + 1, y + 1)
            return coos_manquante_AD_bas_droit

        elif liste_positions == AD_bas_droit2:
            coos_manquante_AD_bas_droit = (x + 1, y)
            return coos_manquante_AD_bas_droit

        elif liste_positions == AD_bas_droit3:
            coos_manquante_AD_bas_droit = (x, y + 1)
            return coos_manquante_AD_bas_droit
        else:
            pass

    '''
    supprime les occurences d'une liste de coordonnées
    :param liste: une liste contenant des coordonnées 
    :return: la liste sans multiples occurences de même coordonnées
    '''
    def suppr_occurences(self, liste):

        idx = 0

        while idx < len(liste):

            for elem in liste:

                while liste.count(elem) > 1:
                    liste.remove(elem)

            idx += 1

        return liste

    '''
    détermine les positions occupées par le joueur dans le jeu
    :param game_state: le plateau de jeu
    :param autre_player: l'autre joueur par rapport à l'ia, on regarde les 'X' dans notre cas
    :return: la liste des positions occupées par un 'X'
    '''
    def determiner_prises(self, game_state, autre_player):

        pos_prises = []

        for i in range(0, self.taille_mat):
            for j in range(0, self.taille_mat):
                if game_state[i][j] == autre_player:
                    pos_prises.append((i, j))
        return pos_prises

    '''
    vérfie les positions disponibles autour d'un pion
    :param x: la coordonnée x du pion 'X'
    :param y: la coordonnée y du pion 'X'
    :param game_state: le plateau de jeu actuel
    :return: la liste des positions libres autour du pon 'X'
    '''
    def verifier_libre(self, x, y, game_state):

        res_list = []  # liste des places libres

        for i in range(x - 1, x + 2):

            if i < self.taille_mat:  # évite le dépassement d'indice
                for j in range(y - 1, y + 2):  # range s'arrête à (lim_haute - 1)

                    if j < self.taille_mat:

                        if i == x and j == y:
                            pass
                        elif game_state[i][j] == '.' and ((i >= 0)) and ((j >= 0)):  # 0 = case vide

                            res_list.append((i, j))
                            # print(res_list)
                        # end ELIF
                    # end IF
                # end FOR
            # end IF
        # end FOR

        return res_list

