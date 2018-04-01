from src import *
import time

def main():
    initDisplay()

    for k in range(20):
        newRoom = Room(SIZE)

        newRoom.midPointGenerationStart()
        newRoom.drought()
        newRoom.randomEntityGen()
        newRoom.renderAll()
        inp = raw_input("Press ENTER to continue.\n")
        if inp == 'e':
            newRoom.initNaturalPhenomenon()
            newRoom.renderRoom()
            raw_input("Press ENTER to continue.")

if __name__ == "__main__":
    main()
