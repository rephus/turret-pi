#!/usr/bin/python
import time 
import pygame

pygame.init()
screen = pygame.display.set_mode((100, 100))
pygame.display.set_caption('Keys')
pygame.mouse.set_visible(1)

while True:
    print "Start loop"
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        print "K_UP pressed"
    elif keys[pygame.K_DOWN]:  
        print "K_DOWN pressed"
    elif keys[pygame.K_SPACE]:  
        print "SPACE pressed"

    time.sleep(0.1)
    pygame.event.pump() 