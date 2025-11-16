# -*- coding: utf-8 -*-
"""
Created on Fri Oct 24 19:01:34 2025

@author: domdo
"""

from cartes import Carte

class Joueur:
    """Définit ce qu'est un joueur
    Un joueur a un numéro.
    Un joueur a une taille max de main qui dépend du nombre de joueur auquel on joue
    Un joueur a une main composé de cartes"""
    def __init__(self,numero,main,nb_joueur):
        self.numero = numero
        self.main = main
        self.taillemax = 9-nb_joueur
    
    def Pioche(self,deck):
        """Permet a un joueur de piocher dans la pioche"""
        if len(self.main)==self.taillemax:
            return False
        else:
            deck.JoueurPioche(self)
            return True
        
    def AjouteCarte(self,card):
        """Ajoute une carte à la main du joueur"""
        self.main.append(card)
        
    def JoueCartes(self,combo):
        """Supprime les cartes de la main du joueur, elles sont ajoutées à la liste CartesJouées"""
        for el in combo:
            Carte_A_Checker = Carte(el[:-1],el[-1])
            i = self.main.index(Carte_A_Checker)
            self.main.pop(i)
    def VerifDefense(self,Attq):
        """Permet de vérifier si le joueur peut survivre à une attaque
        Si non, condition pour le Game Over"""
        s = 0
        for carte in self.main:
            s+=carte.value()
        return (s >= Attq)
    def DefausseCarte(self,combo,defausse):
        """Permet au joueur de défausser un ensemble de carte et les ajouter à la défausse"""
        for el in combo:
            i = self.main.index(Carte(el[:-1],el[-1]))
            self.main.pop(i)
            defausse.AddDefausse([Carte(el[:-1],el[-1])])
            
            
    def __str__(self):
        s = f'Main du joueur {self.numero} : \n'
        for carte in self.main:
            s+= str(carte) + "\n"
        return s