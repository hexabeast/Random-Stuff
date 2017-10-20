import mappe
import camera
import pygame
import images
g = 1500

def coli(p):
    return mappe.collisions(p.x,p.y,p.w,p.h)

class Player():
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.w = 23
        self.h = 50
        self.vx = 0
        self.vy = 0
        self.col = (255,255,255)
        self.speed = 200
        self.collidown = False
        self.direction = False
        self.nimage = 0
        self.t = 0
 
   
 
    def update(self, d):
        self.oldx,self.oldy = self.x,self.y
        self.collidown = False
 
        self.vy+=g*d
 
       
       
        self.y+=d*self.vy
 
        if coli(self):
            self.y = self.oldy
            if self.vy > 0:
                self.collidown = True
            self.vy = 0
 
        self.x+=d*self.vx
 
        if coli(self):
            self.x = self.oldx

 
        if self.vy<0:
            self.nimage = 9
            self.t=0
        elif self.vy>0:
            self.t=0
            self.nimage = 10
 
        if self.t> 0.06 :
            self.t=0
            self.nimage+=1
            if self.nimage >= 9:
                self.nimage=1
        if self.vx == 0 and self.collidown:
            self.nimage = 0

        if self.vx>0:
            self.direction = False
        elif self.vx<0:
            self.direction = True
               
        self.t+=d

        camera.draw(pygame.transform.flip(images.joueur[self.nimage],self.direction,False),int(self.x)-8,int(self.y)-10)





  
