# -*- coding: utf-8 -*-
"""
Created on Mon Nov  3 11:03:25 2025

@author: domdo
"""

#Import externe
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QFont

import sys
from main import Plateau

class QLabel_Carte(QLabel):
    def __init__(self,MainWindow):
        super().__init__(MainWindow)
        self.activate = False
        self.Window = MainWindow
        self.Card = None
        
    clicked=pyqtSignal()

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
    def __init__(self,MainWindow):
        super().__init__(MainWindow)
        self.Window = MainWindow
        
        
    clicked=pyqtSignal()
    def mousePressEvent(self, ev):
        selection_carte = ""
        if self.Window.Selection == []:
            selection_carte = "passe"
        else:
            for el in self.Window.Selection:
                selection_carte += el+';'
            selection_carte = selection_carte[:-1]
            
        if self.Window.Phase == "Attaque":
            SaisieInvalide = not(self.Window.Plateau.ComboFormat(selection_carte) and self.Window.Plateau.ComboAcceptable(selection_carte) and self.Window.Plateau.ComboMain(selection_carte,self.Window.JoueurActuel) or selection_carte == "passe")
        elif self.Window.Phase == "Défense":
            SaisieInvalide = not(self.Window.Plateau.ComboFormat(selection_carte) and self.Window.Plateau.ComboMain(selection_carte,self.Window.JoueurActuel) and self.Window.Plateau.ComboAttq(selection_carte,self.Window.Plateau.ListeTete.Top().Attq))
        
        if self.Window.Phase == "Attaque":
            if not SaisieInvalide:
                if selection_carte != "passe":
                    Combo = selection_carte.split(";")
                    self.Window.Plateau.CartesJouees.AjoutCarte(Combo)
                    self.Window.JoueurActuel.JoueCartes(Combo)
                    self.Window.Plateau.ListeTete.Top().PrendreDegats(self.Window.Plateau.SommeCombo(Combo))
                    Result = self.Window.Plateau.ActivePouvoir(Combo,self.Window.NumJoueur)
                    if Result != None:
                        self.Window.JoueurActuel = self.Window.Plateau.ListeJoueurs[Result]
                        
                    print(self.Window.JoueurActuel)
                else:
                    pass
                
                self.Window.actualise()
                self.Window.unclick()
            
            if self.Window.Plateau.ListeTete.Top().VerifieMort():
                print("L'adversaire est mort.\n")
                self.Window.Plateau.Defausse.AddDefausse(self.Window.Plateau.CartesJouees.liste)
                self.Window.Plateau.CartesJouees.Reset()
                self.Window.Plateau.ListeTete.Top().EstUneCarte = True
                if self.Window.Plateau.ListeTete.Top().DegatsExact():
                    print("Wow ! Exact Damage !\nLa carte de l'adversaire est placée au-dessus de la pioche. \n")
                    self.Window.Plateau.ListeTete.TopVersPioche(self.Window.Plateau.Pioche)
                else:
                    print("La carte de l'adversaire est placée en bas de la défausse. \n ")
                    self.Window.Plateau.ListeTete.TopVersDefausse(self.Window.Plateau.Defausse)
                    
            else:
                self.Window.Phase = "Défense"

            self.Window.actualise()
            self.Window.unclick()
            
        elif self.Window.Phase == "Défense":
            if self.Window.Plateau.ListeTete.Top().Attq > 0:
                print(f"L'adversaire vous attaque avec une puissance de {self.Window.Plateau.ListeTete.Top().Attq}, vous devez défausser cette somme pour survivre")
                self.Fin = not self.Window.JoueurActuel.VerifDefense(self.Window.Plateau.ListeTete.Top().Attq)
                if self.Fin:
                    print("Perdu")
                Combo = selection_carte.split(";")
                self.Window.JoueurActuel.DefausseCarte(Combo,self.Window.Plateau.Defausse)
            else:
                print("L'adversaire n'a pas d'attaque, il ne peut pas vous attaquer.")
                
            self.Window.NumJoueur = (self.Window.NumJoueur+1)%(len(self.Window.Plateau.ListeJoueurs))
            #input(f"Le joueur {NumJoueur} va prendre la main, appuyer sur Entrée pour continuer : ")
            self.Window.JoueurActuel = self.Window.Plateau.ListeJoueurs[self.Window.NumJoueur]
            self.Window.Plateau.JoueurActuel = self.Window.Plateau.ListeJoueurs[self.Window.NumJoueur]
            self.Window.Phase = "Attaque"
            
            self.Window.actualise()
            self.Window.unclick()

