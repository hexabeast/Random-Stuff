import pygame
from pygame.locals import *
import inputs
from random import random

pygame.init()
pygame.display.set_caption("Test")
 
#Crée la surface de l'écran
w = 1200
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

class Baballe():
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.vx = 200
        self.vy = 200
        self.radius = 50
        self.col = (255,255,255)

    def setspeed(self,x,y):
        self.vx = x
        self.vy = y

    def update(self,d):
        self.x+=self.vx*d
        self.y+=self.vy*d
        if self.vx>0 and self.x > w-self.radius:
            self.vx = -self.vx
        if self.vx<0 and self.x < self.radius:
            self.vx = -self.vx
        if self.vy>0 and self.y > h-self.radius:
            self.vy = -self.vy
        if self.vy<0 and self.y < self.radius:
            self.vy = -self.vy
        pygame.draw.circle(screen, self.col, (int(self.x),int(self.y)),self.radius, 0)
        
        
balles = [Baballe(random()*w,random()*h) for i in range(1000)]
for i in range(len(balles)):
    balles[i].vx*=random()*4-2
    balles[i].vy*=random()*4-2
    balles[i].radius = int(0.2*balles[i].radius * random())
    balles[i].col = (int(255*random()), int(255*random()), int(255*random()))

        
while(not end):
    update()
    '''CODE'''
    for i in range(len(balles)):
        balles[i].update(delta)
    ''' '''
    
    #On termine le rendu:
    pygame.display.flip()

#Si on sort de la boucle principale, alors on quitte le programme:
pygame.quit()



'''v = (0,0)
    if inputs.gauche:
        v = (v[0]-200,v[1])
    if inputs.droite:
        v = (v[0]+200,v[1])
    if inputs.haut:
        v = (v[0],v[1]-200)
    if inputs.bas:
        v = (v[0],v[1]+200)

balle.setspeed(v[0],v[1])'''
