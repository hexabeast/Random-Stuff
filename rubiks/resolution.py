"""
Ce module permet de connaître les suites de coups à faire
pour avancer dans la résolution du cube en utilisant l'algorithme dit
'couche par couche'

On définira "une couleur" comme un entier de 0 à 5,
0 <=> Rouge
1 <=> Orange
2 <=> Bleu
3 <=> Vert
4 <=> Jaune
5 <=> Blanc

On fera dans l'ordre:
-La face blanche et sa couronne (2 etapes)
-La deuxieme couronne (1 etape)
-La face jaune (4 etapes)

Avec un total de 7 étapes

Ce module n'a d'utilité qu'en étant exploité par un autre script, il n'est pas autonome.
"""


#Taille du cube
taille = 3

#Etape actuelle et etape atteinte au dernier coup
derniereEtape = 1
etape = 1

#Liste de faces sous la forme d'une liste de 6 faces
#Une face étant une liste de 3 lignes
#Une ligne étant une liste de 3 couleurs
#Une couleur étant un entier valant de 0 à 5
faces = None
#Cette liste sera définie par un script extérieur.

def coordonnees(face,x,y):
    """
    Entree : Les coordonnees x et y d'une facette en fonction de la face "face"
    ces coordonnees pourront exceder la taille de la face, par exemple avec x = 4
    on aura une facette n'appartenant pas vraiment à la face donnée en argument
    mais a une face adjacente.
    
    Sortie : La face sur laquelle se trouve réellement cette facette, ainsi que ses coordonnees sur cette face,
    qui cette-fois ci seront bornées par la taille de la face.
    """
    if x<0:
        x+=taille
        nface = 0
        if face == 1:
            nface = 3
        elif face == 2:
            nface = 1
        elif face == 0:
            nface = 2
        elif face == 3:
            nface = 0
        elif face == 4:
            x,y = taille-1-y,x
            nface = 2
        elif face == 5:
            x,y = y,taille-1-x
            nface = 2
        return coordonnees(nface,x,y)
    
    elif x>=taille:
        x-=taille
        nface = 0
        if face == 1:
            nface = 2
        elif face == 2:
            nface = 0
        elif face == 0:
            nface = 3
        elif face == 3:
            nface = 1
        elif face == 4:
            x,y = y,taille-1-x
            nface = 3
        elif face == 5:
            x,y = taille-1-y,x
            nface = 3
        return coordonnees(nface,x,y)

    elif y<0:
        y+=taille
        nface = 0
        if face == 1:
            x,y = taille-1-x,taille-1-y
            nface = 5
        elif face == 2:
            x,y = taille-1-y,x
            nface = 5
        elif face == 0:
            nface = 5
        elif face == 3:
            x,y = y,taille-1-x
            nface = 5
        elif face == 4:
            nface = 0
        elif face == 5:
            x,y = taille-1-x,taille-1-y
            nface = 1
        return coordonnees(nface,x,y)
    
    elif y>=taille:
        y-=taille
        nface = 0
        if face == 1:
            x,y = taille-1-x,taille-1-y
            nface = 4
        elif face == 2:
            x,y = y,taille-1-x
            nface = 4
        elif face == 0:
            nface = 4
        elif face == 3:
            x,y = taille-1-y,x
            nface = 4
        elif face == 4:
            x,y = taille-1-x,taille-1-y
            nface = 1
        elif face == 5:
            nface = 0
        return coordonnees(nface,x,y)

    return (face,x,y)
    
def coordface(face,x,y):
    """
    Même fonction que "coordonnees" a la différence près que celle-ci ne renvoie
    que la couleur de la facette visée et ni sa position ni sa face
    """
    global faces
    c = coordonnees(face,x,y)
    return faces[c[0]][c[1]][c[2]]

def optimisation(liste):
    """
    Cette etape réduit le nombre de coups
    """
    nliste = []
    if len(liste)>0:
        
        nliste.append(liste[0])
        for i in range(1,len(liste)):
            if liste[i][0] == nliste[len(nliste)-1][0]:
                nliste[len(nliste)-1] = (liste[i][0],liste[i][1]+nliste[len(nliste)-1][1])
            else:
                nliste.append(liste[i])

        for i in range(len(nliste)-1,-1,-1):
            while nliste[i][1]>2:
                nliste[i] = (nliste[i][0],nliste[i][1]-4)

            while nliste[i][1]<-2:
                nliste[i] = (nliste[i][0],nliste[i][1]+4)
                
            if nliste[i][1] == 0:
                nliste.pop(i)       
    return nliste

