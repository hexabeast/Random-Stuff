"""
Script principal; c'est celui qu'il faut executer.
Il utilise la bibliothèque 3D vPython pour le rendu et le déplacement
de petits parallélépipèdes rectangles de couleurs différentes formant le cube.

Le module "resolution" permet de connaître les suites de coups à faire
pour avancer dans la résolution du cube en utilisant l'algorithme dit
'couche par couche'

Le module "reconaissance" permet, associé à une réalisation matérielle
(une boite en carton avec webcam, lampe et support pour le cube à l'intérieur),
permet de scanner un cube réel afin d'en réaliser une copie virtuelle afin
de le résoudre en utilisant l'algorithme.

Seules les parties traitant de la résolution du cube seront vraiment commentées,
pas les parties du code gérant l'affichage 3D.


On définira "une couleur" comme un entier de 0 à 5,
0 <=> Rouge
1 <=> Orange
2 <=> Bleu
3 <=> Vert
4 <=> Jaune
5 <=> Blanc
"""

#Imports:
import debug
import time
debug.stopPrinting()
from visual import *
debug.startPrinting()
from random import randint
import resolution

camera = False

if camera:
    import reconnaissance

#Taille du cube (3x3x3)
taille = 3
resolution.taille = taille

#Variables utiles pour la partie graphique de l'algorithme:

scene = display(title='Rubiks Cube',x=0, y=0, width=800, height=800,center=(0,0,0), background=(1,1,1))

scene.forward = (1,-1,-1)
scene.range = 12
scene.lights = (distant_light(direction=(1,1,0.8), color=color.gray(0.6)),
                distant_light(direction=(1,-1,-0.8), color=color.gray(0.6)),
                distant_light(direction=(-1,1,-0.8), color=color.gray(0.6)),
                distant_light(direction=(-1,-0.9,0.8),color=color.gray(0.6)))
scene.ambiant = 0.6
scene.fov = pi/3.5


forward = (-1,0,-1)

position = vector(0,0,0)
cube = []

rx = -1
ry = -1
rz = -1

angle = 0

morceaux = [[[None for l in range(taille)] for i in range(taille)] for j in range(taille)]

entreeutilisateur= -1

#Simple information : le nombre de coups qui ont été nécessaires à la résolution
perf = 0

#Liste de faces sous la forme d'une liste de 6 faces
#Une face étant une liste de 3 lignes
#Une ligne étant une liste de 3 couleurs
#Une couleur étant un entier valant de 0 à 5
faces = [[[0 for l in range(taille)] for i in range(taille)] for j in range(6)]

#Utilisé lors des rotations de faces
tempfaces = [[[0 for l in range(taille)] for i in range(taille)] for j in range(6)]

#Liste de coups passés
backup = []

#Liste de coups à venir
coups = []



# FONCTIONS ET CLASSES
################################################################

#Fonctions non commentées (car rien à voir avec l'algorithme en lui-même):
def recon():
    global faces
    fini = False
    while not fini:
        print("T pour scanner une face, R pour annuler")
        if keystopn()==1:
            print("Scan...")
            if camera:
                im = reconnaissance.photo(False)
                faces[im[1][1]] = im
            else:
                print("Script de reconnaissance désactivé")
        else:
            fini = True
        constructionCube()

    checklist = [0 for i in range(6)]
    for i in range(6):
        for j in range(3):
            for k in range(3):
                checklist[faces[i][j][k]]+=1
    for n in checklist:
        if n != 9:
            print("Erreur de scan! Recommencez")
            recon()
            break

def coordonnees(face,x,y):
    return resolution.coordonnees(face,x,y)

