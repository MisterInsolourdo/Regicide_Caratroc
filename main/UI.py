# -*- coding: utf-8 -*-
"""
Created on Mon Nov  3 11:03:25 2025

@author: domdo
"""

#Import externe
from PyQt5.QtWidgets import QApplication, QWidget, QSpinBox, QLabel
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtMultimedia import QSound

import sys
from main import Plateau
#Import des différents boutons
from UI_Buttons import QLabel_Carte, QButton_Passer, QButton_Valider, QButton_Transition, QButton_ValideJoker


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
        self.Adversaire.setGeometry(QtCore.QRect(int(w/3)+50,0,int(w/4),int(h/2)))
        self.Adversaire.setScaledContents(True)
        
        #Les PVs de l'adversaire
        self.PV = QtWidgets.QLabel(self)
        self.PV.setGeometry(QtCore.QRect(0,300,800,20))
        self.PV.setAlignment(Qt.AlignCenter)
        
        #L'Attaque de l'adversaire
        self.Attq = QtWidgets.QLabel(self)
        self.Attq.setGeometry(QtCore.QRect(0,325,800,20))
        self.Attq.setAlignment(Qt.AlignCenter)
        
        #Texte Contextuel
        self.Text = QtWidgets.QLabel(self)
        self.Text.setGeometry(QtCore.QRect(0,350,800,40))
        self.Text.setAlignment(Qt.AlignCenter)
        self.Text.setText("Phase d'attaque")
        
        #La liste des cartes du joueur en cours.
        self.Main = []
        for i in range(9):
            Carte_i = QLabel_Carte(self)
            Carte_i.setGeometry(QtCore.QRect(int(w/9)*i, int(3*h/4), int(w/10),int(h/5)))
            Carte_i.setScaledContents(True)
            self.Main.append(Carte_i)
            
        #La Pioche
        self.Pioche = QtWidgets.QLabel(self)
        self.Pioche.setGeometry(QtCore.QRect(0,0,int(w/10),int(h/5)))
        self.Pioche.setScaledContents(True)
        
        self.CartesRestantes = QtWidgets.QLabel(self)
        self.CartesRestantes.setGeometry(QtCore.QRect(100,0,100,100))
        self.CartesRestantes.setStyleSheet("color: black;")
        font = QFont("Arial", 14, QFont.Bold)  # (nom, taille, style)
        self.CartesRestantes.setFont(font)
        
        #La Défausse
        self.Defausse = QtWidgets.QLabel(self)
        self.Defausse.setGeometry(QtCore.QRect(0,int(h/5),int(w/10),int(h/5)))
        self.Defausse.setScaledContents(True)
        
        self.CartesDefausse = QtWidgets.QLabel(self)
        self.CartesDefausse.setGeometry(QtCore.QRect(100,100,100,100))
        self.CartesDefausse.setStyleSheet("color: black;")
        font = QFont("Arial", 14, QFont.Bold)  # (nom, taille, style)
        self.CartesDefausse.setFont(font)
        
        #Le bouton valider 
        self.Validate = QButton_Valider(self)
        self.Validate.setGeometry(QtCore.QRect(w-100,h-50,100,40))
        self.Validate.setText("Valider")
        
        #Le bouton passer
        self.Passer = QButton_Passer(self)
        self.Passer.setGeometry(QtCore.QRect(w-100,h-150,100,40))
        self.Passer.setText("Passer")
        
        #Le bouton pour assurer les transitions
        self.Transition = QButton_Transition(self)
        self.Transition.setGeometry(QtCore.QRect(0,500,800,40))
        self.Transition.setText("...")
        
        #Une spinBox pour sélectionner le joueur qui doit jouer (Notamment suite à l'utilisation d'un Joker)
        self.SelectJoueur = QSpinBox(self)
        self.SelectJoueur.setMinimum(0)
        self.SelectJoueur.setMaximum(n-1)
        self.SelectJoueur.setGeometry(QtCore.QRect(230,300,340,40))
        self.SelectJoueur.setPrefix("Joker Activé, sélectionner le prochain joueur à jouer : ")
        self.SelectJoueur.hide()
        
        #Un bouton de transition entre un Joker et le plateau
        self.TransitionJoker = QButton_ValideJoker(self)
        self.TransitionJoker.setGeometry(QtCore.QRect(0,500,800,40))
        self.TransitionJoker.setText("Valider le joueur suivant")
        
        
        
        #Création d'un plateau
        self.Plateau = Plateau(n)
        
        #Les mains des joueur
        self.Mains = []
        for i in range(n):
            Main_i = QtWidgets.QLabel(self)
            Main_i.setGeometry(QtCore.QRect(600,20*i,200,20))
            Main_i.setStyleSheet("color: black;")
            font = QFont("Arial", 10, QFont.Bold)  # (nom, taille, style)
            Main_i.setFont(font)
            self.Mains.append(Main_i)
        
        #Les Têtes visibles suivantes sont affichées, Il y en a au maximum 3
        self.TetesVisibles = []
        for i in range(3):
            Tete_i = QLabel(self)
            Tete_i.setGeometry(QtCore.QRect(0+20*i, 250, int(w/10),int(h/5)))
            Tete_i.setScaledContents(True)
            self.TetesVisibles.append(Tete_i)
        self.TetesVisibles.reverse()
            
        #Petit texte pour indique à quoi correspond ces cartes dans l'UI
        self.TetesVisiblesTexte = QLabel(self)
        self.TetesVisiblesTexte.setGeometry(QtCore.QRect(80, 250+int(w/20), 200,40))
        self.TetesVisiblesTexte.setAlignment(Qt.AlignCenter)
        self.TetesVisiblesTexte.setText("Prochain Adversaire\nà combattre")
        
        #Les cartes jouées sont affichées également. Techniquement au maximum il y en a 16
        #Car la carte la plus forte a 40PVs et qu'on peut techniquement la tuer
        #Qu'avec des 1,2,3,4 or 4*1+4*2+4*3+4*4 = 40
        self.CartesJouees = []
        for i in range(16):
            CJ_i = QLabel(self)
            if i <= 7:
                CJ_i.setGeometry(QtCore.QRect(570+18*i, 150, int(w/10),int(h/5)))
            else:
                CJ_i.setGeometry(QtCore.QRect(570+18*(i-8), 200, int(w/10),int(h/5)))
            CJ_i.setScaledContents(True)
            self.CartesJouees.append(CJ_i)
            
        #Petit texte pour indique à quoi correspond ces cartes dans l'UI
        self.CJTexte = QLabel(self)
        self.CJTexte.setGeometry(QtCore.QRect(570, 120, 230,20))
        self.CJTexte.setAlignment(Qt.AlignCenter)
        self.CJTexte.setText("Cartes Jouées : ")
            
        
        #Création d'une sélection
        self.Selection= []
        
        #Musique !!! 
        self.Musique = QSound("./Son/Legendaire.wav")
        self.Musique.setLoops(100000)
        self.Musique.play()
            
    def setupUi(self):
        self.Plateau.PiocheInitiale()
        self.NumJoueur = 0
        self.JoueurActuel = self.Plateau.ListeJoueurs[self.NumJoueur]
        self.actualise()
        
    def Boucle_de_Jeu(self,selection_carte):
        #On teste si la saisie est valide
        if self.Phase == "Attaque":
            SaisieInvalide = not(self.Plateau.ComboFormat(selection_carte) and self.Plateau.ComboAcceptable(selection_carte) and self.Plateau.ComboMain(selection_carte) or selection_carte == "passe")
        elif self.Phase == "Défense":
            SaisieInvalide = not(self.Plateau.ComboFormat(selection_carte) and self.Plateau.ComboMain(selection_carte) and self.Plateau.ComboAttq(selection_carte,self.Plateau.ListeTete.Top().Attq))
        
        if self.Phase == "Attaque":
            if not SaisieInvalide:
                #Si on joue un Joker, le tour se finit et on sélectionne un nouveau joueur via l'interface adaptée.
                if self.Plateau.Phase_Attaque(UI=True, UI_Selection=selection_carte)==True:
                    self.ShowInterfaceJoker()
                    #Le return true est juste là pour assurer qu'on sorte de la boucle de jeu.
                    return True
            else:
                self.Text.setText("La sélection est invalide")
                #Return None pour ne pas aller plus loin
                return None
                
            #On vérifie si l'adversaire est mort ou non. 
            #S'il est mort on reste en phase d'attaque, on change d'adversaire et on garde le même joueur
            if self.Plateau.ListeTete.Top().VerifieMort():
                print("L'adversaire est mort.\n")
                self.Plateau.Defausse.AddDefausse(self.Plateau.CartesJouees.liste)
                self.Plateau.CartesJouees.Reset()
                self.Plateau.ListeTete.Top().EstUneCarte = True
                if self.Plateau.ListeTete.Top().DegatsExact():
                    print("Wow ! Exact Damage !\nLa carte de l'adversaire est placée au-dessus de la pioche. \n")
                    self.Plateau.ListeTete.TopVersPioche(self.Plateau.Pioche)
                else:
                    print("La carte de l'adversaire est placée en bas de la défausse. \n ")
                    self.Plateau.ListeTete.TopVersDefausse(self.Plateau.Defausse)
                    
            #Sinon on passe à la phase de Défense si l'adversaire a de l'attaque
            else:
                if self.Plateau.ListeTete.Top().Attq <= 0:
                    self.NumJoueur = (self.NumJoueur+1)%(len(self.Plateau.ListeJoueurs))
                    self.JoueurActuel = self.Plateau.ListeJoueurs[self.NumJoueur]
                    self.Plateau.JoueurActuel = self.Plateau.ListeJoueurs[self.NumJoueur]
                    self.Text.setText(f"L'adversaire n'a pas d'attaque. Le joueur {self.NumJoueur} prend la main")
                    self.TransitionJoueur()
                else:
                    self.Fin = not self.Plateau.JoueurActuel.VerifDefense( self.Plateau.ListeTete.Top().Attq)
                    if self.Fin:
                        self.Text.setText(f"Game Over ! Le joueur {self.NumJoueur} ne peut pas se défendre de {self.Plateau.ListeTete.Top().Attq}")
                        self.HidePlateau()
                        self.Musique = QSound("./Son/GameOver.wav")
                        self.Musique.setLoops(100000)
                        self.Musique.play()
                    else:
                        self.Text.setText(f"Phase de Défense : L'adversaire attaque de {self.Plateau.ListeTete.Top().Attq}. Défaussez-vous d'une valeur supérieur ou égale")
                        self.Phase = "Défense"
                    
            
            #On actualise l'UI et on désélectionne la sélection.
            self.actualise()
            self.unclick()
            
            
        elif self.Phase == "Défense":
            if not SaisieInvalide:
                self.Plateau.Phase_Defense(UI=True, UI_Selection=selection_carte)
                self.NumJoueur = (self.NumJoueur+1)%(len(self.Plateau.ListeJoueurs))
                self.JoueurActuel = self.Plateau.ListeJoueurs[self.NumJoueur]
                self.Plateau.JoueurActuel = self.Plateau.ListeJoueurs[self.NumJoueur]
                self.TransitionJoueur()
                self.Phase = "Attaque"
                self.Text.setText("Phase d'attaque")
                
                self.Fin = len(self.Plateau.JoueurActuel.main)==0 and self.Plateau.ListeTete.Top().Attq>0
                if self.Fin:
                    self.HidePlateau()
                    self.Text.setText(f"Game Over ! Le joueur {self.NumJoueur} n'a plus de cartes et ne peut donc se défendre")
                    self.Musique = QSound("./Son/GameOver.wav")
                    self.Musique.setLoops(100000)
                    self.Musique.play()
                
            
            #On actualise l'UI et on désélectionne la sélection.
            self.actualise()
            self.unclick()
            
        #Victoire
        if self.Plateau.ListeTete.EstVide():
            self.Fin =True
            self.HidePlateau()
            self.Text.setText("VOUS AVEZ GAGNÉ !!!")
            self.Adversaire.hide()
            self.PV.hide()
            self.Attq.hide()
            self.Musique = QSound("./Son/Fanfare.wav")
            self.Musique.setLoops(100000)
            self.Musique.play()
    
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
        
        if Tete != None:
            carte = Tete.valeur + Tete.couleur.norm()
            
            #Actualisation de la carte
            pixmap = QtGui.QPixmap(f"Cartes/{carte}.png")
            self.Adversaire.setPixmap(pixmap)
            
            #Actualisation des PVs/Attq de la carte
            self.PV.setText(f"Pv : {Tete.PVs}")
            self.Attq.setText(f"Attq : {Tete.Attq}")

    def actualise_pioche(self, Pioche):
        if len(Pioche) == 0:
            pixmap = QtGui.QPixmap("Cartes/Dummy.png")
        else:
            pixmap = QtGui.QPixmap("Cartes/FaceCache.png")
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
        
    def actualise_Mains(self):
        for i in range(len(self.Mains)):
            Joueur_i = self.Plateau.ListeJoueurs[i]
            
            if Joueur_i == self.Plateau.JoueurActuel:
                self.Mains[i].setStyleSheet("color: red;")
            else:
                self.Mains[i].setStyleSheet("color: black;")
                
            self.Mains[i].setText(f"Joueur {i} : {str(len(Joueur_i.main))} cartes")
            
    def actualise_TetesVisibles(self):
        if self.Plateau.ListeTete.EstToutInvisible():
            self.Plateau.ListeTete.Revele4Cartes()    
        for i in range(3):
            try:
                Tete = self.Plateau.ListeTete.liste[i+1]
                if Tete.visible:
                    pixmap = QtGui.QPixmap(f"Cartes/{Tete.valeur + Tete.couleur.norm()}.png")
                    self.TetesVisibles[i].setPixmap(pixmap)
                else:
                     pixmap = QtGui.QPixmap("Cartes/Dummy.png")   
                     self.TetesVisibles[i].setPixmap(pixmap)
                
            except:
                pixmap = QtGui.QPixmap("Cartes/Dummy.png")
                self.TetesVisibles[i].setPixmap(pixmap)
                
    def actualise_CartesJouees(self):
        for i in range(16):
            try:
                CarteJouee = self.Plateau.CartesJouees.liste[i]
                pixmap = QtGui.QPixmap(f"Cartes/{CarteJouee.valeur + CarteJouee.couleur.norm()}.png")
                self.CartesJouees[i].setPixmap(pixmap)
            except:
                pixmap = QtGui.QPixmap("Cartes/Dummy.png")
                self.CartesJouees[i].setPixmap(pixmap)
    
                
        
    def actualise(self):
        """Actualise l'affichage"""
        self.actualise_main(self.JoueurActuel)
        self.actualise_adversaire(self.Plateau.ListeTete.Top())
        self.actualise_pioche(self.Plateau.Pioche)
        self.actualise_defausse(self.Plateau.Defausse)
        self.actualise_Mains()
        self.actualise_TetesVisibles()
        self.actualise_CartesJouees()
        self.Selection = []
        
    def unclick(self):
        """Permet de désélectionner tous les éléments de la main"""
        for Label in self.Main:
            Label.unclick()
            
    def HidePlateau(self):
        """Cache l'ensemble du plateau.
        Sert pour afficher les éléments de défaite/victoire
        Sert pour afficher un affichage vide lors de la transition entre les joueurs
        Sert pour sélectionner le prochain joueur après l'utilisation d'un Joker"""
        for carte in self.Main:
            carte.hide()
        self.Passer.hide()
        self.Validate.hide()
        
    def showPlateau(self):
        """Réaffiche l'ensemble du plateau.
        Sert pour faire revenir le plateau après un HidePlateau suite à un changement de joueur/Joker"""
        for carte in self.Main:
            carte.show()
        self.Passer.show()
        self.Validate.show()
        
    def ShowInterfaceJoker(self):
        self.HidePlateau()
        self.TransitionJoker.show()
        self.SelectJoueur.show()
        
    def TransitionJoueur(self):
        self.HidePlateau()
        self.Transition.show()
        self.Transition.setText(f"Le joueur {self.NumJoueur} va prendre la main")
        
        
        
    
        
        
if __name__ == '__main__':
    #Ouverture de la fenêtre principale
    app = QApplication(sys.argv)
    ui = MainWindow(2)
    ui.setWindowTitle("PyQTicide")
    
    ui.setupUi()
    ui.show()
    
    sys.exit(app.exec_())