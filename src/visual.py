import pygame

grey = (100,100,100)
green = (0,200,0)
blue = (0,0,255)
yellow = (200,200,10)
brown = (136,69,19)
red = (255,0,0)
black = (80,80,80)

very_low = (0,128,255)
low = (0,255,0)
medium = (255,255,0)
high = (255,128,0)
very_high = (255,0,0)
non_charted = (255,20,147)

SIZEB = 15
SIZE = (SIZEB, SIZEB)
NUMBER_OF_AVAILABLE_TILES = 5

#view
def initDisplay():
    pygame.init()
    gameDisplay = pygame.display.set_mode((SIZE[0] *10, SIZE[1] * 10))
    pygame.display.set_caption("Procedural Generation")

def rect(color, coord):
    pygame.draw.rect(gameDisplay,color,coord)