class morceau:

    def delete(self):
        if self.cube != None:
            self.cube.visible = False
            del self.cube
        for c in self.carres:
            c.visible = False
            del c
        self.f.visible = False
        del self.f
        del self.carres
        del self.carrespos
        self.carres = []

    def reconstruct(self,x,y,z,carrepos, carrecouleurs):
        if self.initie:
            self.delete()
        self.x = x
        self.y = y
        self.z = z

        self.f = frame()
        self.f.pos = (x,y,z)

        self.cube = None
        if len(carrecouleurs)>0: self.cube = box(frame=self.f, pos=(0,0,0), color = (0.2,0.2,0.2), length=3, height=3, width=3)

        self.carres = []
        self.carrespos = carrepos
        for i in range(len(self.carrespos)):
            l = 2.8
            h = 2.8
            w = 2.8
            if abs(self.carrespos[i].x-0)>0.1:
                l = 0.15
            if abs(self.carrespos[i].y-0)>0.1:
                h = 0.15
            if abs(self.carrespos[i].z-0)>0.1:
                w = 0.15
                
            self.carres.append(box(frame=self.f, pos=self.carrespos[i], color = carrecouleurs[i], length=l, height=h, width=w))
            
    def __init__(self,x,y,z,carrepos, carrecouleurs):
        self.initie = False
        self.reconstruct(x,y,z,carrepos, carrecouleurs)
        self.initie = True
            


def printface(n):
    print()
    for i in range(taille-1,-1,-1):
        s = ""
        for j in range(taille):
            s+=str(faces[n][j][i])+','
        print(s)

def printcube():
    print('------------------')
    for i in range(6):
        printface(i)
    print('------------------')

def keystop(k):
    key = ''
    while(key!=k):
        key = scene.kb.getkey()

def keystopn():
    n = -1
    while n<0:
        key = scene.kb.getkey()
        if key == 'r':
            n = 0
        elif key == 't':
            n = 1
        elif key == 'y':
            n = 2
        elif key == 'b' and len(backup)>0:
            n = 3
    return n

def confirmRotate(speed):
    
    global rx,ry,rz, taille
    
    if rx>=0:
        for i in range(taille):
            for j in range(taille):
                morceaux[rx][i][j].f.rotate(angle=speed, axis=(1,0,0), origin=(0,0,0)) 
    elif ry>=0:
        for i in range(taille):
            for j in range(taille):
                morceaux[i][ry][j].f.rotate(angle=speed, axis=(0,1,0), origin=(0,0,0))
    elif rz>=0:
        for i in range(taille):
            for j in range(taille):
                morceaux[i][j][rz].f.rotate(angle=speed, axis=(0,0,1), origin=(0,0,0))

def nombreVersCouleur(n):
    if n==0:
        return (0.85,0.05,0.15)#ROUGE
    elif n==1:
        return (1,0.5,0)#ORANGE
    elif n==2:
        return (0,0.4,1)#BLEU
    elif n==3:
        return (0,0.8,0.25) #VERT
    elif n==4:
        return (1,0.9,0)#JAUNE
    elif n==5:
        return (1,1,1)#BLANC
    else:
        print("ERREUR : COULEUR NON EXISTANTE")
        
 

def constructionCube():
    global morceaux, faces
    
    for i in range(taille):
        for j in range(taille):
            for k in range(taille):
                couleurs = []
                cpos = []
                
                if i == taille-1:
                    couleurs.append(nombreVersCouleur(faces[0][taille-1-k][j]))
                    cpos.append(vector(1.5,0,0))
                if i == 0:
                    couleurs.append(nombreVersCouleur(faces[1][k][j]))
                    cpos.append(vector(-1.5,0,0))

                if j == taille-1:
                    couleurs.append(nombreVersCouleur(faces[4][taille-1-k][taille-1-i]))
                    cpos.append(vector(0,1.5,0))
                if j == 0:
                    couleurs.append(nombreVersCouleur(faces[5][taille-1-k][i]))
                    cpos.append(vector(0,-1.5,0))

                if k == taille-1:
                    couleurs.append(nombreVersCouleur(faces[2][i][j]))
                    cpos.append(vector(0,0,1.5))
                if k == 0:
                    couleurs.append(nombreVersCouleur(faces[3][taille-1-i][j]))
                    cpos.append(vector(0,0,-1.5))

                if morceaux[i][j][k] != None:
                    morceaux[i][j][k].reconstruct((i-(taille-1)*0.5)*3,(j-(taille-1)*0.5)*3,(k-(taille-1)*0.5)*3,cpos,couleurs)
                else:
                    morceaux[i][j][k] = morceau((i-(taille-1)*0.5)*3,(j-(taille-1)*0.5)*3,(k-(taille-1)*0.5)*3,cpos,couleurs)


