import images
import camera

w = 0
h = 0
blocs = None

def load(nom):
    global blocs, w, h

    f = open("niveaux/"+nom,'r')

    tempbloc = []

    for ligne in f:
        tempbloc.append([])
        for caractere in ligne.split(",")
            tempbloc[-1].append(int(caractere))
    f.close()

    h = len(tempbloc)
    w = len(tempbloc[0])

    blocs = [[0 for i in range(w)] for j in range(h)]

    for i in range(h):
        for j in range(w):
            if tempbloc[i][j] != 0:
                blocs[i][j] = 1
                

def draw(delta):
    global blocs, w, h
    for i in range(h):
        for j in range(w):
            if blocs[i][j] == 1:
                camera.draw(images.bloc[0],i*32,j*32)
    

    
