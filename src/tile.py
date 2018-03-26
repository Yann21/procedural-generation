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