#Fonctions commentées:

def rotateFace(face,n):
    """
    Entree: face une couleur sous forme d'entier, n un entier
    Cette fonction tourne la face de couleur "face" n fois
    """
    if face==0:
        rotate2(0,taille-1,-n)
    elif face==1:
        rotate2(0,0,n)

    elif face==2:
        rotate2(2,taille-1,-n)
    elif face==3:
        rotate2(2,0,n)

    elif face==4:
        rotate2(1,taille-1,-n)
    elif face==5:
        rotate2(1,0,n)

def rotate2(direction, rangee, n):
    """
    Entree: direction, rangee et n des entiers
    Cette fonction tourne la portion du cube selon la direction et la rangee donnee
    n fois
    """
    if direction == 0:
        rotate(rangee,-1,-1,n)
    elif direction == 1:
        rotate(-1,rangee,-1,n)
    else:
        rotate(-1,-1,rangee,n)



def rotate(x,y,z,n):
    """
    Entree : x, y et z entiers. Un seul de ces entiers devra etre non
    nul.
    Cette fonction tourne la portion de cube de rangee x, y ou z selon la direction
    choisie, et ce n fois
    """
    
    global rx, ry, rz, angle, faces, tempfaces, taille
    rx = x
    ry = y
    rz = z

    if y==1 or x==1 or z==1:
        print("ATTENTION : MILIEU TOURNE")

    while n < -1:
        n +=4
    while n > 2:
        n-=4


    angle = n*pi/2

    while n < 0:
        n +=4
    while n > 3:
        n-=4
    
    
    for l in range(n):
        for i in range(taille):
            for j in range(taille):
                for k in range(6):
                    tempfaces[k][i][j] = faces[k][i][j]


           
        if x>=0:
            for i in range(taille):
                for j in range(taille):
                    if x == 0:
                        tempfaces[1][j][taille-1-i] = faces[1][i][j]
                    if x == taille-1:
                        tempfaces[0][i][j] = faces[0][j][taille-1-i]

            for i in range(taille*4):
                coordsD = coordonnees(2,x,i+taille)
                coordsA = coordonnees(2,x,i)
                tempfaces[coordsA[0]][coordsA[1]][coordsA[2]] = faces[coordsD[0]][coordsD[1]][coordsD[2]]
            


        elif y>=0:
            for i in range(taille):
                for j in range(taille):
                    if y == 0:
                        tempfaces[5][j][taille-1-i] = faces[5][i][j]
                    if y == taille-1:
                        tempfaces[4][i][j] = faces[4][j][taille-1-i]
            for i in range(taille*4):
                coordsD = coordonnees(0,i-taille,y)
                coordsA = coordonnees(0,i,y)
                tempfaces[coordsA[0]][coordsA[1]][coordsA[2]] = faces[coordsD[0]][coordsD[1]][coordsD[2]]



        elif z>=0:
            for i in range(taille):
                for j in range(taille):
                    if z == 0:
                        tempfaces[3][j][taille-1-i] = faces[3][i][j]
                        
                    if z == taille-1:
                        tempfaces[2][i][j] = faces[2][j][taille-1-i]

            for i in range(taille*4):
                coordsD = coordonnees(0,taille-1-z,i-taille)
                coordsA = coordonnees(0,taille-1-z,i)
                tempfaces[coordsA[0]][coordsA[1]][coordsA[2]] = faces[coordsD[0]][coordsD[1]][coordsD[2]]



                    
        for i in range(taille):
            for j in range(taille):
                for k in range(6):
                    faces[k][i][j] = tempfaces[k][i][j]



