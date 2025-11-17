# -*- coding: utf-8 -*-
"""
Created on Fri Oct 24 19:02:35 2025

@author: domdo
"""

import random
from cartes import Carte, Tete, Couleur

class Pioche:
    """Définit ce qu'est une pioche"""
    def __init__(self,nb_joueur):
        self.Pioche = []
        if nb_joueur==4:
            Joker = 2
        if nb_joueur==3:
            Joker = 1
        else:
            Joker = 0
        for i in range(1,11):
            for couleur in ['Carreau','Coeur','Trèfle','Pique']:
                self.Pioche.append(Carte(str(i),couleur))
        for i in range(Joker):
            self.Pioche.append(Carte("0",'Joker'))
               
        random.shuffle(self.Pioche)
        
    def Recup(self,ListeCartes):
        """Rajout de cartes dans la pioche à la suite de l'utilisation d'une carte coeur"""
        self.Pioche = self.Pioche + ListeCartes
        
    def AjoutTop(self,carte):
        """Rajout d'une carte au-dessus de la pioche (Si l'adversaire a été tué avec le nombre exact de dégats)"""
        self.Pioche = [carte] + self.Pioche
        
    def JoueurPioche(self,J):
        """Définit ce qu'il se passe pour la pioche quand un joueur pioche dedans"""
        if len(self.Pioche) != 0:
            J.AjouteCarte(self.Pioche[0])
            self.Pioche = self.Pioche[1:]
        else:
            pass
        
        
    def __str__(self):
        if self.Pioche == []:
            return "La Pioche est vide"
        s = ""
        for carte in self.Pioche:
            s = s + str(carte) + "\n"
        return s
    
    def __len__(self):
        return len(self.Pioche)
    
class Defausse:
    """Définit ce qu'est une Défausse"""
    def __init__(self):
        self.Defausse = []
        
    def AddDefausse(self,listeCartes):
        """Ajout de cartes de la défausse
        - Soit à la suite d'une défausse dû à l'attaque d'un joueur
        - Soit quand on vide les cartes jouées dans la défausse"""
        self.Defausse = listeCartes + self.Defausse
            
    def VideDefausse(self,n,deck):
        """Vide la défausse après qu'un joueur ait joué un pouvoir coeur"""
        nb_cartes = n
        if n > len(self.Defausse):
            nb_cartes = len(self.Defausse)
        
        Cartes_Recup = self.Defausse[nb_cartes:]
        Cartes_Recup.reverse()
        
        self.Defausse = self.Defausse[:nb_cartes]
        deck.Recup(Cartes_Recup)
        
        
    def __str__(self):
        if self.Defausse == []:
            return "La défausse est vide"
        s = ""
        for carte in self.Defausse:
            s = s + str(carte) + "\n"
        return s
    
    def __len__(self):
        return len(self.Defausse)
    
class ListeTete:
    """Définit ce qu'est la liste des adversaires"""
    def __init__(self):
        Valet,Dame,Roi = [],[],[]
        for couleur in ['d','c','t','p']:
            Valet.append(Tete("V", couleur, 10, 20, Couleur(couleur), True))
            Dame.append(Tete("D", couleur, 15, 30, Couleur(couleur), False))
            Roi.append(Tete("R", couleur, 20, 40, Couleur(couleur), False))
        random.shuffle(Valet) 
        random.shuffle(Dame)
        random.shuffle(Roi)
        self.liste = Valet + Dame + Roi
        
    def EstVide(self):
        """Teste si la liste est vide -> Condition de victoire"""
        return self.liste == []
    
    def EstToutInvisible(self):
        """Regarde si toutes les cartes sont invisibles"""
        Bool = True
        for tete in self.liste:
            if tete.visible:
                Bool = False
        return Bool
    
    def Revele4Cartes(self):
        """Révèle les 4 cartes suivantes.
        Est éxécuté si toutes les cartes sont invisibles"""
        if len(self.liste) != 0:
            for i in range(4):
                self.liste[i].DevientVisible()
            
    def Top(self):
        """Permet de sélectionner la carte du dessus de la liste = Adversaire courant"""
        if len(self.liste)==0:
            return None
        return self.liste[0]
    
    def TopVersPioche(self,deck):
        """Envoie la tête du haut vers la pioche
        Est éxéxuté quand l'adversaire actuel se prend des dégâts exacts"""
        Top = self.Top()
        self.liste = self.liste[1:]
        deck.AjoutTop(Top)
        
    def TopVersDefausse(self,defausse):
        """Envoie la tête du haut vers la défausse
        Est éxécuté quand l'adversaire actuel meurt sans prendre des dégâts exacts"""
        Top = self.Top()
        self.liste = self.liste[1:]
        defausse.AddDefausse([Top])
        
    def __str__(self):
        s = ""
        for tete in self.liste:
            if tete.visible:
                s += str(tete) + '\n'
        return s
    
class CartesJouees:
    """Définit ce qu'est l'ensemble des cartes jouées dans un tour"""
    def __init__(self):
        self.liste = []
        
    def AjoutCarte(self, combo):
        """Ajoute des cartes dans la liste"""
        l_carte = []
        for combi in combo:
            new_card = Carte(combi[:-1],combi[-1])
            l_carte.append(new_card)
        self.liste = self.liste + l_carte
        
    def Reset(self):
        """Remet la liste à zéro -> Pendant la fin du tour"""
        self.liste = []
        
    def __str__(self):
        s = ""
        for el in self.liste:
            s += str(el) + "\n"

        return s
