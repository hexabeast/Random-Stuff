import pygame
from pygame.locals import *
import inputs
import math

pygame.init()
pygame.display.set_caption("Test")
 
#Crée la surface de l'écran
w = 800
h = 600
screen = pygame.display.set_mode((w, h), HWSURFACE | DOUBLEBUF)

tempsDerniereImage=0
delta=0.01
deltaMultiplieur = 1

collisions = []
balles = []
panier = None
gravity = -500
 
end = False


class Panier():
    def __init__(self,x,y,d):
        self.x = x
        self.y = y
        self.x1 = x-d/2
        self.x2 = x+d/2
        self.radius = 10
        self.col = (255,255,255)

    def update(self,d):
        pygame.draw.lines(screen, self.col, False, [(self.x1,self.y),(self.x2,self.y)], 2)
        
        pygame.draw.circle(screen, self.col, (int(self.x1),int(self.y)),self.radius, 0)
        pygame.draw.circle(screen, self.col, (int(self.x2),int(self.y)),self.radius, 0)

    def collide(self,balle):
        d1 = math.sqrt((balle.x-self.x1)**2+(balle.y-self.y)**2)
        d2 = math.sqrt((balle.x-self.x2)**2+(balle.y-self.y)**2)
        x,y = 0,0
        x1 = self.x1-balle.x
        if d2<self.radius+balle.radius:
            x1 = self.x2-balle.x
        if d1<self.radius+balle.radius or d2<self.radius+balle.radius:
            y1 = self.y-balle.y
            x2 = balle.vx
            y2 = balle.vy
            
            cosi = (x1*x2 + y1*y2)/math.sqrt(x2**2+y2**2)
            x3 = balle.x+cosi*(x1)
            y3 = balle.y+cosi*(y1)

            x4 = balle.x+balle.vx
            y4 = balle.y+balle.vy

            x5 = 2*x3 - x4
            y5 = 2*y3 - y4

            x = balle.x-x5
            y = balle.y-y5
            x /=1.5*((math.sqrt(x**2+y**2)/math.sqrt(balle.vx**2+balle.vy**2)))  
            y /=1.5*((math.sqrt(x**2+y**2)/math.sqrt(balle.vx**2+balle.vy**2)))
        return (x,y)

class Viseur():
    def __init__(self,x,y):
        self.etat = 0
        self.x = x
        self.y = y
        
        self.rotation = 0
        self.rotmin = -3.5/2
        self.rotmax = 0.2
        self.rotdir = 1
        self.rotspeed = 3
        
        self.longueur = 50
        self.longmin = 10
        self.longmax = 100
        self.longdir = 1
        self.longspeed = 200
        self.col1 = (255,150,40)
        self.col2 = (255,255,255)
        self.reload = True
        self.currentballe = None

    def update(self,d,clic):
        global balles
        if self.etat == 0:
            if self.reload:
                self.longueur = 50
                self.currentballe = Baballe(self.x,self.y,self)
                self.currentballe.disable = True
                self.currentballe.col = self.col1
                self.etat = 1
                balles.append(self.currentballe)
                self.reload = False
            
        elif self.etat == 1:
            self.rotation+=self.rotspeed*self.rotdir*d
            if self.rotation>self.rotmax:
                self.rotdir = -1
            elif self.rotation<self.rotmin:
                self.rotdir = 1
            if clic:
                self.etat+=1

        elif self.etat == 2:
            self.longueur+=self.longspeed*self.longdir*d
            if self.longueur>self.longmax:
                self.longdir = -1
            elif self.longueur<self.longmin:
                self.longdir = 1
            if clic:
                self.etat = 0
                self.currentballe.disable = False
                self.currentballe = None

        px = math.cos(self.rotation)*self.longueur
        py = math.sin(self.rotation)*self.longueur
        
        if self.currentballe != None:
            self.currentballe.x = self.x+px
            self.currentballe.y = self.y+py
            self.currentballe.vx = px*10
            self.currentballe.vy = py*10

            
        pygame.draw.lines(screen, self.col2, False, [(self.x,self.y),(self.x+px,self.y+py)], 5)
        

        
            


class Baballe():
    def __init__(self,x,y,vis):
        self.vis = vis
        self.touchey = False
        self.x = x
        self.y = y
        self.vx = 250
        self.vy = 0
        self.radius = 20
        self.col = (255,150,40)
        self.disable = False

    def setspeed(self,x,y):
        self.vx = x
        self.vy = y

    def update(self,d):
        global reload
        if not self.disable:
            oldy = self.y
            oldx = self.x
            oldvy = self.vy
            self.vy-=gravity*d
            
            self.y+=self.vy*d
            self.x+=self.vx*d

            coly = (panier.collide(self))
            if coly != (0,0):
                self.x = oldx
                self.y = oldy
                self.vx = coly[0]
                self.vy = coly[1]
            else:
                if self.vy>0 and self.y > h-self.radius:
                    self.vy = -self.vy*0.8
                    self.vx -= self.vx*0.002
                    self.y = oldy
                    if not self.touchey:
                        self.vis.reload = True
                        self.touchey = True
                if self.vy<0 and self.y < self.radius:
                    self.vy = -self.vy*0.8
                    self.y = oldy

                if self.vx>0 and self.x > w-self.radius:
                    self.vx = -self.vx*0.8
                    self.x = oldx
                if self.vx<0 and self.x < self.radius:
                    self.vx = -self.vx*0.8
                    self.x = oldx

            '''
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
            '''    
        pygame.draw.circle(screen, self.col, (int(self.x),int(self.y)),self.radius, 0)



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



panier = Panier(w/2,h/4,120)

vis = Viseur(w/10,h*9/10)

vis2= Viseur(w*9/10,h*9/10)
vis2.col1 = (40,150,255)
vis2.col2 = (255,150,150)
vis2.rotmin = -3.45
vis2.rotmax = -1.3

while(not end):
    update()
    '''CODE'''
    vis.update(delta,inputs.clicespace)
    vis2.update(delta,inputs.clicenter)
    for b in balles:
        b.update(delta)
    panier.update(delta)
    ''' '''
    
    #On termine le rendu:
    pygame.display.flip()

#Si on sort de la boucle principale, alors on quitte le programme:
pygame.quit()
