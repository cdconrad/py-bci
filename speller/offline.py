#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This is a training routine for the P3 speller. Participants are asked
to attend to a certain letter on a grid. Each grid that is generated
is treated as a stand along instance, so is designed to save each
instance as an epoch.
"""

import pygame, random

def offline():
        
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
    FPS = 200 # 2 FPS should give us epochs of 500 ms

    #specify the grid content
    grid = ["ABCDEF",
            "GHIJKL",
            "MNOPQR",
            "STUVWX",
            "YZ1234",
            "56789_"]

    phrase = ""

    lines = len(grid)
    columns = len(grid[0])

    length = screenrect.width / columns
    height = screenrect.height / lines

    oldhighlight = 0

    numtrials = 100
    targets = [[1,3],[3,2],[4,1],[2,3],[4,4]]
    targetcounter = 0

    waittime = 1000

    #we will use this function to write the letters
    def write(msg, colour=(30,144,255)):
        myfont = pygame.font.SysFont("None", 90)
        mytext = myfont.render(msg, True, colour)
        mytext = mytext.convert_alpha()
        return mytext

    #use this function to write the spelled phrase
    def writePhrase():
        for z in range(len(phrase)):
            textsurface = write(phrase[z], (255,255,255))
            background.blit(textsurface, (length * z + length/4, height * 5 + height/4))

    #generate uncoloured frame
    def makeStandard():
        for y in range(lines):
            for x in range(columns):
                textsurface = write(grid[y][x])
                background.blit(textsurface, (length * x + length/4, height * (y-1) + height/4))

        writePhrase()
        screen.blit(background, (0,0))
        pygame.display.flip()

    def makeTarget(target):
        for y in range(lines):
            for x in range(columns):
                if y == target[0] and x == target[1]:
                    textsurface = write(grid[y][x],(255,255,100))
                    background.blit(textsurface, (length * x + length/4, height * (y-1) + height/4))
                else:
                    textsurface = write(grid[y][x])
                    background.blit(textsurface, (length * x + length/4, height * (y-1) + height/4))
        writePhrase()

    #generate a coloured random coloured column or row
    def makeHighlighted(oldhighlight=0):
        rowcol = random.randint(0,1) #determines whether to highlight a row or column
        highlight = random.randint(0,lines-1) #determines which row or column

        if highlight == oldhighlight: #adjusts repeated values
            if highlight == 0 or 2 or 4:
                highlight += 1
            else:
                highlight -=1

        newhighlight = highlight

        for y in range(lines):
            for x in range (columns):
                if rowcol == 0: #highlight a row
                    if y == highlight:
                        textsurface = write(grid[y][x],(255,255,100))
                        background.blit(textsurface, (length * x + length/4, height * (y-1) + height/4))
                    else:
                        textsurface = write(grid[y][x])
                        background.blit(textsurface, (length * x + length/4, height * (y-1) + height/4))
                else: #highlight a column
                    if x == highlight:
                        textsurface = write(grid[y][x],(255,255,100))
                        background.blit(textsurface, (length * x + length/4, height * (y-1) + height/4))
                    else:
                        textsurface = write(grid[y][x])
                        background.blit(textsurface, (length * x + length/4, height * (y-1) + height/4))

        writePhrase()
        return(newhighlight)

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

        if targetcounter < 5: #5 test
            
            if numtrials == 100:
                makeTarget(targets[targetcounter])
                numtrials = 0
                targetcounter += 1
                screen.blit(background, (0,0)) #clean whole screen
                pygame.display.flip()
                pygame.time.wait(waittime)
            
            makeStandard()
            oldhighlight = makeHighlighted(oldhighlight)

            screen.blit(background, (0,0)) # clean whole screen
            pygame.display.flip()
            numtrials += 1

        elif targetcounter < 10: #5 train
            if numtrials == 100:
                target = [2,2] #change this to the classified value later
                phrase = phrase + grid[target[0]][target[1]]
                makeTarget(target)
                numtrials = 0
                targetcounter += 1
                screen.blit(background, (0,0))
                pygame.display.flip()
                pygame.time.wait(waittime)

            makeStandard()
            oldhighlight = makeHighlighted(oldhighlight)

            screen.blit(background, (0,0)) # clean whole screen
            pygame.display.flip()
            numtrials += 1

    pygame.quit()


#currently the scripts are written to be run as standalone
#routines. We should change these to work in conjunction once we get
#the classifiers working
if __name__=="__main__":
    offline() 
