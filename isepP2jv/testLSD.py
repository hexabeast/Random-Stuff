import pygame
from pygame.locals import *
import inputs
import math
import random

pygame.init()
pygame.display.set_caption("Test")
 
#Crée la surface de l'écran
w = 800
h = 800
screen = pygame.display.set_mode((w, h), HWSURFACE | DOUBLEBUF)

tempsDerniereImage=0
delta=0.01
deltaMultiplieur = 1
 
end = False

def update():
    global tempsDerniereImage, end, deltaMultiplieur, delta
    
    #On calcule le delta:
    t = pygame.time.get_ticks()
    delta = (t - tempsDerniereImage) / 1000.0 * deltaMultiplieur
    tempsDerniereImage = t

    if delta>100000000.05:
        delta = 0.05

    #Regarde s'il y a une event
    for event in pygame.event.get():
        if event.type == QUIT:
            #On quitte la fenêtre
            end = True
    inputs.update()
    
    #On "nettoie" le contenu de la fenêtre
    #pygame.draw.rect(screen, (0,0,0), (0,0,w,h), 0)
    
angle = 0
while(not end):
    update()
    '''CODE'''
    angle+=1*delta
    deltaMultiplieur+=0.2*delta
    if deltaMultiplieur > 100:
        deltaMultiplieur = 100

    posx = int(w/2 + math.cos(angle)*200)
    posy = int(w/2 + math.sin(angle)*200)
    col = (int(255*random.random()),int(255*random.random()),int(255*random.random()))

    pygame.draw.circle(screen, col, (posx,posy),200, 0)
    
    
    """m = 10

    for i in range(m):
        j = i/float(m)
        posx = int(w/2+(inputs.sourispos[0]-w/2)*(j))
        posy = int(h/2+(inputs.sourispos[1]-h/2)*(j))
        col = (int(255*j),int(255*j),int(255*j))

        pygame.draw.circle(screen, col, (posx,posy),int((w-(j*w))/3), 0)
    """
    ''' '''
    
    #On termine le rendu:
    pygame.display.flip()

#Si on sort de la boucle principale, alors on quitte le programme:
pygame.quit()
