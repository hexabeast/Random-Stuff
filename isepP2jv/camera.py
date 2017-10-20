import pygame

x,y = 0,0

screen = 0

def draw(texture,px,py):
    screen.blit(texture,(px-x,py-y))
