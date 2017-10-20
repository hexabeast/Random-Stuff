import pygame
from pygame.locals import *
import inputs
import images
import camera
import mappe
import player

pygame.init()
pygame.display.set_caption("Test")

#Crée la surface de l'écran
w = 1200
h = 800
screen = pygame.display.set_mode((w, h), HWSURFACE | DOUBLEBUF)

camera.screen = screen

tempsDerniereImage=0
delta=0.01
deltaMultiplieur = 1
 
end = False

images.init()

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


mappe.load("niveau1") 
p = player.Player(200,200)

while(not end):
    update()

    if inputs.gauche:
        p.vx = -200
    elif inputs.droite:
        p.vx = 200
    else:
        p.vx = 0
    if inputs.haut and p.collidown:
        p.vy = -1000
    
    '''CODE'''
    mappe.draw(delta)
    camera.x = p.x-w/2
    camera.y = p.y-h/2
    p.update(delta)

    ''' '''
    
    #On termine le rendu:
    pygame.display.flip()

#Si on sort de la boucle principale, alors on quitte le programme:
pygame.quit()