def coup(faces2):
    """
    Fonction qui sera appelée par un script extérieur
    """
    global faces, derniereEtape, etape
    faces = faces2
    derniereEtape = etape
    return optimisation(etape1())
    
def etape1():
    """
    Cette etape assemble la croix de la première face
    """
    global etape
    etape = 1
    
    passer = True

    malplace = -1

    for i in range(4):
        if coordface(i,1,-1) == 5:
            if faces[i][1][0] != i:
                malplace = i
                passer = False
        else:
            passer = False
    
    if passer:
        #Croix blanche déjà faite: on passe à l'étape 2
        return etape2()
    else:
        rotations = 0
        bienplaces = 0

        for k in range(4):
            cbp = 0
            for i in range(4):
                if coordface(i,1,0) == coordonnees(i,k*3+1,0)[0]:
                    if coordface(i,1,-1) == 5:
                        cbp+=1
            if cbp>bienplaces:
                rotations = k
                bienplaces = cbp

        if rotations>0:
            return [(5,rotations)]

        if malplace>=0:
            return [(malplace,1)]
        
        for i in range(3):
            for j in range(3):
                if (i == 1 or j == 1) and i!=j:
                    if faces[4][i][j] == 5:
                        adjface = coordface(4,2*i-1,2*j-1)
                        t = 0
                        cor = coordonnees(4,3*i-2,3*j-2)
                        while adjface != coordface(cor[0] , cor[1]+3*t, cor[2]):
                            t+=1
                        liste = []
                        for k in range(t):
                            liste.append((4,-1))
                        liste.append((adjface,1))
                        liste.append((adjface,1))
                        return liste

        for i in range(4):
            co = coordonnees(0,1+i*3,2)
            if faces[co[0]][co[1]][co[2]] == 5:
                adjface = coordface(co[0],co[1],co[2]+1)
                
                t = 0
                while adjface != coordface(co[0],co[1]+t*3,co[2]-1):
                    t+=1
                lface = coordonnees(adjface,-1,0)[0]
                    
                liste = []
                for k in range(t):
                    liste.append((4,-1))
                liste.append((4,1))
                liste.append((lface,1))
                liste.append((adjface,-1))
                liste.append((lface,-1))
                return liste

        for i in range(4):
            for j in range(2):
                if faces[i][j*2][1] == 5:
                    sens = j*2-1
                    return [(i,-sens), (4,1), (i,sens)]

        for i in range(4):
            if faces[i][1][0] == 5:
                return [(i,1)]
        
                                            

def etape2():
    """
    Cette etape termine la premiere face (avec la premiere couronne)
    """
    global etape
    etape = 2
    malplace = -1
    passer = True
    for i in range(4):
        if not (coordface(i,0,-1) == 5):
            passer = False
        else:
            if not faces[i][0][0] == i:
                passer = False
                malplace = i
    if passer:
        #Face blanche déjà faite: on passe à l'étape 3
        return etape3()
    else:
        for i in range(4):
            for j in range(2):
                if faces[i][j*2][0] == 5:
                    malplace = coordonnees(i,j*2+1,0)[0]

        for i in range(4):
            for j in range(2):
                if faces[i][j*2][2] == 5:
                    if j == 1:
                        t = 0
                        bonneface = coordface(i,3,2)
                        while coordonnees(i,3+t*3,2)[0] != bonneface:
                            t+=1
                        liste = []
                        for k in range(t):
                            liste.append((4,-1))
                        lface = coordonnees(bonneface,-1,2)[0]
                        liste.append((lface,-1))
                        liste.append((4,-1))
                        liste.append((lface,1))
                        return liste
                        
                    else:
                        t = 0
                        bonneface = coordface(i,-1,2)
                        while coordonnees(i,-1+t*3,2)[0] != bonneface:
                            t+=1
                        liste = []
                        for k in range(t):
                            liste.append((4,-1))
                        liste.append((4,-1))
                        liste.append((bonneface,-1))
                        liste.append((4,1))
                        liste.append((bonneface,1))
                        return liste

        tourner = False
        for i in range(2):
            for j in range(2):
                if faces[4][i*2][j*2] == 5:
                    face1 = coordface(4,i*4-1,j*2)
                    face2 = coordface(4,i*2,j*4-1)

                    gface1 = coordonnees(4,i*4-1,j*2)[0]
                    gface2 = coordonnees(4,i*2,j*4-1)[0]
                    
                    t=0
                    
                    if face1 != gface2 or face2!= gface1:
                        tourner = True
                    else:
                        fface = gface2
                        if coordonnees(gface1,-1,1)[0] == gface2:
                            fface = gface1
                        liste = []
                        liste.append((fface,1))
                        liste.append((4,-1))
                        liste.append((4,-1))
                        liste.append((fface,-1))
                        liste.append((4,1))
                        return liste

        if malplace >= 0:
            liste = []
            liste.append((malplace,1))
            liste.append((4,-1))
            liste.append((malplace,-1))
            return liste
                    
        if tourner:
            return [(4,1)]

