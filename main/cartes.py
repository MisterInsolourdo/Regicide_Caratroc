# -*- coding: utf-8 -*-
"""
Created on Fri Oct 24 18:59:19 2025

Définit les principales mécaniques des cartes entre elles

@author: Fabien
"""


class Couleur:
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
        dico = {"Carreau":"d", "Coeur":"c", "Pique":"p", "Trèfle":"t", "Joker":"j"}
        return dico[self.couleur]
    def __str__(self):
        return self.couleur
    def __eq__(self,other):
        return self.couleur == other.couleur
    def __ne__(self,other):
        return not self.__eq__(other)
    
class Carte:
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
    def __init__(self,valeur, couleur, Attq, PVs, Immu, visible):
        super(Tete, self).__init__(valeur,couleur)
        self.Attq = Attq
        self.PVs = PVs
        self.Immu = Immu
        self.visible = visible
        self.EstUneCarte = False
        
    def DevientVisible(self):
        self.visible = True
        
    def PrendreDegats(self,n):
        self.PVs = self.PVs-n
        
    def DiminueAttaque(self,n):
        self.Attq = self.Attq - n
        if self.Attq < 0:
            self.Attq = 0
            
    def VerifieMort(self):
        return self.PVs<=0
    
    def DegatsExact(self):
        return self.PVs==0
        
    def __str__(self):
        s = super(Tete,self).__str__()
        s = s.replace("10","Valet").replace("15", "Dame").replace("20","Roi")
        if self.EstUneCarte:
            return s
        else:
            return s + f" Attq : {self.Attq}, PVs : {self.PVs}, Immunité : {self.Immu}"