# -*- coding: utf-8 -*-
"""
Created on Mon Nov  3 11:03:25 2025

@author: domdo
"""

#Import externe
from PyQt5.QtWidgets import QLabel, QPushButton

"""Cette librairie définit des surcharges de QLabel ou QPushButton et ce
afin de gérer l'intéractivité de l'utilisateur avec l'UI
Pour ce faire chacune des classes est définie relativement à une fenêtre de plateau de Jeu"""


class QLabel_Carte(QLabel):
    def __init__(self,MainWindow):
        super().__init__(MainWindow)
        self.activate = False
        self.Window = MainWindow
        self.Card = None


    def mousePressEvent(self, ev):
        if self.Card == None:
            pass
        else:
            if self.activate == False:
                self.activate = True
                self.setStyleSheet("border: 5px solid red;")
                self.Window.Selection.append(self.Card)
            else:
                self.setStyleSheet("")
                self.activate = False
                self.Window.Selection.remove(self.Card)
        print(self.Window.Selection)
            
    def set_Card(self,Carte,IsCard=True):
        if IsCard == True:
            self.Card = Carte.valeur + Carte.couleur.norm()
        else:
            self.Card = None
            
    def unclick(self):
        self.activate = False
        self.setStyleSheet("")
        
        
class QButton_Valider(QPushButton):
    """Surcharge de la classe QPushButton pour le bouton Valider"""
    def __init__(self,MainWindow):
        super().__init__(MainWindow)
        self.Window = MainWindow
    
    def mousePressEvent(self, ev):
        """Définit ce qu'il se passe lorsque l'utilisateur appuie sur le bouton Valider
        On prépare le sélection et on l'envoie à la boucle de jeu"""
        selection_carte = ""
        for el in self.Window.Selection:
            selection_carte += el+';'
        selection_carte = selection_carte[:-1]
        
        #On envoie la sélection dans la boucle de jeu.
        self.Window.Boucle_de_Jeu(selection_carte)
        
class QButton_Passer(QPushButton):
    def __init__(self,MainWindow):
        super().__init__(MainWindow)
        self.Window = MainWindow
    
    def mousePressEvent(self, ev):
        """Définit ce qu'il se passe lorsque l'utilisateur appuie sur le bouton Passer"""
        selection_carte = "passe"
        #On envoie la sélection dans la boucle de jeu.
        self.Window.Boucle_de_Jeu(selection_carte)
        
class QButton_Transition(QPushButton):
    def __init__(self,MainWindow):
        super().__init__(MainWindow)
        self.Window = MainWindow
        #Initialement le bouton est caché
        self.hide()
    def mousePressEvent(self, ev):
        """Définit ce qu'il se passe lorsque l'utilisateur appuie sur le bouton Changer de joueur
        lors d'une transition de joueur. Le bouton se cache et laisse apparaitre le plateau de jeu de nouveau"""
        self.hide()
        self.Window.showPlateau()
        
class QButton_ValideJoker(QPushButton):
    def __init__(self,MainWindow):
        super().__init__(MainWindow)
        self.Window = MainWindow
        #Initialement le bouton est caché
        self.hide()
        
    def mousePressEvent(self, ev):
        """Définit ce qu'il se passe lorsque l'utilisateur appuie sur le bouton Changer de joueur
        lors d'une transition de joueur. Le bouton se cache et laisse apparaitre le plateau de jeu de nouveau"""
        self.hide()
        self.Window.NumJoueur = self.Window.SelectJoueur.value()
        self.Window.Plateau.NumJoueur = self.Window.SelectJoueur.value()
        print(self.Window.NumJoueur)
        self.Window.JoueurActuel = self.Window.Plateau.ListeJoueurs[self.Window.NumJoueur]
        self.Window.Plateau.JoueurActuel = self.Window.Plateau.ListeJoueurs[self.Window.NumJoueur]
        self.Window.SelectJoueur.hide()
        self.Window.actualise()
        self.Window.unclick()

        self.Window.showPlateau()
    