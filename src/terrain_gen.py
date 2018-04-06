from __future__ import absolute_import
import random
import time
import math
from src.tile import Tile
from src.visual import *

global a
a = 0

class Room(object):
    def __init__(self, size):
        self.x = size[0]
        self.y = size[1]
        self.dataMatrix = [[-1 for k in range(self.x)] for k in range(self.y)]
        self.entityMatrix = [[False for k in range(self.x)] for k in range(self.y)]
        self.i = 0

    def randomEntityGen(self):
        for n in range(self.x):
            for m in range(self.y):
                self.entityMatrix[n][m] = random.uniform(0,1) > 0.97

    """ Mid Point algorithm start """
    def midPointGenerationStart(self,seed=0):
        self.initCorners(seed)
        global a
        a+= 1
        a = 0
        self.midPointRecGeneration([
            (0,0),
            (self.x-1,0),
            (self.x-1,self.y-1),
            (0,self.y-1)
        ])

    def initCorners(self, seed):
        corners = [random.randint(0,NUMBER_OF_AVAILABLE_TILES-1) for k in
                    range(4)]

        self.dataMatrix[0][0] = corners[0]
        self.dataMatrix[self.x-1][0] = corners[1]
        self.dataMatrix[self.x-1][self.y-1] = corners[2]
        self.dataMatrix[0][self.y-1] = corners[3]

    def midPointRecGeneration(self, corners):
        affichageTileDebug = False

        # Clockwise starting in the upper left corner; visualising:
        corners = [
            (corners[0][0], corners[0][1]),
            (corners[1][0], corners[1][1]),
            (corners[2][0], corners[2][1]),
            (corners[3][0], corners[3][1])
        ]

        # Step1: if algorithm at the end, stop it
        if corners[0] == corners[1] or corners[1]==corners[2] or \
            (abs(corners[0][0]-corners[1][0]) == 1 and abs(corners[1][1]-corners[2][1])==1):
            return 0

        else:
            # Step2: assign value to midPoint
            midPointCoordinates = (
                int(sum([corner[0] for corner in corners])/4),
                int(sum([corner[1] for corner in corners])/4)
            )

            midPointValue = self.dataMatrix[midPointCoordinates[0]][midPointCoordinates[1]]

            if midPointValue == -1:
                #Do calculations only if the point isnt set
                cornerValues = [self.dataMatrix[x[0]][x[1]] for x in corners]
                midPointValue = self.formatColorValue((sum(cornerValues)+ self.noise()) / len(cornerValues))
                self.dataMatrix[midPointCoordinates[0]][midPointCoordinates[1]] = midPointValue

            # Step3: assign values to remaining 4 halves
            halvesLocation = []
            for i in range(4):
                halfLocation =((
                    int(math.floor((corners[i][0]+corners[(i+1)%4][0])/2)),
                    int(math.floor((corners[i][1]+corners[(i+1)%4][1])/2))
                ))
                halvesLocation.append(halfLocation)

                if self.dataMatrix[halfLocation[0]][halfLocation[1]] == -1:
                    #do calculations only if tile is empty

                    tripletValues = [
                        self.dataMatrix[corners[i][0]][corners[i][1]],
                        self.dataMatrix[corners[(i+1)%4][0]][corners[(i+1)%4][1]],
                        midPointValue
                    ]

                    halfPointValue = self.formatColorValue((sum(tripletValues) + self.noise()) / len(tripletValues))
                    self.dataMatrix[halvesLocation[i][0]][halvesLocation[i][1]] = halfPointValue

            if affichageTileDebug:
                self.renderRoom()
                raw_input()

            for i in range(4):
                self.midPointRecGeneration([corners[i],halvesLocation[i],midPointCoordinates,halvesLocation[i-1]])

    def noise(self):
        #return random.uniform(0,1.6)**2-1.28
        #return random.uniform(-1.8,1.8)
        return random.uniform(-1.71,1.71)
    """ Mid point algorithm end """

    """ Natural phenomenon """
    def initNaturalPhenomenon(self,seed=0):
        self.drought()
        self.renderRoom()
        raw_input("")
        self.riverConnection()

    def drought(self):
        for x in range(self.x):
            for y in range(self.y):
                waterTileCount = 0
                surroundings = self.surroundings(x,y)

                for tiles in surroundings:
                    if surroundings[tiles] == 0:
                        waterTileCount +=1

                #island simulation
                if self.dataMatrix[x][y] == 0 and waterTileCount == 0:
                    self.dataMatrix[x][y] = self.getSurroundingAverage(x,y)

    def naturalErosion(self):
        return 0

    def riverConnection(self):
        for y in range(self.y):
            for x in range(self.x):
                surroundings = {
                    ((x+1)%self.x,  (y+1)%self.y): "",
                    ((x-1)%self.x,  (y-1)%self.y): "",
                    ((x-1)%self.x,  (y+1)%self.y): "",
                    ((x+1)%self.x,  (y-1)%self.y): "",
                    (x,             (y+1)%self.y): "",
                    (x,             (y-1)%self.y): "",
                    ((x+1)%self.x,   y): "",
                    ((x-1)%self.x,   y): ""
                }
                for coord in surroundings:
                    surroundings[coord] = self.dataMatrix[coord[0]][coord[1]]

                tileValue = self.dataMatrix[x][y]

                waterTiles = []
                waterTileCount = 0
                for tiles in surroundings:
                    if surroundings[tiles] == 0:
                        waterTiles.append(tiles)
                        waterTileCount +=1

                #island simulation do nothing
                if waterTileCount >= 8:
                    continue

                #drought simulation NO OASIS
                if tileValue == 0 and waterTileCount == 0:
                    self.dataMatrix[x][y] = self.getSurroundingAverage(x,y)

                #simulate river
                elif tileValue != 0 and waterTileCount >= 2:
                    coords = []
                    for coord in surroundings:
                        coords.append(coord)

                    if waterTileCount == 2:
                        if  abs(coords[0][0]-coords[1][0]) < 2 and \
                            abs(coords[0][1]-coords[1][1]) < 2:
                            print("tag1")
                            continue

                    #Pattern 2-4-5-7 possible
                    elif waterTileCount == 3:
                        if  (abs(coords[0][0]-coords[1][0]) < 2 and \
                            abs(coords[1][0]-coords[2][0]) < 2) or \
                            (abs(coords[0][1]-coords[1][1]) < 2 and \
                            abs(coords[1][1]-coords[2][1]) < 2):
                            print("tag2")
                            continue

                    # Slightly uncontrolled
                    elif waterTileCount == 4 and random.uniform(0,1) < 0.8\
                        or waterTileCount == 5 and random.uniform(0,1) < 0.6:
                            print("tag3")
                            continue

                    print("je change la couleur")
                    self.dataMatrix[x][y] = 0
                    self.renderRoom()


    """ End natural phenomenon """

    def formatColorValue(self,value):
        if not isinstance(value, int):
            value = int(round(value))
        if value > 4:
            return 4
        if value < 0:
            return 0
        else: return value

    """ Smart generation section """
    def choseRandomElevation(self):
        return random.randint(0,4)

    def checkElevation(self,n,m):
        here = self.dataMatrix[n][m]
        direction = self.surroundings(n,m)

        tolerance = 3
        nonCharted = -1

        condition = [abs(dire-here)<tolerance or dire==nonCharted for dire in direction]

        for i in condition:
            if not i:
                return False
        return True

    def getSurroundingAverage(self,n,m):
        directions = self.surroundings(n,m)
        directions = [dir for dir in directions if dir != -1]

        return self.formatColorValue((sum(directions)/len(directions)))

    def surroundings(self,n,m):
        retour = [
            self.dataMatrix[(n+1)%self.x][(m+1)%self.y],
            self.dataMatrix[(n-1)%self.x][(m-1)%self.y],
            self.dataMatrix[(n-1)%self.x][(m+1)%self.y],
            self.dataMatrix[(n+1)%self.x][(m-1)%self.y],
            self.dataMatrix[n][(m+1)%self.y],
            self.dataMatrix[n][(m-1)%self.y],
            self.dataMatrix[(n+1)%self.x][m],
            self.dataMatrix[(n-1)%self.x][m]
        ]

        return retour

    """ Smart generation section end """

    """ Start rendering section """
    def renderAll(self):
        initDisplay(SIZEB)
        self.renderRoom()
        self.renderEntities()

        pygame.display.update()

    def renderRoom(self):
        colorMappingTile = {
            -1: non_charted,
            0: blue,
            1: yellow,
            2: green,
            3: brown,
            4: grey,

        }

        colorMappingElevation = {
            -1: non_charted,
            0: very_low,
            1: low,
            2: medium,
            3: high,
            4: very_high,
        }

        for m in range(self.y):
            for n in range(self.x):
                rect(colorMappingTile.get(self.dataMatrix[n][m]), (10*n,10*m,10,10))

        pygame.display.update()

    def renderEntities(self):
        for n in range(self.x):
            for m in range(self.y):
                if self.entityMatrix[n][m] == True:
                    rect(orange, (10*n+3.5, 10*m+3.5,3,3))

        pygame.display.update()

def main():
    for k in range(20):
        newRoom = Room(SIZE)

        newRoom.midPointGenerationStart()
        newRoom.randomEntityGen()
        newRoom.renderRoom()
        #newRoom.renderEntities()
        time.sleep(1)

if __name__ == "__main__":
    main()
