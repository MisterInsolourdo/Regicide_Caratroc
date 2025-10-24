# -*- coding: utf-8 -*-
"""
Created on Fri Oct 24 08:58:15 2025

@author: Formation
"""

import random




class Carte:
    def __init__(self,valeur,couleur):
        self.valeur = valeur
        self.couleur = couleur
    def __str__(self):
        return f"{self.valeur} de " + str(self.couleur)
        
class Tete(Carte):
    def __init__(self,valeur, couleur, Attq, PVs, Immu, visible):
        super(Tete, self).__init__(valeur,couleur)
        self.Attq = Attq
        self.PVs = PVs
        self.Immu = Immu
        self.visible = visible
        
    def DevientVisible(self):
        self.visible = True
        
    def __str__(self):
        s = super(Tete,self).__str__()
        s = s.replace("10","Valet").replace("15", "Dame").replace("20","Roi")

        return s + f" Attq : {self.Attq}, PVs : {self.PVs}, Immunité : {self.Immu}"
        
class Couleur:
    def __init__(self,couleur):
        self.couleur = couleur
    def __str__(self):
        return self.couleur
        
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
            for couleur in [Couleur('Carreau'),Couleur('Coeur'),Couleur('Trèfle'),Couleur('Pique')]:
                self.Pioche.append(Carte(i,couleur))
        for i in range(Joker):
            self.Pioche.append(Carte(0,Couleur('Joker')))
               
        random.shuffle(self.Pioche)
        
    def Recup(self,ListeCartes):
        self.Pioche = self.Pioche + ListeCartes
        
    def JoueurPioche(self,J):
        J.AjouteCarte(self.Pioche[0])
        self.Pioche = self.Pioche[1:]
        
        
    def __str__(self):
        if self.Pioche == []:
            return "La Pioche est vide"
        s = ""
        for Carte in self.Pioche:
            s = s + str(Carte) + "\n"
        return s
       
class Defausse:
    def __init__(self):
        self.Defausse = []
        
    def AddDefausse(self,listeCartes):
        for Cartes in listeCartes:
            self.Defausse.append(Cartes)
            
    def VideDefausse(self,n,deck):
        nb_cartes = n
        if n > len(self.Defausse):
            nb_cartes = len(self.Defausse)
        Cartes_Recup = reversed(self.Defausse[-nb_cartes:])
        self.Defausse = self.Defausse[:-nb_cartes]
        deck.Recup(Cartes_Recup)
        
        
    def __str__(self):
        if self.Defausse == []:
            return "La défausse est vide"
        s = ""
        for Carte in self.Pioche:
            s = s + str(Carte) + "\n"
        return s
    
class Joueur:
    def __init__(self,numero,main,nb_joueur):
        self.numero = numero
        self.main = main
        self.taillemax = 9-nb_joueur
    
    def Pioche(self,deck):
        if len(self.main)==self.taillemax:
            return False
        else:
            deck.JoueurPioche(self)
            return True
        
    def AjouteCarte(self,card):
        self.main.append(card)
        
    def __str__(self):
        s = f'Main du joueur {self.numero} : '
        for carte in self.main:
            s+= str(carte) + ";"
        return s
                   
class ListeTete:
    def __init__(self):
        
        Valet,Dame,Roi = [],[],[]
        for couleur in [Couleur('Carreau'),Couleur('Coeur'),Couleur('Trèfle'),Couleur('Pique')]:
            Valet.append(Tete(10, couleur, 10, 20, couleur, True))
            Dame.append(Tete(15, couleur, 15, 30, couleur, False))
            Roi.append(Tete(20, couleur, 20, 40, couleur, False))
        
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
        for i in range(4):
            self.liste[i].DevientVisible()
        
    def __str__(self):
        s = ""
        for Tete in self.liste:
            if Tete.visible:
                s += str(Tete) + '\n'
            else:
                s += "*" + '\n'
        return s
    
class CartesJouees:
    def __init__(self):
        self.liste = []

class Plateau:
    def __init__(self,nb_joueur):
        self.Pioche = Pioche(nb_joueur)
        self.Defausse = Defausse()
        self.CartesJouees = CartesJouees()
        self.ListeTete = ListeTete()
        self.ListeJoueurs = [Joueur(i,[],nb_joueur) for i in range(nb_joueur)]
        self.Fin = False
        self.Win = False
        
    def BoucleDeJeu(self):
        self.PiocheInitiale()
        SaisieInvalide = True, 0
        NumJoueur = int(input("Sélectionner le joueur débutant la partie : "))
        JoueurActuel = self.ListeJoueurs[NumJoueur]
        while not self.Fin:
            if self.ListeTete.EstVide():
                self.Win = True
                self.Fin = True
            elif self.ListeTete.EstToutInvisible():
                self.ListeTete.Revele4Cartes()
            while SaisieInvalide[0]:
                print(self.ListeTete.liste[0])
                print(JoueurActuel)
                selection_carte = input("Sélectionner les cartes à jouer : ")
                print(selection_carte)
            
        
    def PiocheInitiale(self):
        for joueur in self.ListeJoueurs:
            for i in range(joueur.taillemax):
                joueur.Pioche(self.Pioche)
                
    def ComboValide(self):
        num = ['1','2','3','4','5','6','7','8','9','10','V','D','R']
        couleur = ['c','d','t','j','p']
                
    def __str__(self):
        s = ''
        for joueur in self.ListeJoueurs:
            s += str(joueur) + '\n'
        return s
        
        
if __name__ == "__main__":
    plat = Plateau(3)
    plat.BoucleDeJeu()
    