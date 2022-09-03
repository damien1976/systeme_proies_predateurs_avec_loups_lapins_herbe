from random import shuffle, choice
import pygame
import time
import sys

# Grille
taille_x=20
taille_y=20
blockSize = 20 #Set the size of the grid block
WINDOW_HEIGHT = blockSize*taille_x
WINDOW_WIDTH = blockSize*taille_y
nb_loups=5
nb_lapins=15

# Etats du nombre de lapins et de loups
X=[]
Y=[]
Z=[]

# Liste des couleurs
WHITE=(255,255,255)
BLACK=(0,0,0)
colors=[(255,255,255), (150,255,200),(150,255,150),(150,255,100),(0,255,100),(0,255,50), (0,255,0),(0,200,0),(0,150,0), (0,100,0), (0,50,0) ]

pygame.init()
SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Jeu de la vie')
SCREEN.fill(WHITE)

class loup():
    def __init__(self):
        self.age=0
        self.metabolisme=100
        self.just_moved=0 # 0 pas déplacé, 1 vient juste d'être déplacé.
        self.just_given_birth=0 # 1 vient de donner naissance à un nouvel animal 0 le contraire

    def deplace(self):
         return choice(['W', 'E', 'S', 'N'])
        

    def reproduire(self):
        # Reproduction possible (voir si de la place disponible pour mettre le nouveau né dans grille)
        return self.just_given_birth==0 and self.age>=10 and self.metabolisme>=120 and choice(['O', 'N'])=='O'

    def __str__(self):
        return 'loup'

    def __del__(self):
        print("Un loup en moins")

class lapin():
    def __init__(self):
        self.age=0
        self.metabolisme=20
        self.just_moved=0 # 0 pas déplacé, 1 vient juste d'être déplacé.
        self.just_given_birth=0 # 1 vient de donner naissance à un nouvel animal 0 le contraire

    def deplace(self):
        return choice(['W', 'E', 'S', 'N'])

    def reproduire(self):
        # Reporduction possible (voir si de la place disponible pour mettre le nouveau né
        # dans grille et si pas de loup dans voisinage)
        return self.just_given_birth==0 and self.age>=10 and choice(['O', 'N'])=='O' # and self.metabolisme>=40

    def __str__(self):
        return 'lapin'

    def __del__(self):
        print("Un lapin en moins")

