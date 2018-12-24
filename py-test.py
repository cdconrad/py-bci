#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

"""

import pygame
import random

def speller(msg="hello world", duration=5):

    #we will use this function to write the letters
    def write(msg, colour=(30,144,255)):
        myfont = pygame.font.SysFont("None", 90)
        mytext = myfont.render(msg, True, colour)
        mytext = mytext.convert_alpha()
        return mytext
        
    pygame.init() #start pygame

    #specify screen and background sizes
    screen = pygame.display.set_mode((800,800))
    screenrect = screen.get_rect()
    background = pygame.Surface((screen.get_size()))
    backgroundrect = background.get_rect()
    background.fill((0,0,0)) # black
    background = background.convert()
    screen.blit(background, (0,0)) # clean whole screen

    clock = pygame.time.Clock()
    mainloop = True
    FPS = 4 # 2 FPS should give us epochs of 500 ms

    #specify the grid content
    grid = ["ABCDEF",
            "GHIJKL",
            "MNOPQR",
            "STUVWX",
            "YZ1234",
            "56789_"]

    lines = len(grid)
    columns = len(grid[0])

    length = screenrect.width / columns
    height = screenrect.height / lines

    oldhighlight = 0 #we will use this variable to store old previously highlighted values

    #pygame uses a main loop to generate the interface
    while mainloop:
        milliseconds = clock.tick(FPS)  # milliseconds passed since last frame
        seconds = milliseconds / 1000.0 # seconds passed since last frame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mainloop = False # pygame window closed by user
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    mainloop = False # user pressed ESC

        #generate the uncoloured frame
        for y in range(lines):
            for x in range(columns):
                textsurface = write(grid[y][x])
                background.blit(textsurface, (length * x + length/4, height * y + height/4))

        screen.blit(background, (0,0))
        pygame.display.flip()

        #generate the highlighted frame
        rowcol = random.randint(0,1) #determines whether to highlight a row or column
        highlight = random.randint(0,lines-1) #determines which row or column

        if highlight == oldhighlight: #adjusts repeated values
            if highlight == 0 or 2 or 4:
                highlight += 1
            else:
                highlight -=1

        oldhighlight = highlight

        for y in range(lines):
            for x in range (columns):
                if rowcol == 0: #highlight a row
                    if y == highlight:
                        textsurface = write(grid[y][x],(255,255,100))
                        background.blit(textsurface, (length * x + length/4, height * y + height/4))
                    else:
                        textsurface = write(grid[y][x])
                        background.blit(textsurface, (length * x + length/4, height * y + height/4))
                else: #highlight a column
                    if x == highlight:
                        textsurface = write(grid[y][x],(255,255,100))
                        background.blit(textsurface, (length * x + length/4, height * y + height/4))
                    else:
                        textsurface = write(grid[y][x])
                        background.blit(textsurface, (length * x + length/4, height * y + height/4))
        pygame.time.delay(100) #delay 100 ms to allow for attention response
        screen.blit(background, (0,0)) # clean whole screen
        pygame.display.flip()

    pygame.quit()

if __name__=="__main__":
    speller() 
