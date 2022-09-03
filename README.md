# systeme_proies_predateurs_avec_loups_lapins_herbe

On observe dans la nature que les populations de proies et prédateurs ne se stabilisent pas autour d'un certain point d'équilibre, mais évoluent au cours du temps de manière cycliquer : Trop de prédateurs finissent par tuer trop de proies, ce qui cause le déclin des prédateurs par manque de nourriture. Ce déclin permet à la population de proies de croître à nouveau, causant à son tour l'augmentation du nombre de prédateurs, et ainsi de suite.

Simuler un tel écosystème peut se faire sur une grille de cases similaires à celle du jeu de la vie (voir un autre dépôt), mais avec des règles plus complexes. 

On considère ici des lapins (proies) et des loups (prédateurs). Chaque cellule contient de l'herbe et au plus un animal (lapin ou loup). L'herbe pousse d'une unité de nourriture (UN) par unité de temps (UT), jusqu'à une valeur maximale de 100 UN. Au départ, chaque cellule a 20 UN d'herbe et les lapins et les loups sont répartis aléatoirement. 
Chaque animal peut se déplacer dans l'une des quatre directions à chaque UT. Les lapins se nourissent d'herbe et les loups se nourissent de lapins. Un loup mange un lapin (10 UN) s'il est dans son voisisnage. 

Le métabolisme de chaque animal consomme 2 UN par UT pour les loups et 3 UN / UT pour les lapins. Un animal meurt s'il est trop vieux (25 UT pour les lapins, 50 UT pour les loups) ou si son métabolisme devient négatif.
Ce métabolisme ne peut pas dépasser une certaine valeur (45 UN pour les lapins et 200 UN pour les loups)
Un animal se reproduit avec une probabilité de 50% s'il est suffisamment nourri (40 UN pour les lapins et 120 UN pour les loups) ou s'il est suffisamment agé (10 UT). Un lapin ne peut pas se reproduire si un loup est dans son voisinage. 

![image](https://user-images.githubusercontent.com/46868436/188280905-cf23338a-2f83-48d0-b084-4f7da7b38c16.png)