def melanger(n):
    """
    Cette fonction melange le cube en realisant n coups aleatoires
    """
    global angle, taille, backup, perf

    for i in range(n):
        m = randint(0,5)
        p = randint(1,3)
        if p == 3:
            p = -1

        rotateFace(m,p)
        
        confirmRotate(angle)
        angle = 0
        backup = []
        
    constructionCube()
    perf = 0




def reinitCube():
    """
    Cette fonction remet le cube dans son état "résolu"
    """
    for i in range(taille):
        for j in range(taille):
            for k in range(6):
                faces[k][i][j] = k
    constructionCube()

######################################################################
#PARTIE PRINCIPALE DU SCRIPT#

#On met le cube dans son état "résolu"
reinitCube()

#Boucle pas vraiment infinie, lorsque l'on fermera la fenetre 3D vPython,
#on en sortira.
while(True):
    #Si "angle" est non nul, alors on doit faire des trucs graphiques
    if angle!=0:
        oangle = angle

        speed = 0.15
        if angle<0:
            speed = -speed

        angle-=speed

        fini = False
        if oangle*angle<=0:
            speed = speed+angle
            angle = 0
            fini = True

        confirmRotate(speed)

        if fini:
            constructionCube()

    #Sinon on determine la prochaine action a effectuer
    else:
        #Si il n'y a plus de coups a jouer:
        if len(coups) == 0:
            #On utilise le module resolution pour connaitre les prochains coups
            #selon la configuration actuelle du cube
            coups = resolution.coup(faces)

            #Si le module resolution n'a pas trouvé de coups a jouer, le cube est terminé
            if len(coups) == 0:
                #On vérifie le bon déroulement de la résolution, même si c'est théoriquement inutile
                for i in range(6):
                    for j in range(3):
                        for k in range(3):
                            assert faces[i][j][k] == i,"DEFAILLANCE DE L'ALGORITHME DE RESOLUTION"
                                
                #On affiche le nombre de coups qui ont été nécessaire à la résolution
                if perf>0:
                    print('Nombre de coups pour terminer le cube: '+str(perf))

                #On demande a l'utilisateur ce qu'il veut faire
                print('Appuyez sur R pour melanger\nOu sur T pour scanner le cube\n---------------------------------') 
                if keystopn() == 1:
                    #Scanner un cube reel
                    recon()
                else:
                    #Melanger le cube virtuel (1000 mouvements aleatoires)
                    melanger(1000)

                #On demande a l'utilisateur ce qu'il veut faire
                print("Appuyez sur R pour passer au coup suivant;\nAppuyez sur B pour revenir au coup précédent\nAppuyez sur T pour passer a l'etape suivante;\nAppuyez sur Y pour terminer le cube\n---------------------------------")
                entreeutilisateur = 0
                coups = resolution.coup(faces)
                
            
            if entreeutilisateur == 1 and resolution.etape != resolution.derniereEtape:
                entreeutilisateur = keystopn()
        
        if entreeutilisateur == 0:
            entreeutilisateur = keystopn()

        #Si il reste des mouvements a effectuer on les effectue
        if len(coups)>0:
            c = None
            #Si l'utilisateur a choisi de revenir en arriere:
            if entreeutilisateur == 3:
                entreeutilisateur = 0
                c = backup.pop()
                coups.insert(0,(c[0],-c[1]))
                perf-=1
            #Sinon:
            else:
                c = coups.pop(0)
                backup.append((c[0],-c[1]))
                perf+=1
            
            rotateFace(c[0],c[1])
            
    rate(60)


