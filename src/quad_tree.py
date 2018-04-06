class QuadTree(object):
    def __init__(self, u,d,l,r, data):
        self.u = u
        self.d = d
        self.l = l
        self.r = r

        self.data = data

    """
    def __str__(self):
        u = self.u
        d = self.d
        l = self.l
        r = self.r

        if u == None:
            u = "None"

        if d == None:
            d = "None"

        if l == None:
            l = "None"

        if r == None:
            r = "None"

        string = "Up: {}, Down: {}, Left: {}, Right: {}".format(u, d, l, r)
    """

    """
    def setValue(x):
        if x == -1: return None
        else: return x
    """

    def initQuadTree(matrix):
        x = len(matrix) // 2
        y = x

        createQuadTreeFromMatrix(matrix, (x,y))

MATRICE_TEST = [[-1 for n in range(10)] for m in range(10)]

def createQuadTreeFromMatrix(matrix, (x,y)):
    currentNode = matrix[x][y]
    #init
    if type(currentNode) is not QuadTree:
        matrix[x][y] = QuadTree(None, None, None, None, False)
        matrix[x][y].u = QuadTree(None, None, None, None, False),
        matrix[x][y].d = QuadTree(None, None, None, None, False),
        matrix[x][y].l = QuadTree(None, None, None, None, False),
        matrix[x][y].r = QuadTree(None, None, None, None, False),

    #init surroundings
    matrix[x][y+1] = QuadTree(None,matrix[x][y],None,None, False)
    matrix[x][y-1] = QuadTree(matrix[x][y],None,None,None, False)
    matrix[x-1][y] = QuadTree(None,None,None,matrix[x][y], False)
    matrix[x+1][y] = QuadTree(None,None,matrix[x][y],None, False)

    #pointer to surroundings
    matrix[x][y].u = matrix[x][y+1],
    matrix[x][y].d = matrix[x][y-1],
    matrix[x][y].l = matrix[x-1][y],
    matrix[x][y].r = matrix[x+1][y],

#createQuadTreeFromMatrix(MATRICE_TEST, (len(MATRICE_TEST)//2, len(MATRICE_TEST)//2))



(x,y) = (len(matrix)//2,len(matrix)//2)
