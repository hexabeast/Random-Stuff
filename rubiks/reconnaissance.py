"""
Ce module permet, associé à une réalisation matérielle faite "maison"
(une boite en carton avec webcam, lampe et support pour le cube à l'intérieur),
permet de scanner un cube réel afin d'en réaliser une copie virtuelle afin
de le résoudre en utilisant l'algorithme.

ATTENTION : CE SCRIPT N'EST PAS COMMENTE
"""
from PIL import Image
import numpy as np

import cv2

camera_port = 1
     
ramp_frames = 30
camera = cv2.VideoCapture(camera_port)
camera.set(3,320)
camera.set(4,176)

def couleur(col):
    if col[0]>150 and col[1]>150 and col[2]>160:
        return 5 #blanc
    elif col[0]>150 and col[1]>160:
        return 4 #jaune
    elif col[0]>150 and col[1]>80:
        return 1 #orange
    elif col[0]>150:
        return 0 #rouge
    elif col[1]>150:
        return 3 #vert
    else:
        return 2 #bleu


def moyennecoul(im,pos):
    coul = (0,0,0)
    for i in range(pos[0]-2,pos[0]+3):
        for j in range(pos[1]-2,pos[1]+3):
            coul = (coul[0]+im[i][j][0],coul[1]+im[i][j][1],coul[2]+im[i][j][2])
    coul = (int(coul[0]/25),int(coul[1]/25),int(coul[2]/25))
    return coul

def get_image():
    retval, im = camera.read()
    return im

def photo(afficher):
    for i in range(ramp_frames):
        temp = get_image()
    camera_capture = get_image()
    img = Image.fromarray(camera_capture)

    #img = img.resize(size, Image.ANTIALIAS)
    img = img.crop((107,35,img.size[0]-105,img.size[1]-33))
    img =img.convert('RGB')

    for x in range(0, img.size[0]):
        for y in range(0,img.size[1]):
            r, g, b = img.getpixel((x, y))
            img.putpixel((x, y), (b, g, r))

    
    
    img = img.rotate(-90)
    if afficher:
        img.show()
    imga = np.asarray(img)
            

    couleurs = [[None for i in range(3)]for i in range(3)]
    for i in range(3):
        for j in range(3):
            pos = (int(i*(len(imga)/3)+len(imga)/6),int(j*(len(imga[0])/3)+len(imga[0])/6))
            couleurs[j][2-i] = couleur(moyennecoul(imga,pos))

    return couleurs

def quitter():
    camera.close()
