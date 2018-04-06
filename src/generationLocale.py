from visual import *

N = 15
MATRICE_VIDE = [[-1 for n in range (N)] for n in range(N)]

def initField(N):
    initDisplay(N)
    for j in range(N):
        for i in range(N):
            if (i+j)%2 == 0:
                rect(red, (20*i,20*j,20,20))
            else: rect(purple, (20*i,20*j,20,20))

    pygame.display.update()


def acquisitionEntourage((x,y), maxRecDepth):
    if maxRecDepth <= 0: return

    rect(cyan, (x * 20, y * 20, 20,20))
    pygame.display.update()
    #raw_input()

    if MATRICE_VIDE[x-1][y] == -1:
        MATRICE_VIDE[x-1][y] == 1
        acquisitionEntourage((x-1,y),maxRecDepth-1)

    if MATRICE_VIDE[x][y+1] == -1:
        MATRICE_VIDE[x][y+1] == 2
        acquisitionEntourage((x,y+1),maxRecDepth-1)

    if MATRICE_VIDE[x+1][y] == -1:
        MATRICE_VIDE[x+1][y] == 1
        acquisitionEntourage((x+1,y),maxRecDepth-1)

    if MATRICE_VIDE[x][y-1] == -1:
        MATRICE_VIDE[x][y-1] == 1
        acquisitionEntourage((x,y-1),maxRecDepth-1)

initField(N)
acquisitionEntourage( ((N//2),(N//2)), 7)

raw_input()
