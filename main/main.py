# -*- coding: utf-8 -*-
"""
Created on Fri Oct 24 08:58:15 2025

@author: Formation
"""

import random




class Carte:
    def __init__(self,valeur,couleur):
        self.valeur = valeur
        self.couleur = Couleur(couleur)
    def __str__(self):
        return f"{self.valeur} de " + str(self.couleur)
    def __eq__(self,other):
        return (self.couleur == other.couleur) and (self.valeur == other.valeur)
        
class Tete(Carte):
    def __init__(self,valeur, couleur, Attq, PVs, Immu, visible):
        super(Tete, self).__init__(valeur,couleur)
        self.Attq = Attq
        self.PVs = PVs
        self.Immu = Immu
        self.visible = visible
        
    def DevientVisible(self):
        self.visible = True
        
    def PrendreDegats(self,n):
        self.PVs = self.PVs-n
        
    def DiminueAttaque(self,n):
        self.Attq = self.Attq - n
        if self.Attq < 0:
            self.Attq = 0
                
        
    def __str__(self):
        s = super(Tete,self).__str__()
        s = s.replace("10","Valet").replace("15", "Dame").replace("20","Roi")

        return s + f" Attq : {self.Attq}, PVs : {self.PVs}, Immunité : {self.Immu}"
        
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
            
    def __str__(self):
        return self.couleur
    def __eq__(self,other):
        return self.couleur == other.couleur
    def __ne__(self,other):
        return not self.__eq__(other)
        
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
            self.Pioche.append(Carte(0,'Joker'))
               
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
        
    def JoueCartes(self,combo):
        for el in combo:
            Carte_A_Checker = Carte(el[:-1],el[-1])
            i = self.main.index(Carte_A_Checker)
            self.main.pop(i)
        print(self)
        
    def __str__(self):
        s = f'Main du joueur {self.numero} : '
        for carte in self.main:
            s+= str(carte) + ";"
        return s
                   