class MainWindow(QWidget):
    """Cette classe définit la fenêtre principale, ainsi que tous les événements utilisateurs (Clic, appui de touches...etc)"""
    def __init__(self,n):
        super().__init__()
        
        #On définit la taille de la fenêtre.
        self.setFixedWidth(800)
        self.setFixedHeight(594)
        
        self.Phase = "Attaque"
        
        w = self.width()
        h = self.height()
        
        #On définit les emplacements des différent éléments graphiques.
        
        #L'adversaire principal.
        self.Adversaire = QtWidgets.QLabel(self)
        self.Adversaire.setGeometry(QtCore.QRect(int(w/3),0,int(w/4),int(h/2)))
        self.Adversaire.setScaledContents(True)
        
        """print((int(w/4),0,int(w/2),int(h/2)))"""
        
        #Les PVs de l'adversaire
        self.PV = QtWidgets.QLabel(self)
        self.PV.setGeometry(QtCore.QRect(int(w/4),int(h/2)+50,100,20))
        
        #L'Attaque de l'adversaire
        self.Attq = QtWidgets.QLabel(self)
        self.Attq.setGeometry(QtCore.QRect(250,int(h/2)+100,100,20))
        
        #La liste des cartes du joueur en cours.
        self.Main = []
        for i in range(9):
            Carte_i = QLabel_Carte(self)
            Carte_i.setGeometry(QtCore.QRect(int(w/9)*i, int(3*h/4), int(w/9), int(w/9)))
            Carte_i.setScaledContents(True)
            self.Main.append(Carte_i)
            
        #La Pioche
        self.Pioche = QtWidgets.QLabel(self)
        self.Pioche.setGeometry(QtCore.QRect(0,0,100,100))
        self.Pioche.setScaledContents(True)
        
        self.CartesRestantes = QtWidgets.QLabel(self)
        self.CartesRestantes.setGeometry(QtCore.QRect(100,0,100,100))
        self.CartesRestantes.setStyleSheet("color: black;")
        font = QFont("Arial", 14, QFont.Bold)  # (nom, taille, style)
        self.CartesRestantes.setFont(font)
        
        #La Défausse
        self.Defausse = QtWidgets.QLabel(self)
        self.Defausse.setGeometry(QtCore.QRect(0,100,100,100))
        self.Defausse.setScaledContents(True)
        
        self.CartesDefausse = QtWidgets.QLabel(self)
        self.CartesDefausse.setGeometry(QtCore.QRect(100,100,100,100))
        self.CartesDefausse.setStyleSheet("color: black;")
        font = QFont("Arial", 14, QFont.Bold)  # (nom, taille, style)
        self.CartesDefausse.setFont(font)
        
        #Le bouton valider 
        self.Validate = QButton_Valider(self)
        self.Validate.setGeometry(QtCore.QRect(w-100,h-100,100,100))
        self.Validate.setText("Valider")
        
        #Création d'un plateau
        self.Plateau = Plateau(n)
        
        #Création d'une sélection
        self.Selection= []
            
    def setupUi(self):
        self.Plateau.PiocheInitiale()
        self.NumJoueur = 0
        self.JoueurActuel = self.Plateau.ListeJoueurs[self.NumJoueur]
        self.actualise()
    
    def actualise_main(self, Joueur):
        main = Joueur.main
        for i in range(9):
            try:
                Carte_i = self.Main[i]
                carte = main[i]
                Carte_i.setScaledContents(True)
                pixmap = QtGui.QPixmap(f"Cartes/{carte.valeur + carte.couleur.norm()}.png")
                Carte_i.setPixmap(pixmap)
                Carte_i.set_Card(carte)
            except IndexError:
                Carte_i = self.Main[i]
                Carte_i.setScaledContents(True)
                pixmap = QtGui.QPixmap("Cartes/EpicSausage.png")
                Carte_i.setPixmap(pixmap)
                Carte_i.set_Card(None,False)
                
                
            
    def actualise_adversaire(self,Tete):
        carte = Tete.valeur + Tete.couleur.norm()
        
        #Actualisation de la carte
        print(f"Cartes/{carte}.png")
        pixmap = QtGui.QPixmap(f"Cartes/{carte}.png")
        self.Adversaire.setPixmap(pixmap)
        
        #Actualisation des PVs/Attq de la carte
        self.PV.setText(f"Pv : {Tete.PVs}")
        self.Attq.setText(f"Attq : {Tete.Attq}")

    def actualise_pioche(self, Pioche):
        pixmap = QtGui.QPixmap("Cartes/FaceCache.jpg")
        self.Pioche.setPixmap(pixmap)
        self.CartesRestantes.setText(str(len(self.Plateau.Pioche)))
        
    
    def actualise_defausse(self,Defausse):
        if len(Defausse) != 0:
            Carte = Defausse.Defausse[-1]
            pixmap = QtGui.QPixmap(f"Cartes/{Carte.valeur + Carte.couleur.norm()}.png")
            self.Defausse.setPixmap(pixmap)
        else:
            pixmap = QtGui.QPixmap("Dummy.png")
            self.Defausse.setPixmap(pixmap)
            
        self.CartesDefausse.setText(str(len(self.Plateau.Defausse)))
        
    def actualise(self):
        self.actualise_main(self.JoueurActuel)
        self.actualise_adversaire(self.Plateau.ListeTete.Top())
        self.actualise_pioche(self.Plateau.Pioche)
        self.actualise_defausse(self.Plateau.Defausse)
        self.Selection = []
        
    def unclick(self):
        for Label in self.Main:
            Label.unclick()
        
        
        
    
        
        
if __name__ == '__main__':
    #Ouverture de la fenêtre principale
    app = QApplication(sys.argv)
    ui = MainWindow(3)
    
    ui.setupUi()
    ui.show()
    
    sys.exit(app.exec_())