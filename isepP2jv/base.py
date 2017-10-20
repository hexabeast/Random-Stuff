import pygame
from pygame.locals import *
import inputs

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

g = 1500

collisions = []

class Obstacle():
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.w = 50
        self.h = 50
        self.col = (255,255,255)
        
    def update(self, d):
        pygame.draw.rect(screen, self.col, (int(self.x),int(self.y),int(self.w),int(self.h)), 0)


def coli(self):
    for i in range(len(collisions)):
        a = collisions[i].x > self.x+self.w
        b = collisions[i].x+collisions[i].w < self.x
        c = collisions[i].y > self.y+self.h
        d = collisions[i].y+collisions[i].h < self.y

        if not (a or b or c or d):
            return True
    return False

class Carrey():
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.w = 50
        self.h = 50
        self.vx = 0
        self.vy = 0
        self.col = (255,255,255)
        self.speed = 200
        self.collidown = False

    

    def update(self, d):
        self.oldx,self.oldy = self.x,self.y
        self.collidown = False

        self.vy+=g*d
        
        
        self.y+=d*self.vy

        if self.y<0:
            self.y = self.oldy
            self.vy = 0
        elif self.y>h-self.h:
            self.y = self.oldy
            self.vy = 0
            self.collidown = True
        elif coli(self):
            self.y = self.oldy
            if self.vy > 0:
                self.collidown = True
            self.vy = 0

        self.x+=d*self.vx

        if self.x<0:
            self.x = self.oldx
        elif self.x>w-self.w:
            self.x = self.oldx
        elif coli(self):
            self.x = self.oldx

        pygame.draw.rect(screen, self.col, (int(self.x),int(self.y),int(self.w),int(self.h)), 0)

        #ZYEUX
        pygame.draw.circle(screen, (0,0,0), (int(self.x+self.w/4),int(self.y+self.h/4)),15, 0)
        pygame.draw.circle(screen, (0,0,0), (int(self.x+self.w*3/4),int(self.y+self.h/4)),15, 0)
        
        pygame.draw.circle(screen, (255,255,255), (int(self.x+self.w/4),int(self.y+self.h/4)),14, 0)
        pygame.draw.circle(screen, (255,255,255), (int(self.x+self.w*3/4),int(self.y+self.h/4)),14, 0)

        pygame.draw.circle(screen, (0,0,0), (int(self.x+self.w/4),int(self.y+self.h/4)),12, 0)
        pygame.draw.circle(screen, (0,0,0), (int(self.x+self.w*3/4),int(self.y+self.h/4)),12, 0)

        pygame.draw.circle(screen, (120,0,0), (int(self.x+self.w/2),int(self.y+self.h*3/4)),10, 0)
        ###

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



carre = Carrey(w/2, h-50)
    
while(not end):
    update()

    if inputs.sourisclicgauche:
        ca = Obstacle(inputs.sourispos[0]-25,inputs.sourispos[1]-25)
        collisions.append(ca)

    if inputs.droite:
        carre.vx = carre.speed
    elif inputs.gauche:
        carre.vx = -carre.speed
    else:
        carre.vx = 0
        
    if inputs.haut and carre.collidown:
        carre.vy = -6*carre.speed
        
    carre.update(delta)

    for i in range(len(collisions)):
        collisions[i].update(delta)
    '''CODE'''

    ''' '''
    
    #On termine le rendu:
    pygame.display.flip()

#Si on sort de la boucle principale, alors on quitte le programme:
pygame.quit()