def etape3():
    """
    Cette etape permet d'assembler la deuxième couronne du cube
    """
    global etape
    etape = 3
    
    passer = True

    for i in range(4):
        for j in range(3):
            if faces[i][j][1] != i:
                passer = False
    if passer:
        #Deuxieme couronne déjà faite : on passe à l'étape 4
        return etape4()
    else:
        for i in range(4):
            if faces[i][1][2] != 4:
                facehaut = coordface(i,1,3)
                if facehaut !=4:
                    t = 0
                    while faces[i][1][2] != coordonnees(i,1+t*3,2)[0]:
                        t+=1
                    liste = []
                    for k in range(t):
                        liste.append((4,-1))

                    fface = coordonnees(i,1+t*3,2)[0]
                    rface = coordonnees(fface,3,1)[0]
                    lface = coordonnees(fface,-1,1)[0]
                    if facehaut == rface:
                        liste.append((4,1))
                        liste.append((rface,1))
                        liste.append((4,-1))
                        liste.append((rface,-1))
                        liste.append((4,-1))
                        liste.append((fface,-1))
                        liste.append((4,1))
                        liste.append((fface,1))
                    else:
                        liste.append((4,-1))
                        liste.append((lface,-1))
                        liste.append((4,1))
                        liste.append((lface,1))
                        liste.append((4,1))
                        liste.append((fface,1))
                        liste.append((4,-1))
                        liste.append((fface,-1))
                    return liste
        
        for i in range(4):
            lface = coordonnees(i,-1,1)[0]
            if faces[i][0][1] != i or coordface(i,-1,1) != lface:
                liste = []
                liste.append((4,-1))
                liste.append((lface,-1))
                liste.append((4,1))
                liste.append((lface,1))
                liste.append((4,1))
                liste.append((i,1))
                liste.append((4,-1))
                liste.append((i,-1))
                return liste
        
                        
                    
                    

def etape4():
    """
    Cette etape permet d'assembler la croix jaune
    """
    global etape
    etape = 4
    
    passer = True
    for i in range(3):
        for j in range(3):
            if (i == 1 or j == 1) and i!=j:
                if faces[4][i][j] != 4:
                    passer = False

    if passer:
        return etape5()
    else:
        liste = []
        for i in range(4):
            rface = coordonnees(i,3,0)[0]
            if coordface(i,0,4) == 4 and coordface(i,1,5) == 4:
                liste.append((i,1))
                liste.append((4,1))
                liste.append((rface,1))
                liste.append((4,-1))
                liste.append((rface,-1))
                liste.append((i,-1))
                return liste
            
            if (coordface(i,0,4) == 4 and coordface(i,2,4) == 4) or i==3:
                liste.append((i,1))
                liste.append((rface,1))
                liste.append((4,1))
                liste.append((rface,-1))
                liste.append((4,-1))
                liste.append((i,-1))
                return liste

def etape5():
    """
    Cette etape place les aretes de la derniere face au bon endroit
    """
    global etape
    etape = 5
    
    passer = True
    for i in range(4):
        if faces[i][1][2] != i:
            passer = False
    if passer:
        return etape6()
    else:
        compteur = 0
        face = 0
        consecutif = False
        for j in range(5):
            i = coordonnees(0,j*3,0)[0]
            if faces[i][1][2] == i:
                if not consecutif:
                    compteur = 0
                compteur+=1
                if compteur>1:
                    break
                face = i
                consecutif = True
            else:
                consecutif = False
                    
        if compteur!=1:
            return [(4,1)]
        else:
            rface = coordonnees(face,3,0)[0]
            rrarete = coordface(face,7,2)

            liste = []
            
            if rface != rrarete:
                liste.append((rface,1))
                liste.append((4,1))
                liste.append((rface,-1))
                liste.append((4,1))
                liste.append((rface,1))
                liste.append((4,1))
                liste.append((4,1))
                liste.append((rface,-1))
            else:
                liste.append((rface,1))
                liste.append((4,-1))
                liste.append((4,-1))
                liste.append((rface,-1))
                liste.append((4,-1))
                liste.append((rface,1))
                liste.append((4,-1))
                liste.append((rface,-1))
                
            return liste
                
