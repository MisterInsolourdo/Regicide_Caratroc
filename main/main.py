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
        #Initialisation
        self.Pioche = Pioche(nb_joueur)
        self.Defausse = Defausse()
        self.CartesJouees = CartesJouees()
        self.ListeTete = ListeTete()
        self.ListeJoueurs = [Joueur(i,[],nb_joueur) for i in range(nb_joueur)]
        self.NumJoueur = 0
        self.JoueurActuel = self.ListeJoueurs[0]
        self.Fin = False
        self.Win = False
        
    def BoucleDeJeu(self):
        """Initie la boucle de jeu
            On initialise la Pioche
            On choisit qui est le premier joueur
            Puis tant que le jeu n'est pas soit perdu, soit gagné, on alterne les phases de défense et d'attaque"""
        
        self.PiocheInitiale()
        self.NumJoueur = int(input("Sélectionner le joueur débutant la partie : "))
        self.JoueurActuel = self.ListeJoueurs[self.NumJoueur]
        
        #Tant qu'on a ni perdu ni gagné.
        while not self.Fin:
            
            #S'il n'y a plus de têtes, le jeu est gagné.
            if self.ListeTete.EstVide():
                self.Win = True
                self.Fin = True
            
            #S'il y a des têtes et qu'elles sont toutes invisibles, on en révèle quatre
            elif self.ListeTete.EstToutInvisible():
                self.ListeTete.Revele4Cartes()
            
            #Si on a gagné ou perdu, on sort de la boucle
            if self.Fin:
                if self.Win:
                    print("Gagné")
                else:
                    print("Perdu")
                break
            
            #Phase d'attaque. Si le joueur a joué un joker, on zappe la phase de défense
            Joker = self.Phase_Attaque()
            if Joker:
                continue
            
            #On vérifie si l'adversaire est mort ou non. Si non, on entre en phase de Défense.
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
                #On teste si l'attaque de l'adversaire n'est pas 0, pour ne pas lancer de phase de défense inutilement. 
                if self.ListeTete.Top().Attq <= 0:
                    print("L'adversaire n'a pas d'attaque.")
                else:
                    #Si l'adversaire a de l'attaque -> Phase de défense.
                    #Test : Si le joueur ne peut pas se défendre. Le jeu est perdu, on revient au début de la boucle pour afficher le message et break
                    EstPerdu = self.Phase_Defense()
                    if EstPerdu:
                        continue
                
    def PiocheInitiale(self):
        """Tous les joueurs piochent initialement le nombre maximal de cartes qu'ils peuvent dans le mode de jeu"""
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
            
    def ComboMain(self,combo):
        """Teste si la combinaison de cartes proposée est bien présente dans la main du joueur"""
        main = self.JoueurActuel.main.copy()
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
        """Somme les valeurs des cartes d'un combo"""
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
        """Teste si le combo joué est bien supérieur à l'Attaque, lors d'une défense avec une attaque de Attq"""
        Combo = combo.split(";")
        Somme = self.SommeCombo(Combo)
        if Somme < Attq:
            print(f"Vous ne défaussez que {Somme} par rapport à {Attq}, ce n'est pas assez.")
            return False
        else:
            return True
    
    def ActivePouvoir(self,combo, UI=False):
        """Active l'ensemble des pouvoirs d'un combo"""
        Somme = self.SommeCombo(combo)
        Immu = self.ListeTete.Top().Immu
        #Liste pouvoir stocke les pouvoirs déjà utilisés pour éviter une double activation
        Liste_Pouvoir = []
        for el in combo:
            
            if el[-1] == 'c' and Immu != Couleur('c') and (not 'c' in Liste_Pouvoir):
                print(f"Récupération de {Somme} cartes de la défausse.")
                Liste_Pouvoir.append(el[-1])
                self.Defausse.VideDefausse(Somme,self.Pioche)
            if el[-1] == 'p' and Immu != Couleur('p') and (not 'p' in Liste_Pouvoir):
                print(f"L'adversaire perd {Somme} Attq")
                self.ListeTete.Top().DiminueAttaque(Somme)
                Liste_Pouvoir.append(el[-1])
            if el[-1] == 't' and Immu != Couleur('t') and (not 't' in Liste_Pouvoir):
                print("Doubles dégats !")
                self.ListeTete.Top().PrendreDegats(Somme)
                Liste_Pouvoir.append(el[-1])
            if el[-1] == 'd' and Immu != Couleur('d') and (not 'd' in Liste_Pouvoir):
                print(f"Pioche de {Somme} cartes.")
                self.PiocheCarreau(Somme,self.NumJoueur)
                Liste_Pouvoir.append(el[-1])
            if el[-1] == 'j':
                print("Annulation du pouvoir")
                self.ListeTete.Top().Immu = Couleur('j')
                if UI == False:
                    self.NumJoueur = int(input("Un joker a été joué, sélectionnez le joueur jouant après :"))
                return "Joker"
            
            
            
                
    def Phase_Attaque(self, UI=False, UI_Selection=None):
        """Permet de jouer une phase d'attaque
        Le joueur choisit un combo valide de cartes dans sa main
        Les dégats sont infligés
        Les pouvoirs de chacunes des cartes sont appliqués
        """
        
        
        if not UI:
            SaisieInvalide = True
            while SaisieInvalide:
                print(self.ListeTete)
                print(f"Pioche : {len(self.Pioche)} ; Défausse : {len(self.Defausse)}")
                print(self.ListeTete.Top())
                print(self.JoueurActuel)
                
                #Saisie et Test de la validité du combo
                selection_carte = input("Sélectionner les cartes à jouer : ")
                if selection_carte == "passe":
                    SaisieInvalide = False
                else:
                    SaisieInvalide = not(self.ComboFormat(selection_carte) and self.ComboAcceptable(selection_carte) and self.ComboMain(selection_carte) or selection_carte == "passe")
        else:
            selection_carte = UI_Selection
            
        if selection_carte != "passe":
            Combo = selection_carte.split(";")
            self.CartesJouees.AjoutCarte(Combo)
            self.JoueurActuel.JoueCartes(Combo)
            self.ListeTete.Top().PrendreDegats(self.SommeCombo(Combo))
            Result = self.ActivePouvoir(Combo,UI)
            if Result != None:
                self.JoueurActuel = self.ListeJoueurs[self.NumJoueur]
                return True
        else:
            pass
    
    def Phase_Defense(self, UI=False, UI_Selection=None):
        #Si l'adversaire a de l'attaque : Il attaque
        print(f"L'adversaire vous attaque avec une puissance de {self.ListeTete.Top().Attq}, vous devez défausser cette somme pour survivre")
        self.Fin = not self.JoueurActuel.VerifDefense(self.ListeTete.Top().Attq)
        if self.Fin:
            return True
        
        if not UI:
            SaisieInvalide = True
            while SaisieInvalide:
                print(self.JoueurActuel)
                selection_carte = input("Sélectionner les cartes à jouer : ")
                SaisieInvalide = not(self.ComboFormat(selection_carte) and self.ComboMain(selection_carte) and self.ComboAttq(selection_carte,self.ListeTete.Top().Attq))
        else:
            selection_carte = UI_Selection
            
        Combo = selection_carte.split(";")
        self.JoueurActuel.DefausseCarte(Combo,self.Defausse)
        
        #Sinon : On ne fait rien
        
        #On passe au joueur suivant
        self.NumJoueur = (self.NumJoueur+1)%(len(self.ListeJoueurs))
        if not UI:
            input(f"Le joueur {self.NumJoueur} va prendre la main, appuyer sur Entrée pour continuer : ")
        self.JoueurActuel = self.ListeJoueurs[self.NumJoueur]           
                
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
    