class Heuristique:

    taille_mat = 5

    liste_allies_connus = []
    liste_ennemis_connus = []

    res_list = []

    list_amis = [] #propre à cette classe
    list_ennemis = [] #propre à cette classe

    def __init__(self, j1, j2, LAC, LEC):
        self.joueur1 = j1
        self.joueur2 = j2
        self.liste_allies_connus = LAC
        self.liste_ennemis_connus = LEC

    def HEURISTIQUE(self,matrice): # les alliés seront TOUJOURS les jetons de l'IA et les ennemis les jetons du JOUEUR ( ou de l'autre IA)

        idx = 0
        liste_pions_allies = self.recup_pos_pions(matrice,'IA')  # on récupère les positions des pions de l'ia

        holding = []  # liste qui stocke les alliés du pion initial

        while idx < len(liste_pions_allies):

            self.liste_allies_connus.clear()

            temp_coos = liste_pions_allies[idx]
            a = temp_coos[0]
            b = temp_coos[1]

            self.liste_allies_connus.append(liste_pions_allies[idx])

            temp_value = self.heuristique(temp_coos[0], temp_coos[1], a, b, 0, holding,matrice) # OK, NE PAS modifier!!

            if temp_value[0] == [liste_pions_allies[idx] ]: #pas d'alliés

                idx+=1 # on se place au jeton suivant pour voir s'il a des allies

            else:

                allie = temp_value[0]  # liste d'amis issue de l'heuristique
                ennemi = temp_value[1]  # liste d'ennemis issue de l'heuristique

                valeur_calculee = self.calculer_valeur_heuristique(a, b, allie, ennemi)
                self.liste_ennemis_connus.clear()

                return valeur_calculee

    def recup_pos_pions(self,matrice,player): # dans minmax, retourne la liste des pions du joueurdans le jeu actuel

        if player == 'IA':

            player_value = 'X'
        else:

            player_value = 'O'

        temp_list = []
        for i in range(0,self.taille_mat):
            for j in range(0,self.taille_mat):

                if matrice[i][j]==player_value :
                    temp_list.append ( (i,j) )
                #end IF
            #end FOR
        #end FOR
        return temp_list

    def heuristique(self,x,y,x_ref,y_ref,count,stocking,game):  # OK, ne pas y toucher !

        print('!!!début heuristique!!!')

        # amis
        self.calculer_position_amis(x,y,game,self.joueur1)
        self.update_liste_allies_connus(self.liste_allies_connus, self.list_amis)

        # ennemis cette fois ci
        self.calculer_position_amis(x,y,game,self.joueur2)
        self.update_liste_allies_connus(self.liste_ennemis_connus,self.list_ennemis)

        temp = self.list_amis
        self.save_original_list(count, temp,stocking)

        if stocking == []:
            stocking = temp

        if stocking != [] :

            for (i,j) in stocking:

                print('APPEL recursif HEURISTIQUE')
                self.heuristique(i, j,x_ref,y_ref,10,[],game)

            #end FOR

        else:

            print('plus d alliés autour')

        liste_generale = [(self.liste_allies_connus), (self.liste_ennemis_connus)]  # on mets les 2 listes ensemble pour pouvoir les return
        return liste_generale

    def calculer_position_amis(self,x,y,matrice,player): # calcule la position des jetons amis et ignore ceux déja comptabilisés -> dans l'heuristique

        if player == 'IA' :

            player_value = 'X'
        else :

            player_value = 'O'

        for i in range(x-1, x+2):

            if i < self.taille_mat:
                for j in range(y-1, y+2): # range s'arrête à (lim_haute - 1)

                    if j < self.taille_mat:

                        if i==x and j ==y: # position du jeton actuel
                            pass

                        elif matrice[i][j] == player_value and  (i>= 0 ) and  (j>= 0) :  # '.' = case vide  --> 'X' = ami( par rapport à l'IA)  'O' = ennemi ( autre joueur)

                            if player_value== 'X':  #cas où on appelle la fct pour les alliés
                                self.list_amis.append( (i, j) )

                            else: #cas où on appelle la fct pour les ennemis
                                self.list_ennemis.append( (i,j) )

                        #end ELIF
                    #end IF
                #end FOR
           #end FOR
        #end FOR

    def calculer_valeur_heuristique(self,x,y,l_allies,l_ennemis):

        # -> process propre au cas "carré"
        carre_haut_gauche = [(x,y),(x - 1, y - 1), (x - 1, y), (x, y - 1)]
        carre_haut_droit = [(x - 1, y), (x - 1, y + 1), (x, y + 1)]
        carre_bas_gauche = [(x, y - 1), (x + 1, y - 1), (x + 1, y)]
        carre_bas_droit = [(x, y + 1), (x + 1, y), (x + 1, y + 1)]

        if (l_allies == carre_haut_gauche) or (l_allies == carre_haut_droit) or (l_allies == carre_bas_gauche) or ( l_allies == carre_bas_droit):  # disposition en carré avec un coin étant (x,y) en paramètre
            value = 4
            return value
        # end IF

        print('les jetons ne sont pas disposés en carré')

        #lors de l'appel de ces fcts, on s'intéresse au deuxième élément retourné, à savoir le nombre d'elem sur la même orientation
        #proche de 4 -> valeur élevée
        #proche de 0 -> valeur faible

        val_allies = self.check_orientation_allies(l_allies) # return "H","V","DM" ou "DD" avec le nombre d'éléments associés à cette orientation
        orientation = val_allies[0]
        val_ennemis = self.check_ennemis(l_ennemis,orientation)

        if val_allies[1] ==4:
            return val_allies[1]

        elif val_ennemis == 4:
            return val_ennemis

        valeur = val_allies[1] - val_ennemis
        return valeur

    def check_ennemis(self,l_ennemis,orient):

        l_ennemis = sorted(l_ennemis)

        result = 0

        match orient:
            case 'H': #same X

                result = self.test_longueur_ennemis(l_ennemis,'H')

            case 'V' : #same Y

                result = self.test_longueur_ennemis(l_ennemis, 'V')

            case 'DM':

                result = self.sens_diagonale(l_ennemis, 'DM')

            case 'DD':

                result = self.sens_diagonale(l_ennemis, 'DD')

        #end MATCH

        return result

    def sens_diagonale(self,ennemis, statut):

        idx = 1
        liste_diago_montante = []
        liste_diago_descendante = []

        if statut == "DM":

            ennemis.sort(reverse=True) # on prends le + grand X en premier comme base de la diago, vu qu'elle doit remonter --> les X qui diminuent
            couple_init = ennemis[0]
            liste_diago_montante.append(couple_init)

            while idx < len(ennemis):

                temp_couple = ennemis[idx]

                if temp_couple[0] == 0:
                    break # useless de regarder plus loin, les autres couples ayant un X + petit

                if (temp_couple[0]<couple_init[0]) and (temp_couple[1]>couple_init[1]): # on se situe 1 au dessus et 1 à droite ?
                    liste_diago_montante.append(temp_couple)

                couple_init = temp_couple # comme la liste "ennemis" est trié dans l'ordre décroissant des x et y,  le couple qu'on observe actuellement la nouvelle reference
                #end IF

                idx+=1
            #end WHILE

            return(len(liste_diago_montante))

        else: #diago qui descends

            couple_init = ennemis[0]
            liste_diago_descendante.append(couple_init)

            while idx < len(ennemis):

                temp_couple = ennemis[idx]

                if temp_couple[0] == 4:
                    break  # useless de regarder plus loin, les autres couples ayant un X + grand

                if (temp_couple[0]-1 == couple_init[0]) and (temp_couple[1]-1 == couple_init[1]):  # on se situe 1 au dessus et 1 à droite ?
                    liste_diago_descendante.append(temp_couple)

                couple_init = temp_couple  # comme la liste "ennemis" est trié dans l'ordre décroissant des x et y,  le couple qu'on observe actuellement la nouvelle reference
                # end IF

                idx += 1
            # end WHILE
            return (len(liste_diago_descendante))

    def test_longueur_ennemis(self,ennemis, statut): # FONCTIONNE

        ennemis = sorted(ennemis)

        l_0 = []
        l_1 = []
        l_2 = []
        l_3 = []
        l_4 = []

        long0 = long1 = long2 = long3 = long4 = 0

        if statut == "H":

            for elem in ennemis:

                match elem[0]:
                    case 0:
                        l_0.append(elem)
                    case 1:
                        l_1.append(elem)
                    case 2:
                        l_2.append(elem)
                    case 3:
                        l_3.append(elem)
                    case 4:
                        l_4.append(elem)
                    case other:
                        pass
                # end MATCH

            liste_retenue = self.plus_longue_liste(l_0, l_1, l_2, l_3, l_4)
            return len(liste_retenue)
        else:

            for elem in ennemis:

                match elem[1]:
                    case 0:
                        l_0.append(elem)
                    case 1:
                        l_1.append(elem)
                    case 2:
                        l_2.append(elem)
                    case 3:
                        l_3.append(elem)
                    case 4:
                        l_4.append(elem)
                    case other:
                        pass
                # end MATCH

            liste_retenue = self.plus_longue_liste(l_0, l_1, l_2, l_3, l_4)
            return len(liste_retenue)

    def plus_longue_liste(self,liste1, liste2, liste3, liste4, liste5):

        # Créé une liste ayant comme éléments la longueur de chaque liste
        lengths = [len(liste1), len(liste2), len(liste3), len(liste4), len(liste5)]

        # cherche l'index de la + longue liste
        longest_index = lengths.index(max(lengths))

        # selon l'index, retourne la liste
        if longest_index == 0:
            return liste1
        elif longest_index == 1:
            return liste2
        elif longest_index == 2:
            return liste3
        elif longest_index == 3:
            return liste4
        elif longest_index == 4:
            return liste5

    def update_liste_allies_connus(self,liste_allies_connus, nouveaux_allies): #allie ou ennemis selon le besoin

        idx = 0

        while idx < len(liste_allies_connus):

            if liste_allies_connus[idx] in nouveaux_allies:
                nouveaux_allies.remove(liste_allies_connus[idx])
            # end IF

            idx += 1
        #end WHILE

        for elem in nouveaux_allies:# on ajoute les inconnus à la liste des connus
            liste_allies_connus.append(elem)
        #fin FOR

        #ici on retire des occurences ( s'il y en a)
        for elem in liste_allies_connus:
            while (liste_allies_connus.count(elem) > 1):
                liste_allies_connus.remove(elem)

    def save_original_list(self,n,list,stock): # utilisé dans la fct récursive "heuristique"

        if n==0: # 1ère passe dans la fonction
            for elem in list:
                stock.append(elem)

    def check_orientation_allies(self,l_allies): # retourne l'orientation ou se situe le maximum d'alliés

        idx = 1

        compteur_vertical= 1
        compteur_horizontal = 1
        compteur_diago_montante = 1
        compteur_diago_descendante = 1
        # on les fait tous = 1 car le couple initial de la liste est le jeton initial introduit dans "heuristique"

        liste_orientation_valeur = []

        couple_initial = l_allies[0] # => stockage du premier couple d'alliés ( = le x,y du jeton initial trouvé par "trouver_jeton")

        while idx < len(l_allies):
            temp_couple = l_allies[idx] #-> print un couple  et PAS un élément du couple

            #check horizontal ET vertical
            if temp_couple[0] == couple_initial[0]: # on check les x du couple (x,y) -> si les X pareils, alors sur la même ligne
                compteur_horizontal += 1

            elif temp_couple[1] == couple_initial[1]:# on check les y du couple (x,y) -> si les Y pareils, alors sur la même colonne
                compteur_vertical += 1
            # end IF

            if( (temp_couple[0]-1) == (couple_initial[0]) and (temp_couple[1]+1) == (couple_initial[1]) ) or (temp_couple[0]+1) == (couple_initial[0]) and (temp_couple[1]-1) == (couple_initial[1]) : #on check (x-1,y+1) ou (x+1,y-1)
                compteur_diago_montante +=1 # diagonale qui monte comme ca: "/"

            elif ( (temp_couple[0]-1) == (couple_initial[0]) and (temp_couple[1]-1) == (couple_initial[1]) ) or ( (temp_couple[0]+1)== (couple_initial[0]) and (temp_couple[1]+1) == (couple_initial[1] ) ):
               compteur_diago_descendante +=1 # diagonale qui descend comme ca: "\"
            #end IF

            couple_initial= temp_couple
            idx+=1
        #end WHILE

        if compteur_vertical > compteur_horizontal:

            liste_orientation_valeur.append("V")
            liste_orientation_valeur.append(compteur_vertical)
            return liste_orientation_valeur  # orientation retenue: verticale

        elif compteur_vertical < compteur_horizontal:

            liste_orientation_valeur.append("H")
            liste_orientation_valeur.append(compteur_horizontal)
            return liste_orientation_valeur # orientation retenue: horizontal

        # diagos
        elif compteur_diago_montante > compteur_diago_descendante:

            liste_orientation_valeur.append("DM")
            liste_orientation_valeur.append(compteur_diago_montante)
            return liste_orientation_valeur # orientation retenue: diago montante

        elif compteur_diago_montante < compteur_diago_descendante:

            liste_orientation_valeur.append("DD")
            liste_orientation_valeur.append(compteur_diago_descendante)
            return liste_orientation_valeur # orientation retenue: diago descendante

        elif compteur_vertical == compteur_horizontal:

            liste_orientation_valeur.append("H")
            liste_orientation_valeur.append(compteur_horizontal)
            return liste_orientation_valeur  # horizontal par défaut quand ils sont égaux

        else:

            liste_orientation_valeur.append("DM")
            liste_orientation_valeur.append(compteur_diago_montante)
            return liste_orientation_valeur # orientation retenue: diago montante par défaut
