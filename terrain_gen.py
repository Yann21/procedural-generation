import random
import pygame
import time

size = 15

#view
pygame.init()
gameDisplay = pygame.display.set_mode((size *10, size * 10))
pygame.display.set_caption("Procedural Generation")

grey = (100,100,100)
green = (0,200,0)
blue = (0,0,255)
yellow = (200,200,10)
brown = (136,69,19)
red = (255,0,0)

very_low = (0,128,255)
low = (0,255,0)
medium = (255,255,0)
high = (255,128,0)
very_high = (255,0,0)
non_charted = (64,64,64)

def rect(color, coord):
    pygame.draw.rect(gameDisplay,color,coord)

pygame.display.update()

class Tile(object):
    def __init__(self, *args):
        self.POSSIBLE_TYPES = ["Water", "Sand","Grass", "Wood", "Rock"]

        if args == ():
            self.initialiseRandom()
        else:
            self.type = self.setType(args[0])

    def __repr__(self):
        return self.type

    def setType(self, num):
        return self.POSSIBLE_TYPES[num]

    def initialiseRandom(self):
        self.type = random.choice(self.POSSIBLE_TYPES)

class Room(object):
    def __init__(self, size):
        self.x = size
        self.y = size
        self.dataMatrix = [[-1 for k in range(size)] for k in range(size)]
        self.entityMatrix = [[True for k in range(size)] for k in range(size)]

    """
    def pureRandomGen(self):
        for n in range(self.x):
            for m in range(self.y):
                t = Tile()
                t.initialiseRandom()
                self.dataMatrix.append(t)
    """

    def randomEntityGen(self):
        for n in range(self.x):
            for m in range(self.y):
                self.entityMatrix[n][m] = random.uniform(0,1) > 0.97

    def smartGeneration(self):
        for m in range(self.x):
            for n in range(self.y):
                if random.randint(0,1) > 0.6 and n != 0 and m != 0:
                    test = self.getContinuity(n,m)
                    self.dataMatrix[n][m] = test

                else:
                    while True:
                        t2 = self.choseRandomElevation()
                        self.dataMatrix[n][m] = t2
                        if self.checkElevation(n,m):break

                    self.dataMatrix[n][m] = t2
                    t1 = t2

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

    def getContinuity(self,n,m):
        directions = self.surroundings(n,m)
        directions = [dir for dir in directions if dir != -1]

        return round(sum(directions)/len(directions))


    def surroundings(self,n,m):
        VARIATION = True
        if VARIATION:
            retour = [
                self.dataMatrix[(n+1)%size][(m+1)%size],
                self.dataMatrix[(n-1)%size][(m-1)%size],
                self.dataMatrix[(n-1)%size][(m+1)%size],
                self.dataMatrix[(n+1)%size][(m-1)%size],
                self.dataMatrix[n][(m+1)%size],
                self.dataMatrix[n][(m-1)%size],
                self.dataMatrix[(n+1)%size][m],
                self.dataMatrix[(n-1)%size][m]
            ]

        else:
            retour =[
                self.dataMatrix[n][(m+1)%size],
                self.dataMatrix[n][(m-1)%size],
                self.dataMatrix[(n+1)%size][m],
                self.dataMatrix[(n-1)%size][m]
            ]

        return retour

    def renderRoom(self):
        colorMappingTile = {
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

        for n in range(self.x):
            for m in range(self.y):
                rect(colorMappingTile.get(self.dataMatrix[n][m]), (10*n,10*m,10,10))

        pygame.display.update()

    def renderEntities(self):
        for n in range(self.x):
            for m in range(self.y):
                if self.entityMatrix[n][m] == True:
                    rect(red, (10*n+2.5, 10*m+2.5,5,5))

        pygame.display.update()

def main():
    for k in range(10):
        newRoom = Room(size)
        newRoom.smartGeneration()
        newRoom.randomEntityGen()
        newRoom.renderRoom()
        newRoom.renderEntities()
        time.sleep(1)

if __name__ == "__main__":
    main()