class ListeTete:
    def __init__(self):
        
        Valet,Dame,Roi = [],[],[]
        for couleur in ['d','c','t','p']:
            Valet.append(Tete(10, couleur, 10, 20, Couleur(couleur), True))
            Dame.append(Tete(15, couleur, 15, 30, Couleur(couleur), False))
            Roi.append(Tete(20, couleur, 20, 40, Couleur(couleur), False))
        
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
            
    def Top(self):
        return self.liste[0]
        
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
    def AjoutCarte(self, combo):
        l_carte = []
        for combi in combo:
            new_card = Carte(combi[:-1],combi[-1])
            l_carte.append(new_card)
        self.liste = self.liste + l_carte
        

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
        NumJoueur = int(input("Sélectionner le joueur débutant la partie : "))
        JoueurActuel = self.ListeJoueurs[NumJoueur]
        while not self.Fin:
            SaisieInvalide = True
            if self.ListeTete.EstVide():
                self.Win = True
                self.Fin = True
            elif self.ListeTete.EstToutInvisible():
                self.ListeTete.Revele4Cartes()
            while SaisieInvalide:
                print(self.ListeTete.liste[0])
                print(JoueurActuel)
                selection_carte = input("Sélectionner les cartes à jouer : ")
                SaisieInvalide = not(self.ComboFormat(selection_carte) and self.ComboAcceptable(selection_carte) and self.ComboMain(selection_carte,JoueurActuel))
            Combo = selection_carte.split(";")
            self.CartesJouees.AjoutCarte(Combo)
            JoueurActuel.JoueCartes(Combo)
            self.ListeTete.Top().PrendreDegats(self.SommeCombo(Combo))
            self.ActivePouvoir(Combo,NumJoueur)
                
    def PiocheInitiale(self):
        for joueur in self.ListeJoueurs:
            for i in range(joueur.taillemax):
                joueur.Pioche(self.Pioche)
                
    def ComboFormat(self,combo:str):
        """Teste si la combinaison de cartes est un combo au bon format"""
        num = ['1','2','3','4','5','6','7','8','9','10','V','D','R']
        couleur = ['c','d','t','j','p']
        Combinaison_valide = []
        
        for numero in num:
            for c in couleur:
                Combinaison_valide.append(numero+c)
        Combinaison_valide.append("0j")
        
        vecteur = combo.split(";")
        Bool_Combo = True
        
        #On vérifie que les éléments sont au bon format
        for combinaison in vecteur:
            if combinaison not in Combinaison_valide:
                print("Format incorrect, le format doit être NuméroCouleur séparé de ';'")
                print("Ex : '4c;4d' pour jouer un combo de 4")
                print("Les couleurs sont c:Coeur, d:Carreau(Diamond), t:Trèfle, p:Pique, j:Joker(Uniquement avec un 0) ")
                print("Les nombres vont de 0 à 10 et les têtes sont V:Valet, D:Dame, R:Roi.")
                Bool_Combo = False
                
        return Bool_Combo
        
    def ComboAcceptable(self,combo:str):
        """Teste si un combo au bon format est acceptable selon les règles"""
        v = combo.split(";")
        if len(v)==1:
            return True
        else:
            if (("1c" in v) or ("1d" in v) or ("1t" in v) or ("1p" in v)) and (len(v) == 2):
                return True
            
            l = []
            s = 0
            for el in v:
                if l==[]:
                    if el[:-1] in ["V","D","R","0"]:
                        print("Le combo n'est pas acceptable, un combo sans as, doit être fait avec des cartes donc la somme < 10")
                        return False
                    elif int(el[:-1])>5:
                        print("Le combo n'est pas acceptable, un combo sans as, doit être fait avec des cartes donc la somme < 10")
                        return False
                    else:
                        l.append(int(el[:-1]))
                        s+= int(el[:-1])
                else:
                    if int(el[:-1]) not in l:
                        print("Le combo n'est pas acceptable, un combo sans as, doit être fait avec des doublons ou des triplets ou des quadruplets")
                        return False
                    else:
                        s+= int(el[:-1])
            if s<=10:
                return True
            else:
                print("Le combo n'est pas acceptable, un combo sans as, doit être fait avec des cartes donc la somme < 10")
                return False
            
    def ComboMain(self,combo,joueur):
        main = joueur.main.copy()
        v = combo.split(";")
        Bool = True
        for combi in v:
            valeur = combi[:-1]
            couleur = combi[-1]
            Carte_A_Checker = Carte(valeur,couleur)
            print(Carte_A_Checker in main)
            if Carte_A_Checker not in main:
                print("Une carte du combo n'est pas présente dans votre main.")
                Bool = False
            else:
                i = main.index(Carte_A_Checker)
                main.pop(i)
        return Bool
    
    def SommeCombo(self,combo):
        s = 0
        for el in combo:
            if el[:-1] == "V":
                s += 10
            elif el[:-1] == "D":
                s += 15
            elif el[:-1] == "R":
                s += 20
            else:
                s += int(el[:-1])
                
        return s
    def ActivePouvoir(self,combo,num_joueur):
        Somme = self.SommeCombo(combo)
        Immu = self.ListeTete.Top().Immu
        for el in combo:
            if el[-1] == 'c' and Immu != Couleur('c'):
                self.Defausse.VideDefausse(Somme,self.Pioche)
            if el[-1] == 'p' and Immu != Couleur('p'):
                self.ListeTete.Top().DiminueAttaque(Somme)
            if el[-1] == 't' and Immu != Couleur('t'):
                self.ListeTete.Top().PrendreDegats(Somme)
            if el[-1] == 'j':
                self.ListeTete.Top().Immu = Couleur('j')
            if el[-1] == 'd' and Immu != Couleur('d'):
                self.PiocheCarreau(Somme,num_joueur)
                
    def PiocheCarreau(self,n,num_joueur):
        s = n
        joueur = num_joueur
        i = 8*8
        while s != 0 and i != 0 :
            Pioche = self.ListeJoueurs[joueur].Pioche(self.Pioche)
            if Pioche :
                s = s-1
            i = i-1
            joueur = (joueur+1)%(len(self.ListeJoueurs))
            print(joueur)
            
            
            
            
                    
                
        
    def __str__(self):
        s = ''
        for joueur in self.ListeJoueurs:
            s += str(joueur) + '\n'
        return s
        
        
if __name__ == "__main__":
    plat = Plateau(3)
    plat.BoucleDeJeu()
    