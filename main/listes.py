# -*- coding: utf-8 -*-
"""
Created on Fri Oct 24 19:02:35 2025

@author: domdo
"""

import random
from cartes import Carte, Tete, Couleur

class Pioche:
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
        self.Pioche = self.Pioche + ListeCartes
        
    def AjoutTop(self,carte):
        self.Pioche = [carte] + self.Pioche
        
    def JoueurPioche(self,J):
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
    def __init__(self):
        self.Defausse = []
        
    def AddDefausse(self,listeCartes):
        self.Defausse = listeCartes + self.Defausse
            
    def VideDefausse(self,n,deck):
        nb_cartes = n
        if n > len(self.Defausse):
            nb_cartes = len(self.Defausse)
        
        Cartes_Recup = self.Defausse[:nb_cartes]
        Cartes_Recup.reverse()
        
        self.Defausse = self.Defausse[nb_cartes:]
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
        return self.liste == []
    
    def EstToutInvisible(self):
        Bool = True
        for tete in self.liste:
            if tete.visible:
                Bool = False
        return Bool
    
    def Revele4Cartes(self):
        if len(self.liste) != 0:
            for i in range(4):
                self.liste[i].DevientVisible()
            
    def Top(self):
        if len(self.liste)==0:
            return None
        return self.liste[0]
    
    def TopVersPioche(self,deck):
        Top = self.Top()
        self.liste = self.liste[1:]
        deck.AjoutTop(Top)
        
    def TopVersDefausse(self,defausse):
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
    def __init__(self):
        self.liste = []
    def AjoutCarte(self, combo):
        l_carte = []
        for combi in combo:
            new_card = Carte(combi[:-1],combi[-1])
            l_carte.append(new_card)
        self.liste = self.liste + l_carte
        
    def Reset(self):
        self.liste = []
    def __str__(self):
        s = ""
        for el in self.liste:
            s += str(el) + "\n"
        return s