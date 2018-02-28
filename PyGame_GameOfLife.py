# Game of life 
# Based on the code created by Trevor Appleton
# http://trevorappleton.blogspot.co.uk/2013/07/python-game-of-life.html
# 

import pygame, sys
from pygame.locals import *
import random

# Number of frames per second
FPS = 15

# Sets size of grid
WINDOWWIDTH = 640
WINDOWHEIGHT = 640
CELLSIZE = 10 

# Checks cell size will not return a fraction
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size"
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size"

# Note // is Python 3 syntax, for Python 2 use /
CELLWIDTH = WINDOWWIDTH // CELLSIZE # number of cells wide 
CELLHEIGHT = WINDOWHEIGHT // CELLSIZE # Number of cells high

# Colour setup
BLACK =    (0,  0,  0)
WHITE =    (0, 0, 0) # White should be (255, 255, 255) but this is better on the eye
DARKGRAY = (40, 40, 40)
GREEN =    (200,200,200) # Green should be (0, 255, 0) for full green, agian changed to better on the eye

#Draws the grid lines
def drawGrid():
    # draw vertical lines
    for x in range(0, WINDOWWIDTH, CELLSIZE): 
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x,0),(x,WINDOWHEIGHT))
    # draw horizontal lines
    for y in range (0, WINDOWHEIGHT, CELLSIZE): 
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0,y), (WINDOWWIDTH, y))

# Clears the grid
def blankGrid():
    gridDict = {}
    for y in range (CELLHEIGHT):
        for x in range (CELLWIDTH):
            gridDict[x,y] = 0
    return gridDict

# Colours the cells green for life and white for no life
def colourGrid(item, lifeDict):
    x = item[0]
    y = item[1]
    y = y * CELLSIZE # translates array into grid size
    x = x * CELLSIZE # translates array into grid size
    if lifeDict[item] == 0:
        pygame.draw.rect(DISPLAYSURF, WHITE, (x, y, CELLSIZE, CELLSIZE))
    if lifeDict[item] == 1:
        pygame.draw.rect(DISPLAYSURF, GREEN, (x, y, CELLSIZE, CELLSIZE))
    return None

def startingGridRandom(lifeDict):
    for item in lifeDict:
        lifeDict[item] = random.randint(0,1)
    return lifeDict
 
def getNeighbours (item, lifeDict):
    neighbours = 0
    for x in range (-1,2):
        for y in range (-1,2):
            checkCell = (item[0]+x,item[1]+y)
            if checkCell[0] < CELLWIDTH and checkCell[0] >= 0:
                if checkCell[1] < CELLHEIGHT and checkCell[1] >= 0:
                    if lifeDict[checkCell] == 1:
                        if x == 0 and y == 0:
                            neighbours += 0 
                        else:
                            neighbours += 1
    return neighbours

# Copies the grid to a new one, then updates the data
def tick(lifeDict):
    newTick = {}
    for item in lifeDict:
        numberNeighbours = getNeighbours(item, lifeDict)
        if lifeDict[item] == 1:
            # 1 - Any live cell with fewer than two live neighbours dies, as if caused by under-population
            if numberNeighbours < 2:
                newTick[item] = 0
            # 3 - Any live cell with more than three live neighbours dies, as if by over-population
            elif numberNeighbours > 3:
                newTick[item] = 0
            else:
            # 2 - Any live cell with two or three live neighbours lives on to the next generation
                newTick[item] = 1
        elif lifeDict[item] == 0:
            # 4 - Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction
            if numberNeighbours == 3:
                newTick[item] = 1
            else:
               newTick[item] = 0
    return newTick 
      
# The main bit of code
def main():
    pygame.init()
    global DISPLAYSURF
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
    pygame.display.set_caption('Game of Life')

    DISPLAYSURF.fill(WHITE)

    lifeDict = blankGrid() # creates library and Populates to match blank grid

    lifeDict = startingGridRandom(lifeDict) # Assign random life
    #Colours in the items which are alive
    for item in lifeDict:
        colourGrid(item, lifeDict)
    drawGrid()
    pygame.display.update()
    
    while True: #main game loop
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
               startingGridRandom(lifeDict)
               pass
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        
        # Runs a tick
        lifeDict = tick(lifeDict)

        # Colours the live cells, and clears the dead ones
        for item in lifeDict:
            colourGrid(item, lifeDict)

        drawGrid()
        pygame.display.update()  
        FPSCLOCK.tick(FPS)    
        
if __name__=='__main__':
    main()
