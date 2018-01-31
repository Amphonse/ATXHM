import pygame
import random
import math
import time
import mans

(width,height) = (1280,800)
menu = False
screen = pygame.display.set_mode((width,height))
pygame.font.init()

hello = True
running = True

Jeff = mans.mans("Jeff",screen)
Bob =  mans.mans("Bob",screen)

Jeff.reset()


class mans_manager():
    def __init__(self,mans):
        self.mans = mans
        
        
                    
                
Jeffs = mans_manager(Jeff)        
mpos = pygame.mouse.get_pos()        
#Jeffs.mans.vats(mpos)



while running:
    mpos = pygame.mouse.get_pos()
    #Jeffs.mans.vats(mpos)
    #do turns left to live
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(pygame.mouse.get_pos())
            Jeff.mupdate()
            Bob.mupdate()
            if pygame.mouse.get_pressed()[2]:
                screen.fill((0,0,0))
                ##will write code to sort this bit out
                Jeffs.mans.reset()
                mpos = pygame.mouse.get_pos()
                menu = False
            elif pygame.mouse.get_pressed()[0]:
                Jeffs.mans.left_click(Bob,menu)
                screen.fill((0,0,0))
                Jeffs.mans.reset()
                mpos = pygame.mouse.get_pos()
                menu = False
            if pygame.mouse.get_pressed()[2]:    
                menu=Jeffs.mans.right_click(mpos)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                print("Hallo")
                ##will write code to sort this bit out
                Jeffs.mans.invman(0,"Belt","Left Hand")
                print(Jeffs.mans.equipment["Left Hand"])
            if event.key == pygame.K_b:
                print("Hallo")
                ##will write code to sort this bit out
                Jeffs.mans.invman(0,"Left Hand","Belt")
                print(Jeffs.mans.equipment["Left Hand"])
            if event.key == pygame.K_c:
                if hello:
                    screen.fill((0,0,0))
                    Jeff.reset()
                    Jeffs = mans_manager(Jeff)
                    hello = False
                else:
                    screen.fill((0,0,0))
                    Bob.reset()
                    Jeffs = mans_manager(Bob)
                    hello=True
        if event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h),
                                              pygame.RESIZABLE)
            #head_im = pygame.image.load("Head.png").convert()
            #head_im.set_colorkey((255,255,255))
            #screen.blit(pygame.transform.scale(head_im, (int(event.w/width*75),int(event.w/width*88))), (0, 0))
            screen.fill((0,0,0))
            Jeff.resize()
            Bob.resize()
            Jeffs.mans.reset()
                        
            
        
                
            
            
    pygame.display.update()
