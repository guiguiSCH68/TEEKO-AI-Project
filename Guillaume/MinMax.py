from Heuristique import *

import copy

class MinMax:

    def __init__(self,j1,j2,LPA, LPE, LAC, LEC,matrice_jeu):
        self.joueur1 = j1
        self.joueur2 = j2
        self.liste_pions_allies = LPA
        self.liste_pions_ennemis = LPE
        self.liste_allies_connus = LAC
        self.liste_ennemis_connus = LEC
        self.taille_mat = 5
        self.res_list = []
        self.heuris = Heuristique(j1,j2,[],[]) #on instancie l'heuristique
        self.jeu_actuel = matrice_jeu
        self.coup_opti = []


    #regarder comment récupérer le coup opti... ( en dehoors de la fct hein)

    @staticmethod
    def get_jeu(matrice):
        return matrice

    def donner_coup_opti(self):
        return self.coup_opti

    def minmax_avec_alpha_beta(self,game_state, player_turn, depth,count_2,alpha,beta):

        if depth == 0: # noeud terminal de minmax ( on est au bout de l'arbre)

            #condition pour gagner/perdre

            check = self.heuris.HEURISTIQUE(game_state)

            if check == 4:
                return check

            elif check == -4:
                return check

            else:
                return check

        else:
            coup_opti = []
            stock_liste_pions_initial = []

            temp =self.liste_pions_allies
            self.heuris.save_original_list(count_2, temp, stock_liste_pions_initial)

            if player_turn == 'X': # on maximise l'IA  #MODIFICATION FAITE ICI

                game_state = copy.deepcopy(self.jeu_actuel) # on copie tel quel la matrice de jeu actuel (game_state)
                valeur_init = -10
                for pion in stock_liste_pions_initial : #--> définie lors du placement des pions. actualisée après chaque call du minmax pour le prochain coup ( contient les positions non modifiées ainsi que celle modifiée)

                    liste_depl = self.verifier_libre(pion[0], pion[1], game_state)

                    for deplacement in liste_depl : # res_list = liste des déplacements possibles autour DU jeton

                        changed_game = self.simuler_deplacement(game_state,pion,deplacement,player_turn)
                        valeur = self.MAX( self.minmax_avec_alpha_beta(changed_game, False, depth-1, 0,alpha,beta), valeur_init)
                        alpha = valeur
                        if valeur == valeur_init : # le coup actuel est - bien que le précédent
                            pass  # on récup pas le couple (pion, coos du déplacement du pion)
                        else:
                            coup_opti = self.get_coup_a_jouer(pion, deplacement)
                            

                        if alpha >= beta:
                            return alpha

                        game_state = copy.deepcopy(self.jeu_actuel) # on revient au jeu initial
                        valeur_init = valeur # on fait ca pour comparer la valeur suivante à l'actuelle MAX(), pour savoir si le prochain est mieux ou pas

                    liste_depl.clear()

                    #end FOR
                #end FOR

                return valeur_init


            else: # player turn = False --> joueur

                self.res_list.clear()
                valeur_init = 10  # --> remise à cette valeur lors de l'appel du minmax, useless de mettre ici du coup?
                save = copy.deepcopy(game_state)

                for pion in self.liste_pions_ennemis:  # --> définie lors du placement des pions. actualisée après chaque call du minmax pour le prochain coup ( contient les positions non modifiées ainsi que celle modifiée)
                    liste_depl2 = self.verifier_libre(pion[0], pion[1], game_state)

                    for deplacement in liste_depl2:  # res_list = liste des déplacements possibles autour DU jeton

                        changed_game1 = self.simuler_deplacement(game_state, pion, deplacement,player_turn)
                        valeur = self.MIN( self.minmax_avec_alpha_beta(changed_game1, 'T', depth - 1, 0,alpha, beta), valeur_init)
                        beta = valeur
                        if valeur == valeur_init:  # le coup actuel est - bien que le précédent
                            pass
                        if beta >= alpha:
                            return beta

                        game_state = copy.deepcopy(save)

                        valeur_init = valeur

                    liste_depl2.clear()
                    # end FOR

                # end FOR

                return valeur_init
        #end ELSE


    def MAX(self,valeur1, valeur2): # a modifier ( regarder precedent et actuel)

        if valeur1 >= valeur2:
            return valeur1
        else:
            return valeur2

    def MIN(self,valeur1, valeur2):  # a modifier ( regarder precedent et actuel)

        if valeur1 <= valeur2:
            return valeur1
        else:
            return valeur2

    def get_coup_a_jouer(self,pion, coos_deplacement):

        self.coup_opti = [ (pion), (coos_deplacement)]
        return self.coup_opti

    def simuler_deplacement(self,matrice, ancienne_coos, new_coos,player_turn):

        for i in range(0,self.taille_mat):
            for j in range(0, self.taille_mat):

                if (i,j) == ancienne_coos : # lorsqu'on arrive aux bonnes coordonnés
                    matrice[i][j] = '.' # on met la valeur de la case à 0, vu qu'on déplace, la case devient vide
                #end IF

                if (i,j) == new_coos:  # lorsqu'on arrive aux bonnes coordonnés

                    if player_turn == 'X': #en accord avec ce qu iest défini dans le minmax()
                        matrice[i][j] = 'X'  # on met la valeur de la case à 1, vu qu'on déplace, la case devient utilisée
                    else:

                        matrice[i][j] = 'O' #case utilisée pour l'ennemi
        return matrice

    def verifier_libre(self,x,y,game_state): # vérifie les positions libres autour d'un jeton et les place dans une liste -> dans minmax

        res_list = [] #liste des places libres

        for i in range(x-1, x+2):

             if i<self.taille_mat: # évite le dépassement d'indice
                 for j in range(y-1, y+2): # range s'arrête à (lim_haute - 1)

                     if j < self.taille_mat:

                        if i==x and j ==y:
                            pass
                        elif game_state[i][j] == '.' and ( (i>= 0) ) and ( (j>= 0) ):  # 0 = case vide

                            res_list.append( (i,j) )
                            #print(res_list)
                        #end ELIF
                     #end IF
                 #end FOR
             #end IF
        #end FOR

        return res_list
