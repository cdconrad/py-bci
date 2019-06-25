#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
This is a training routine for a P3 speller based on Farwell and Donchin (1988).
Participants are asked to attend to a certain letter on a grid. Rows and columns
will then light up. When the rows or columns highlight the attended letter, a P3
response should be elicited.

This program is written in Pygame, though uses the Psychopy Pythong library to
interact with the Dalhousie NCIL EEG setup. Pygame was deliberately chosen to
demonstrate one of the key features of the Python stack, which is its porability.
Pygame is generally used to create video games, and by using it, we demonstrate
how the stack can be used to conduct unconventional neuroscience experiments.

In this program, a series of grids are generated at the rate specified by the
programmer (500 ms by default). Each grid has a random row or column highlighted.
If the row or column highlights the target letter, the grid triggers the 'target'
response on the EEG's parallel port. If not, they are assigned standard responses.

This program was originally designed for demonstration purposes, but can be used
as a foundation to a finished P300 BCI. In this tutorial, we only demonstrate the
training routine. To complete the BCI, a programmer needs to implement
classifiers and create a separate implementation routine that changes with the
classifiers. Future iterations of this tutorial may consider implementing the
full BCI.

REFERENCES

Farwell, L. A., & Donchin, E. (1988). Talking off the top of your head: toward a
mental prosthesis utilizing event-related brain potentials.
Electroencephalography and clinical Neurophysiology, 70(6), 510-523.
"""

import pygame, random, os, sys

#we will borrow PsychoPy's parallel feature to record stimulus timings using the parallel port
from psychopy import core, parallel
#parallel.setPortAddress(61432) #61432 is the lab port address

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
    FPS = 2 # 2 FPS should give us epochs of 500 ms

    #specify the grid content
    grid = ["      ",
            "ABCDEF",
            "GHIJKL",
            "MNOPQR",
            "STUVWX",
            "YZ1234",
            "56789_"]

    phrase = "" #this is used to store the string at the bottom of the interface

    lines = len(grid)
    columns = len(grid[0])

    length = screenrect.width / columns
    height = screenrect.height / lines

    oldhighlight = 0

    numtrials = 0
    targets = [[1,1],[3,5],[1,0],[2,2],[3,1],[4,0],[6,5]]
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
                #parallel.setData(2) #this is the target; record it in the parallel
                print(highlight)
                print(target)
                print(str(numtrials)) + " **target row"
                core.wait(0.005)
                #parallel.setData(0)
            else:
                #parallel.setData(1) #this is not the target
                print(highlight)
                print(target)
                print(str(numtrials)) + " row"
                core.wait(0.005)
                #parallel.setData(0)
        else: #it is a column
            if target[1] == highlight:
                #parallel.setData(2) #this is the target; record it in the parallel
                print(highlight)
                print(target)
                print(str(numtrials)) + " **target column"
                core.wait(0.005)
                #parallel.setData(0)
            else:
                #parallel.setData(1) #this is not the target
                print(highlight)
                print(target)
                print(str(numtrials)) + " column"
                core.wait(0.005)
                #parallel.setData(0)

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

        if targetcounter < 6:
            if numtrials == 0:
                makeTarget(targets[targetcounter])
                screen.blit(background, (0,0)) #clean whole screen
                pygame.display.flip()
                pygame.time.wait(waittime)
                numtrials += 1
            elif numtrials == 121:
                targetcounter += 1
                numtrials = 0
            else:
                makeStandard()
                oldhighlight = makeHighlighted(targets[targetcounter], oldhighlight)

                screen.blit(background, (0,0)) # clean whole screen
                pygame.display.flip()
                numtrials += 1

        else:
            pygame.quit()


#currently the scripts are written to be run as standalone
#routines. We should change these to work in conjunction once we get
#the classifiers working sometime in the future.
if __name__=="__main__":
    offline()
