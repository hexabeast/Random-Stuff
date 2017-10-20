import pygame
from pygame.locals import *
import inputs
from random import random

pygame.init()
pygame.display.set_caption("Pong")
 
#Crée la surface de l'écran
w = 1200
h = 800
screen = pygame.display.set_mode((w, h), HWSURFACE | DOUBLEBUF)

tempsDerniereImage=0
delta=0.01
deltaMultiplieur = 1

collisions = []
gravity = -500
 
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

class Babarre():
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.vy = 0
        self.speed = 200
        self.w = 30
        self.h = 150
        self.col = (255,255,255)
        
    def update(self,d):
        self.oldy = self.y
        self.y+=self.vy*d

        if self.y<0:
            self.y = self.oldy
        elif self.y>h-self.h:
            self.y = self.oldy

        pygame.draw.rect(screen, self.col, (int(self.x),int(self.y),int(self.w),int(self.h)), 0)
        

class Baballe():
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.vx = 250
        self.vy = 0
        self.radius = 20
        self.col = (255,255,255)

    def setspeed(self,x,y):
        self.vx = x
        self.vy = y

    def update(self,d):
        oldy = self.y
        oldx = self.x
        oldvy = self.vy
        self.vy-=gravity*d
        
        self.y+=self.vy*d
        self.x+=self.vx*d

        if self.out():
            self.x = w/2
            self.y = h/4
            self.vy = 0

        if self.vy>0 and self.y > h-self.radius:
            self.vy = -self.vy
            self.y = oldy
        if self.vy<0 and self.y < self.radius:
            self.vy = -self.vy
            self.y = oldy

        for i in range(len(collisions)):
            a = collisions[i].x > self.x+self.radius
            b = collisions[i].x+collisions[i].w < self.x-self.radius
            c = collisions[i].y > self.y+self.radius
            d = collisions[i].y+collisions[i].h < self.y-self.radius

            if not (a or b or c or d):
                self.vx = -self.vx
                self.y = oldy
                self.x = oldx
                collisions[i].y = collisions[i].oldy
                self.vy += collisions[i].vy
                break
            
        pygame.draw.circle(screen, self.col, (int(self.x),int(self.y)),self.radius, 0)

    def out(self):
        if self.x > w+self.radius*4:
            return True
        elif self.x < -self.radius*4:
            return True
        return False
        
balle = Baballe(w/2,h/4)
barre1 = Babarre(80,h/3)
barre2 = Babarre(w-110,h/3)

collisions.append(barre1)
collisions.append(barre2)

while(not end):
    update()
    '''CODE'''
    if inputs.haut:
        barre1.vy = -barre1.speed
    elif inputs.bas:
        barre1.vy = barre1.speed
    else:
        barre1.vy = 0

    #barre2.y = max(0,min((balle.y-barre2.h/2), h-barre2.h))
    if inputs.gauche:
        barre2.vy = -barre1.speed
    elif inputs.droite:
        barre2.vy = barre1.speed
    else:
        barre2.vy = 0
    
    barre1.update(delta)
    barre2.update(delta)
    balle.update(delta)
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
