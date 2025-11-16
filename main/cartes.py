# -*- coding: utf-8 -*-
"""
Created on Fri Oct 24 18:59:19 2025

Définit les principales mécaniques des cartes entre elles

@author: Fabien
"""


class Couleur:
    """Définit ce qu'est une couleur"""
    def __init__(self,couleur):
        dico = {"d":"Carreau", "c":"Coeur", "p":"Pique", "t":"Trèfle", "j":"Joker"}
        if couleur in dico.keys():
            self.couleur = dico[couleur]
        elif couleur in dico.values():
            self.couleur = couleur
        else:
            print("Erreur dans l'attribution de couleur")
            self.couleur = None
    def norm(self):
        """Normalisation des noms"""
        dico = {"Carreau":"d", "Coeur":"c", "Pique":"p", "Trèfle":"t", "Joker":"j"}
        return dico[self.couleur]
    def __str__(self):
        return self.couleur
    def __eq__(self,other):
        return self.couleur == other.couleur
    def __ne__(self,other):
        return not self.__eq__(other)
    
class Carte:
    """Définit ce qu'est une carte
    Une carte a une valeur et une couleur"""
    
    def __init__(self,valeur,couleur):
        self.valeur = valeur
        self.couleur = Couleur(couleur)
        
    def value(self):
        if self.valeur == 'R':
            return 20
        if self.valeur == 'D':
            return 15
        if self.valeur == 'V':
            return 10
        else:
            return int(self.valeur)
        
    def __str__(self):
        return f"{self.valeur} de " + str(self.couleur)
    def __eq__(self,other):
        if other == None:
            return False
        else:
            return (self.couleur == other.couleur) and (self.valeur == other.valeur)
        
class Tete(Carte):
    """Définit ce qu'est une tête. 
    Une tête est une carte qui a d'autres attribut.
    Notamment elle a une statistique d'Attq, de PVs. Elle a une immunité dépendant de sa couleur.
    Elle peut être visible ou non.
    Et enfin elle peut être une carte ou un adversaire (self.EstUneCarte)"""
    def __init__(self,valeur, couleur, Attq, PVs, Immu, visible):
        super(Tete, self).__init__(valeur,couleur)
        self.Attq = Attq
        self.PVs = PVs
        self.Immu = Immu
        self.visible = visible
        self.EstUneCarte = False
        
    def DevientVisible(self):
        """Rend la carte visible"""
        self.visible = True
        
    def PrendreDegats(self,n):
        """Inflige n dégats à la tête"""
        self.PVs = self.PVs-n
        
    def DiminueAttaque(self,n):
        """Diminue de n l'Attaque de la tête"""
        self.Attq = self.Attq - n
        if self.Attq < 0:
            self.Attq = 0
            
    def VerifieMort(self):
        """Vérifie si la carte est morte ou non"""
        return self.PVs<=0
    
    def DegatsExact(self):
        """Vérifier si la carte a exactement perdu le nombre de PVs ou non"""
        return self.PVs==0
        
    def __str__(self):
        s = super(Tete,self).__str__()
        s = s.replace("10","Valet").replace("15", "Dame").replace("20","Roi")
        if self.EstUneCarte:
            return s
        else:
            return s + f" Attq : {self.Attq}, PVs : {self.PVs}, Immunité : {self.Immu}"