def boncoin(i,face):
    """
    Fonction permettant de déterminer si le coin en haut à gauche de la face i
    coincide bien avec la face entrée en second argument
    """
    adjacentes = [face]
    adjacentes.append(coordonnees(face,-1,0)[0])
    adjacentes.append(coordonnees(face,0,3)[0])

    coin = [coordface(i,0,2)]
    coin.append(coordface(i,-1,2))
    coin.append(coordface(i,0,3))

    for adj in adjacentes:
        if not(adj in coin):
            return False
    return True

def etape6():
    """
    Cette etape place les coins de la derniere face au bon endroit
    """
    global etape
    etape = 6
    
    passer = True
    for i in range(4):
        if not boncoin(i,i):
            passer = False
    if passer:
        return etape7()
    else:
        liste = []
        for i in range(4):
            if boncoin(i,i) or i == 3:

                rf = coordonnees(i,3,0)[0]
                rrf = coordonnees(i,6,0)[0]

                if boncoin(rf,rrf):
                    rface = rf
                    lface = coordonnees(i,-1,0)[0]
                    liste.append((rface,1))
                    liste.append((4,-1))
                    liste.append((lface,-1))
                    liste.append((4,1))

                    liste.append((rface,-1))
                    liste.append((4,-1))
                    liste.append((lface,1))
                    liste.append((4,1))
                else:
                    rface = i
                    lface = rrf
                    liste.append((lface,-1))
                    liste.append((4,1))
                    liste.append((rface,1))
                    liste.append((4,-1))

                    liste.append((lface,1))
                    liste.append((4,1))
                    liste.append((rface,-1))
                    liste.append((4,-1))

                return liste

def etape7():
    """
    Cette etape oriente les coins de la derniere face dans la bonne direction
    """
    global etape
    etape = 7
    
    passer = True
    for i in range(2):
        for j in range(2):
            if faces[4][i*2][j*2] != 4:
                passer = False
    if passer:
        return etape8()
    else:
        combinaison = -1
        fface = 0
        for i in range(4):
            if coordface(i,0,2) != i and coordface(i,-4,2) != coordonnees(i,-4,2)[0]:
                if coordface(i,0,2) == 4:
                    if coordface(i,-4,2) == 4:
                        combinaison = 0
                        fface = i
                elif coordface(i,-4,2) != 4:
                    combinaison = 1
                    fface = coordonnees(i,-4,2)[0]

        if combinaison == -1:
            for i in range(4):
                if coordface(i,0,2) != i and coordface(i,-4,2) != i:
                    if coordface(i,2,2) == i:
                        if coordface(i,0,2) == 4:
                            combinaison = 0
                            fface = i
                        else:
                            combinaison = 1
                            fface = coordonnees(i,-4,2)[0]
                                
        liste = []
        if combinaison == 0:
            rface = coordonnees(fface,3,0)[0]
            lface = coordonnees(fface,-1,0)[0]
            liste.append((rface,1))
            liste.append((4,1))
            liste.append((rface,-1))
            liste.append((4,1))
            liste.append((rface,1))
            liste.append((4,1))
            liste.append((4,1))
            liste.append((rface,-1))

            liste.append((lface,-1))
            liste.append((4,-1))
            liste.append((lface,1))
            liste.append((4,-1))
            liste.append((lface,-1))
            liste.append((4,-1))
            liste.append((4,-1))
            liste.append((lface,1))
        elif combinaison == 1:
            rface = coordonnees(fface,3,0)[0]
            lface = coordonnees(fface,-1,0)[0]
            liste.append((rface,1))
            liste.append((4,-1))
            liste.append((4,-1))
            liste.append((rface,-1))
            liste.append((4,-1))
            liste.append((rface,1))
            liste.append((4,-1))
            liste.append((rface,-1))

            liste.append((lface,-1))
            liste.append((4,1))
            liste.append((4,1))
            liste.append((lface,1))
            liste.append((4,1))
            liste.append((lface,-1))
            liste.append((4,1))
            liste.append((lface,1))
        else:
            print("ERREUR")
        return liste
            
                        

def etape8():
    """
    Si on arrive à cette étape, c'est que le cube est sous sa forme résolue
    On renvoie ainsi une liste vide pour le signifier
    """
    return []
