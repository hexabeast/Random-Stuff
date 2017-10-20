import pygame
from pygame.locals import *
import inputs

pygame.init()
pygame.display.set_caption("Test")
 
#Crée la surface de l'écran
w = 800
h = 600
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

    if delta>0.05:
        delta = 0.05

    #Regarde s'il y a une event
    for event in pygame.event.get():
        if event.type == QUIT:
            #On quitte la fenêtre
            end = True
    inputs.update()
    
    #On "nettoie" le contenu de la fenêtre
    pygame.draw.rect(screen, (0,0,0), (0,0,w,h), 0)




    
while(not end):
    update()
    '''CODE'''

    ''' '''
    
    #On termine le rendu:
    pygame.display.flip()

#Si on sort de la boucle principale, alors on quitte le programme:
pygame.quit()
