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

L'ensemble des règles officielles peuvent se trouver ici : https://iello.fr/jeux/regicide/

