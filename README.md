# PyQTicide
## Régicide
Régicide est un jeu coopérative se jouant de 1 à 4 joueurs. Il a été crée par Paul Abrahams, Luke Badger et Andy Richdale
PyQTicide est une adaptation du jeu réalisé avec PyQT dans un cadre scolaire. La version actuelle ne gère pas le mode solo.

Le but du jeu est de vaincre l'ensemble des têtes (Valet, Dame, Roi) avec ses mains, la pioche et la défausse.
Les têtes constituent les adversaires que l'on doit vaincre à chaque tour. Ils ont une attaque variable (10,15,20) contre laquelle il faut se défendre à chaque tour en défaussant cette valeur.

Pour cela, on utilise son jeu chacun son tour, en utilisant les pouvoirs de chaque couleur.
- Les Piques permettent de diminuer l'attaque des adversaires
- Les Trèfles permettent de faire des dégâts doubles
- Les Coeurs permettent de ramener des cartes de la défausse vers la pioche
- Les Carreaux permettent de piocher des cartes

Les têtes vaincues sont des cartes comme les autres et peuvent être piochées plus tard.
On gagne si l'on vaint toutes les têtes, on perd si un joueur est incapable de se défendre d'une attaque d'un adversaire.

Un tour classique se présente sous la forme :
- Le joueur{i} joue une carte ou un combo de cartes.
- On inflige les dégâts et active les pouvoirs de chaque carte
- L'adversaire, s'il n'est pas mort, attaque le joueur{i}
- On passe au joueur{i+1} (Sauf si l'adversaire est mort auquel cas on reste au joueur{i}) 

Un combo valide est :
- Soit une carte seule
- Soit un as et une autre carte
- Soit X fois la même carte à condition que la somme des cartes soit inférieure ou égale à 10.

L'ensemble des règles officielles peuvent se trouver ici : https://iello.fr/jeux/regicide/

## Lancer le jeu
Le jeu est disponible sous deux formats : En ligne de commande ou avec une interface graphique (UI)
### En ligne de commande
Le fichier main.py contient le jeu en ligne de commandes.

On peut modifier ces lignes pour changer le nombre de joueur sur le plateau
if __name__ == "__main__":
    plat = Plateau(2)
    plat.BoucleDeJeu()

Le jeu commence par demander le numéro du joueur qui va commencer.
A chaque étape, seront affichés en ligne de commande :
Les têtes suivantes qui sont visibles
Le nombre de cartes restant dans la Pioche ; dans la Défausse
L'Adversaire actuellement en jeu ; Son Attaque ; Ses PVs ; Et le pouvoir auquel il est immunisé.
La main du joueur à qui c'est le tour.

Pour jouer le joueur doit joueur une combinaison valide de sa main ou passer.

Pour cela, il doit écrire :
- Soit "passe" pour passer
- Soit une combinaison de cartes valides sous un format spécifique. Ce format spécifique est de la forme ValeurCouleur avec Valeur:{0;1;2;3;4;5;6;7;8;9;10;V;D;R} et Couleur:{j;p;t;c;d} avec  j:Joker-p:Pique-t:Trèfle-c:Coeur-d:Carreau(Diamond)
- La combinaison doit être séparée par des ; et être présente dans la main du joueur

Ainsi les combinaisons :
"5t;5c" joue un combo de 5 de Trèfle et de 5 de Coeur
"7d" joue un 7 de Carreau
"0j" joue le Joker (seule carte de valeur 0)

Puis le joueur doit éventuellement se défendre en jouant des cartes dont la somme est supérieure à l'attaque de l'adversaire, en tapant les cartes qu'il veut défausser sous le même format.
Entre le tour de chaque joueur, un message apparait et attend juste qu'on appuie sur entrée pour passer au joueur suivant (Pour éviter que le joueur voir la main de son coéquipier)

### Interface graphique (UI)

Le jeu se joue de la même façon en mode UI.

<img width="799" height="621" alt="image" src="https://github.com/user-attachments/assets/6ea785da-38e1-4579-8008-ac31351cab66" />

Les combinaisons se jouent en cliquant sur les cartes que l'on souhaite jouer puis en cliquant sur le bouton "Valider"
Si le joueur ne veut pas jouer, il peut cliquer sur passer (Il se fera quand même attaquer)

Lors de la phase de défense : 







