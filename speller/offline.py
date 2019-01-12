#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
This is a training routine for the P3 speller. Participants are asked
to attend to a certain letter on a grid. Each grid that is generated
is treated as a stand along instance, so is designed to save each
instance as an epoch.
"""

import pygame, random, os, sys

#we will borrow PsychoPy's parallel feature to record stimulus timings using the parallel port
from psychopy import core, parallel
parallel.setPortAddress(61432) #61432 is the lab port address

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
    FPS = 3 # 2 FPS should give us epochs of 500 ms

    #specify the grid content
    grid = ["      ",
            "ABCDEF",
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

    numtrials = 121
    targets = [[1,1],[3,5],[1,0],[2,2],[3,1],[0,4],[6,5]]
    targetcounter = 0

    waittime = 3000

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

    #this function makes a makes a target
    def makeTarget(target):
        for y in range(lines):
            for x in range(columns):
                if y == target[0] and x == target[1]:
                    textsurface = write(grid[y][x],(255,0,0))
                    background.blit(textsurface, (length * x + length/4, height * (y-1) + height/4))
                else:
                    textsurface = write(grid[y][x])
                    background.blit(textsurface, (length * x + length/4, height * (y-1) + height/4))
        writePhrase()

    #generate a coloured random coloured column or row
    def makeHighlighted(target, oldhighlight=0):
        rowcol = random.randint(0,1) #determines whether to highlight a row or column
        if rowcol == 0:
            highlight = random.randint(0,lines-1) #determines which row or column
        else:
            highlight = random.randint(0,columns-1)
        print highlight
        print target

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

        #record on the parallel port; test to see if row is the same as target
        if rowcol == 0: #if it is a row
            if target[0] == highlight:
                parallel.setData(2) #this is the target; record it in the parallel
                print str(numtrials) + " **target row"
                core.wait(0.005)
                parallel.setData(0)
            else:
                parallel.setData(1) #this is not the target
                print str(numtrials) + " row"
                core.wait(0.005)
                parallel.setData(0)
        else: #it is a column
            if target[1] == highlight:
                parallel.setData(2) #this is the target; record it in the parallel
                print str(numtrials) + " **target column"
                core.wait(0.005)
                parallel.setData(0)
            else:
                parallel.setData(1) #this is not the target
                print str(numtrials) + " column"
                core.wait(0.005)
                parallel.setData(0)

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

        if targetcounter < 7:

            if numtrials == 121: #120 trials for train
                makeTarget(targets[targetcounter])
                numtrials = 0
                targetcounter += 1
                screen.blit(background, (0,0)) #clean whole screen
                pygame.display.flip()
                pygame.time.wait(waittime)

            makeStandard()
            oldhighlight = makeHighlighted(targets[targetcounter-1], oldhighlight)

            screen.blit(background, (0,0)) # clean whole screen
            pygame.display.flip()
            numtrials += 1

        else:
            break

        #this part of the function will be used when we have more than just a test routine
        '''
        elif targetcounter < 6: #1 test
            if numtrials == 120: #120 trials for test
                target = [2,2] #change this to the classified value later
                phrase = phrase + grid[target[0]][target[1]]
                makeTarget(target)
                numtrials = 0
                targetcounter += 1
                screen.blit(background, (0,0))
                pygame.display.flip()
                pygame.time.wait(waittime)

            makeStandard()
            oldhighlight = makeHighlighted(targets[targetcounter], oldhighlight)

            screen.blit(background, (0,0)) # clean whole screen
            pygame.display.flip()
            numtrials += 1
        '''
    pygame.quit()


#currently the scripts are written to be run as standalone
#routines. We should change these to work in conjunction once we get
#the classifiers working
if __name__=="__main__":
    offline()