class herbe():
    def __init__(self):
        self.metabolisme=20 # max 100
    
    def couleur(self):
        return colors[self.metabolisme//10]

    def encadre(self,x):
        if x<0:
            return 0
        elif x>255:
            return 255
        else:
            return x
        
class grille():
    def __init__(self, taille_x, taille_y, nb_loups, nb_lapins):
        self.taille_x=taille_x
        self.taille_y=taille_y
        self.nb_lapins=nb_lapins
        self.nb_loups=nb_loups
        self.animaux=[]
        self.img_loup=pygame.image.load('wolf.gif')
        self.img_lapin=pygame.image.load('rabbit.gif')
        self.initialise_loups_lapins()

    def initialise_loups_lapins(self):
        l=list(range(self.taille_x*self.taille_y))
        shuffle(l)
        
        self.animaux=[]
        for i in range(self.taille_x):
            liste=[]
            for j in range(self.taille_y):
                liste.append([herbe(), None, None])
            self.animaux.append(liste)

        for i in l[:nb_loups]:
            self.animaux[i%self.taille_x][i//self.taille_y][1]=loup() 
            
        for i in l[nb_loups:nb_loups+nb_lapins]:
            self.animaux[i%self.taille_x][i//self.taille_y][2]=lapin()

    def reproduction(self):
        for i in range(self.taille_x):
            for j in range(self.taille_y):
                animal = self.animaux[i][j][1] # cas des loups

                # il y a un loup et il peut se reproduire : On regarde les cases voisines (Une case libre pour le nouveau né)
                if animal != None and animal.reproduire():
                    # A gauche
                    
                    if self.est_dans_grille(i-1, j) and self.animaux[i-1][j][1]==None and self.animaux[i-1][j][2]==None:
                        self.animaux[i-1][j][1]=loup() # on crée un loup
                        self.nb_loups+=1 # On met à jour le nombre de loups
                        self.animaux[i-1][j][1].just_given_birth=1 # il vient de naître
                        self.animaux[i-1][j][1].just_moved=1 # Il ne peut pas se déplacer. 
                        animal.just_given_birth=1 # l'animal parent vient de mettre bas
                        animal.just_moved=1 # l'animal parent ne peut pas se déplacer
                        self.animaux[i][j][1]=animal
                
                    elif self.est_dans_grille(i-1, j-1) and self.animaux[i-1][j-1][1]==None and self.animaux[i-1][j-1][2]==None: # à gauche
                        self.animaux[i-1][j-1][1]=loup() # on crée un loup
                        self.nb_loups+=1 # On met à jour le nombre de loups
                        self.animaux[i-1][j-1][1].just_given_birth=1 # il vient de naître
                        self.animaux[i-1][j-1][1].just_moved=1 # Il ne peut pas se déplacer. 
                        animal.just_given_birth=1 # l'animal parent vient de mettre bas
                        animal.just_moved=1 # l'animal parent ne peut pas se déplacer
                        self.animaux[i][j][1]=animal

                    elif self.est_dans_grille(i-1, j+1) and self.animaux[i-1][j+1][1]==None and self.animaux[i-1][j+1][2]==None: # à gauche
                        self.animaux[i-1][j+1][1]=loup() # on crée un loup
                        self.nb_loups+=1 # On met à jour le nombre de loups
                        self.animaux[i-1][j+1][1].just_given_birth=1 # il vient de naître
                        self.animaux[i-1][j+1][1].just_moved=1 # Il ne peut pas se déplacer. 
                        animal.just_given_birth=1 # l'animal parent vient de mettre bas
                        animal.just_moved=1 # l'animal parent ne peut pas se déplacer
                        self.animaux[i][j][1]=animal

                    # A droite
                    elif self.est_dans_grille(i+1, j) and self.animaux[i+1][j][1]==None and self.animaux[i+1][j][2]==None:
                        self.animaux[i+1][j][1]=loup() # on crée un loup
                        self.nb_loups+=1 # On met à jour le nombre de loups
                        self.animaux[i+1][j][1].just_given_birth=1 # il vient de naître
                        self.animaux[i+1][j][1].just_moved=1 # Il ne peut pas se déplacer. 
                        animal.just_given_birth=1 # l'animal parent vient de mettre bas
                        animal.just_moved=1 # l'animal parent ne peut pas se déplacer
                        self.animaux[i][j][1]=animal
                
                    elif self.est_dans_grille(i+1, j-1) and self.animaux[i+1][j-1][1]==None and self.animaux[i+1][j-1][2]==None: # à gauche
                        self.animaux[i+1][j-1][1]=loup() # on crée un loup
                        self.nb_loups+=1 # On met à jour le nombre de loups
                        self.animaux[i+1][j-1][1].just_given_birth=1 # il vient de naître
                        self.animaux[i+1][j-1][1].just_moved=1 # Il ne peut pas se déplacer. 
                        animal.just_given_birth=1 # l'animal parent vient de mettre bas
                        animal.just_moved=1 # l'animal parent ne peut pas se déplacer
                        self.animaux[i][j][1]=animal

                    elif self.est_dans_grille(i+1, j+1) and self.animaux[i+1][j+1][1]==None and self.animaux[i+1][j+1][2]==None: # à gauche
                        self.animaux[i+1][j+1][1]=loup() # on crée un loup
                        self.nb_loups+=1 # On met à jour le nombre de loups
                        self.animaux[i+1][j+1][1].just_given_birth=1 # il vient de naître
                        self.animaux[i+1][j+1][1].just_moved=1 # Il ne peut pas se déplacer. 
                        animal.just_given_birth=1 # l'animal parent vient de mettre bas
                        animal.just_moved=1 # l'animal parent ne peut pas se déplacer
                        self.animaux[i][j][1]=animal

                    # Dessus-dessous
                    elif self.est_dans_grille(i, j-1) and self.animaux[i][j-1][1]==None and self.animaux[i][j-1][2]==None: # à gauche
                        self.animaux[i][j-1][1]=loup() # on crée un loup
                        self.nb_loups+=1 # On met à jour le nombre de loups
                        self.animaux[i][j-1][1].just_given_birth=1 # il vient de naître
                        self.animaux[i][j-1][1].just_moved=1 # Il ne peut pas se déplacer. 
                        animal.just_given_birth=1 # l'animal parent vient de mettre bas
                        animal.just_moved=1 # l'animal parent ne peut pas se déplacer
                        self.animaux[i][j][1]=animal

                    elif self.est_dans_grille(i, j+1) and self.animaux[i][j+1][1]==None and self.animaux[i][j+1][2]==None: # à gauche
                        self.animaux[i][j+1][1]=loup() # on crée un loup
                        self.nb_loups+=1 # On met à jour le nombre de loups
                        self.animaux[i][j+1][1].just_given_birth=1 # il vient de naître
                        self.animaux[i][j+1][1].just_moved=1 # Il ne peut pas se déplacer. 
                        animal.just_given_birth=1 # l'animal parent vient de mettre bas
                        animal.just_moved=1 # l'animal parent ne peut pas se déplacer
                        self.animaux[i][j][1]=animal


                animal = self.animaux[i][j][2] # cas des lapins
                # il y a un loup et il peut se reproduire : On regarde les cases voisines (Une case libre pour le nouveau né)
                cpt_loups=0
                if self.est_dans_grille(i-1, j-1) and self.animaux[i-1][j-1][1]!=None:
                    cpt_loups+=1
                if self.est_dans_grille(i-1, j) and self.animaux[i-1][j][1]!=None:
                    cpt_loups+=1
                if self.est_dans_grille(i-1, j+1) and self.animaux[i-1][j+1][1]!=None:
                    cpt_loups+=1
                if self.est_dans_grille(i, j-1) and self.animaux[i][j-1][1]!=None:
                    cpt_loups+=1
                if self.est_dans_grille(i, j+1) and self.animaux[i][j+1][1]!=None:
                    cpt_loups+=1
                if self.est_dans_grille(i+1, j-1) and self.animaux[i+1][j-1][1]!=None:
                    cpt_loups+=1
                if self.est_dans_grille(i+1, j) and self.animaux[i+1][j][1]!=None:
                    cpt_loups+=1
                if self.est_dans_grille(i+1, j+1) and self.animaux[i+1][j+1][1]!=None:
                    cpt_loups+=1
                    
                if cpt_loups==0 and animal != None and animal.reproduire():
                    # A gauche
                    if self.est_dans_grille(i-1, j) and self.animaux[i-1][j][2]==None:
                        self.animaux[i-1][j][2]=lapin() # on crée un lapin
                        self.nb_lapins+=1 # On met à jour le nombre de lapins
                        self.animaux[i-1][j][2].just_given_birth=1 # il vient de naître
                        self.animaux[i-1][j][2].just_moved=1 # Il ne peut pas se déplacer. 
                        animal.just_given_birth=1 # l'animal parent vient de mettre bas
                        animal.just_moved=1 # l'animal parent ne peut pas se déplacer
                        self.animaux[i][j][2]=animal
                
                    elif self.est_dans_grille(i-1, j-1) and self.animaux[i-1][j-1][2]==None: # à gauche
                        self.animaux[i-1][j-1][2]=lapin() # on crée un lapin
                        self.nb_lapins+=1 # On met à jour le nombre de lapins
                        self.animaux[i-1][j-1][2].just_given_birth=1 # il vient de naître
                        self.animaux[i-1][j-1][2].just_moved=1 # Il ne peut pas se déplacer. 
                        animal.just_given_birth=1 # l'animal parent vient de mettre bas
                        animal.just_moved=1 # l'animal parent ne peut pas se déplacer
                        self.animaux[i][j][2]=animal

                    elif self.est_dans_grille(i-1, j+1) and self.animaux[i-1][j+1][2]==None: # à gauche
                        self.animaux[i-1][j+1][2]=lapin() # on crée un lapin
                        self.nb_lapins+=1 # On met à jour le nombre de lapins
                        self.animaux[i-1][j+1][2].just_given_birth=1 # il vient de naître
                        self.animaux[i-1][j+1][2].just_moved=1 # Il ne peut pas se déplacer. 
                        animal.just_given_birth=1 # l'animal parent vient de mettre bas
                        animal.just_moved=1 # l'animal parent ne peut pas se déplacer
                        self.animaux[i][j][2]=animal

                    # A droite
                    elif self.est_dans_grille(i+1, j) and self.animaux[i+1][j][2]==None:
                        self.animaux[i+1][j][2]=lapin() # on crée un lapin
                        self.nb_lapins+=1 # On met à jour le nombre de lapins
                        self.animaux[i+1][j][2].just_given_birth=1 # il vient de naître
                        self.animaux[i+1][j][2].just_moved=1 # Il ne peut pas se déplacer. 
                        animal.just_given_birth=1 # l'animal parent vient de mettre bas
                        animal.just_moved=1 # l'animal parent ne peut pas se déplacer
                        self.animaux[i][j][2]=animal
                
                    elif self.est_dans_grille(i+1, j-1) and self.animaux[i+1][j-1][2]==None: # à gauche
                        self.animaux[i+1][j-1][2]=lapin() # on crée un lapin
                        self.nb_lapins+=1 # On met à jour le nombre de lapins
                        self.animaux[i+1][j-1][2].just_given_birth=1 # il vient de naître
                        self.animaux[i+1][j-1][2].just_moved=1 # Il ne peut pas se déplacer. 
                        animal.just_given_birth=1 # l'animal parent vient de mettre bas
                        animal.just_moved=1 # l'animal parent ne peut pas se déplacer
                        self.animaux[i][j][2]=animal

                    elif self.est_dans_grille(i+1, j+1) and self.animaux[i+1][j+1][2]==None: # à gauche
                        self.animaux[i+1][j+1][2]=lapin() # on crée un lapin
                        self.nb_lapins+=1 # On met à jour le nombre de lapins
                        self.animaux[i+1][j+1][2].just_given_birth=1 # il vient de naître
                        self.animaux[i+1][j+1][2].just_moved=1 # Il ne peut pas se déplacer. 
                        animal.just_given_birth=1 # l'animal parent vient de mettre bas
                        animal.just_moved=1 # l'animal parent ne peut pas se déplacer
                        self.animaux[i][j][2]=animal

                    # Dessus-dessous
                    elif self.est_dans_grille(i, j-1) and self.animaux[i][j-1][2]==None: # à gauche
                        self.animaux[i][j-1][2]=lapin() # on crée un lapin
                        self.nb_lapins+=1 # On met à jour le nombre de lapins
                        self.animaux[i][j-1][2].just_given_birth=1 # il vient de naître
                        self.animaux[i][j-1][2].just_moved=1 # Il ne peut pas se déplacer. 
                        animal.just_given_birth=1 # l'animal parent vient de mettre bas
                        animal.just_moved=1 # l'animal parent ne peut pas se déplacer
                        self.animaux[i][j][2]=animal

                    elif self.est_dans_grille(i, j+1) and self.animaux[i][j+1][2]==None: # à gauche
                        self.animaux[i][j+1][2]=lapin() # on crée un lapin
                        self.nb_lapins+=1 # On met à jour le nombre de lapins
                        self.animaux[i][j+1][2].just_given_birth=1 # il vient de naître
                        self.animaux[i][j+1][2].just_moved=1 # Il ne peut pas se déplacer. 
                        animal.just_given_birth=1 # l'animal parent vient de mettre bas
                        animal.just_moved=1 # l'animal parent ne peut pas se déplacer
                        self.animaux[i][j][2]=animal
                
    

    def deplacements(self):
        for i in range(self.taille_x):
            for j in range(self.taille_y):
                for k in [1,2]:
                    if self.animaux[i][j][k] != None: # il y a un animal
                        animal=self.animaux[i][j][k]
                        direction=animal.deplace()
                        
                        if direction=='E' and self.est_dans_grille(i-1, j) and self.animaux[i-1][j][k]==None and animal.just_moved==0: # à gauche
                            animal.just_moved=1
                            self.animaux[i-1][j][k]=animal
                            self.animaux[i][j][k]=None
                            
                        if direction=='W' and self.est_dans_grille(i+1, j) and self.animaux[i+1][j][k]==None and animal.just_moved==0: # à droite
                            animal.just_moved=1
                            self.animaux[i+1][j][k]=animal
                            self.animaux[i][j][k]=None
                            
                        if direction=='N' and self.est_dans_grille(i, j+1) and self.animaux[i][j+1][k]==None and animal.just_moved==0: # haut
                            animal.just_moved=1
                            self.animaux[i][j+1][k]=animal
                            self.animaux[i][j][k]=None
                            
                        if direction=='S' and self.est_dans_grille(i, j-1) and self.animaux[i][j-1][k]==None and animal.just_moved==0: # bas
                            animal.just_moved=1
                            self.animaux[i][j-1][k]=animal
                            self.animaux[i][j][k]=None

        for i in range(self.taille_x):
            for j in range(self.taille_y):
                for k in [1,2]:
                    if self.animaux[i][j][k] != None: # il y a un animal
                        self.animaux[i][j][k].just_moved=0 # remise à 0 de l'état "vient d'être déplacé".
                        self.animaux[i][j][k].just_given_birth=0 # Remise à 0 de l'état "vient de mettre bas" ou "vient de naitre"
                        
                        
        return

     
                    
    def avance_generation(self):
        # Reproduction
        self.reproduction()
        
        # mettre à jour le nombre de lapins / loups après déplacement
        self.deplacements()
        
        # Mise à jour metabolisme / âge / décés
        for i in range(self.taille_x):
            for j in range(self.taille_y):
                if self.animaux[i][j][1] != None: # c'est un loup
                    loup=self.animaux[i][j][1]
                    loup.metabolisme-=2
                    loup.age+=1
                    if loup.age>=50 or loup.metabolisme<=0:
                        self.animaux[i][j][1]=None
                        self.nb_loups-=1 # un loup meurt
                    else:
                        self.animaux[i][j][1]=loup
                        
                if self.animaux[i][j][2] != None: # c'est un lapin
                    lapin=self.animaux[i][j][2]
                    lapin.metabolisme-=3
                    lapin.age+=1

                    herbe=self.animaux[i][j][0]
                    herbe.metabolisme-=3
            
                    if herbe.metabolisme<=0:
                        herbe.metabolisme=0
                    else:
                        lapin.metabolisme+=3
                        if lapin.metabolisme>=45:
                            lapin.metabolisme=45
                    
                    self.animaux[i][j][0]=herbe
                    self.animaux[i][j][2]=lapin
                    
                    if lapin.age>=25 or lapin.metabolisme<=0:
                        self.animaux[i][j][2]=None
                        self.nb_lapins-=1 # On met à jour le nombre de lapins
                    else:
                        self.animaux[i][j][2]=lapin
                    
                if self.animaux[i][j][1] != None and self.animaux[i][j][2] != None: # lapin + loup sur la même cellule
                    loup=self.animaux[i][j][1]
                    self.animaux[i][j][2]=None
                    loup.metabolisme+=10
                    if loup.metabolisme>=200:
                        loup.metabolisme=200
                    self.animaux[i][j][1]=loup
                    self.nb_lapins-=1 # On met à jour le nombre de lapins

                if self.animaux[i][j][2]==None: # Pas de lapin
                    # Problème de l'herbe
                    herbe=self.animaux[i][j][0]
                    herbe.metabolisme+=1
                    if herbe.metabolisme>=100:
                        herbe.metabolisme=100
                    
                    self.animaux[i][j][0]=herbe
                              
        return 
                        
    def drawGrid(self):
        for i in range(self.taille_x):
            for j in range(self.taille_y):
                herbe=self.animaux[i][j][0]
                rect=pygame.Rect(i*blockSize, j*blockSize, blockSize, blockSize)
                pygame.display.get_surface().fill(herbe.couleur(), rect)
                if self.animaux[i][j][1]!=None:
                    SCREEN.blit(self.img_loup, (i*blockSize, j*blockSize))
                elif self.animaux[i][j][2]!=None:
                    SCREEN.blit(self.img_lapin, (i*blockSize, j*blockSize))    
                pygame.draw.rect(SCREEN, BLACK, rect, 1)

    def est_dans_grille(self, i, j):
        if i>=0 and j>=0 and i<self.taille_x and j<self.taille_y:
            return True
        else:
            return False

g=grille(taille_x, taille_y, nb_loups, nb_lapins)
cpt=0 # compte les générations
while True:
    g.drawGrid()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    time.sleep(1)
    g.avance_generation()
    X.append(cpt) # On recupére les générations (ligne de temps)
    Y.append(g.nb_lapins) # On récupère le nombre de lapins à chaque génération.
    Z.append(g.nb_loups) # On récupère le nombre de loups à chaque génération.
    cpt+=1 # Avance d'une génération
    
