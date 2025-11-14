# -*- coding: utf-8 -*-
"""
Created on Fri Oct 24 08:58:15 2025
@author: Fabien
"""

from cartes import Carte, Couleur
from joueur import Joueur
from listes import Pioche, Defausse, ListeTete, CartesJouees
    
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
            if self.ListeTete.EstVide():
                self.Win = True
                self.Fin = True
            elif self.ListeTete.EstToutInvisible():
                self.ListeTete.Revele4Cartes()
            if self.Fin:
                continue
            SaisieInvalide = True
            while SaisieInvalide:
                print(self.ListeTete)
                print(f"Pioche : {len(self.Pioche)} ; Défausse : {len(self.Defausse)}")
                print(self.ListeTete.Top())
                print(JoueurActuel)
                selection_carte = input("Sélectionner les cartes à jouer : ")
                if selection_carte == "passe":
                    SaisieInvalide = False
                else:
                    SaisieInvalide = not(self.ComboFormat(selection_carte) and self.ComboAcceptable(selection_carte) and self.ComboMain(selection_carte,JoueurActuel) or selection_carte == "passe")
            if selection_carte != "passe":
                Combo = selection_carte.split(";")
                self.CartesJouees.AjoutCarte(Combo)
                JoueurActuel.JoueCartes(Combo)
                self.ListeTete.Top().PrendreDegats(self.SommeCombo(Combo))
                Result = self.ActivePouvoir(Combo,NumJoueur)
                if Result != None:
                    JoueurActuel = self.ListeJoueurs[Result]
                    continue
            else:
                pass
            
            if self.ListeTete.Top().VerifieMort():
                print("L'adversaire est mort.\n")
                self.Defausse.AddDefausse(self.CartesJouees.liste)
                self.CartesJouees.Reset()
                self.ListeTete.Top().EstUneCarte = True
                if self.ListeTete.Top().DegatsExact():
                    print("Wow ! Exact Damage !\nLa carte de l'adversaire est placée au-dessus de la pioche. \n")
                    self.ListeTete.TopVersPioche(self.Pioche)
                else:
                    print("La carte de l'adversaire est placée en bas de la défausse. \n ")
                    self.ListeTete.TopVersDefausse(self.Defausse)
                
            else:
                if self.ListeTete.Top().Attq > 0:
                    print(f"L'adversaire vous attaque avec une puissance de {self.ListeTete.Top().Attq}, vous devez défausser cette somme pour survivre")
                    self.Fin = not JoueurActuel.VerifDefense(self.ListeTete.Top().Attq)
                    if self.Fin:
                        print("Perdu")
                        continue
                    SaisieInvalide = True
                    while SaisieInvalide:
                        print(JoueurActuel)
                        selection_carte = input("Sélectionner les cartes à jouer : ")
                        SaisieInvalide = not(self.ComboFormat(selection_carte) and self.ComboMain(selection_carte,JoueurActuel) and self.ComboAttq(selection_carte,self.ListeTete.Top().Attq))
                    Combo = selection_carte.split(";")
                    JoueurActuel.DefausseCarte(Combo,self.Defausse)
                else:
                    print("L'adversaire n'a pas d'attaque, il ne peut pas vous attaquer.")
                    
                NumJoueur = (NumJoueur+1)%(len(self.ListeJoueurs))
                input(f"Le joueur {NumJoueur} va prendre la main, appuyer sur Entrée pour continuer : ")
                JoueurActuel = self.ListeJoueurs[NumJoueur]                
                
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
    
    def ComboAttq(self,combo,Attq):
        Combo = combo.split(";")
        Somme = self.SommeCombo(Combo)
        if Somme < Attq:
            print(f"Vous ne défaussez que {Somme} par rapport à {Attq}, ce n'est pas assez.")
            return False
        else:
            return True
    
    def ActivePouvoir(self,combo,num_joueur):
        Somme = self.SommeCombo(combo)
        Immu = self.ListeTete.Top().Immu
        for el in combo:
            if el[-1] == 'c' and Immu != Couleur('c'):
                print(f"Récupération de {Somme} cartes de la défausse.")
                self.Defausse.VideDefausse(Somme,self.Pioche)
            if el[-1] == 'p' and Immu != Couleur('p'):
                print(f"L'adversaire perd {Somme} Attq")
                self.ListeTete.Top().DiminueAttaque(Somme)
            if el[-1] == 't' and Immu != Couleur('t'):
                print("Doubles dégats !")
                self.ListeTete.Top().PrendreDegats(Somme)
            if el[-1] == 'j':
                print("Annulation du pouvoir")
                self.ListeTete.Top().Immu = Couleur('j')
                NumJoueur = int(input("Un joker a été joué, sélectionnez le joueur jouant après :"))
                return NumJoueur
            
            if el[-1] == 'd' and Immu != Couleur('d'):
                print(f"Pioche de {Somme} cartes.")
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
        
    def __str__(self):
        s = ''
        for joueur in self.ListeJoueurs:
            s += str(joueur) + '\n'
        return s
        
        
if __name__ == "__main__":
    plat = Plateau(2)
    plat.BoucleDeJeu()
    