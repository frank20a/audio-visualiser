class Dimension:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def getDiagonal(self):
        return (self.x ** 2 + self.y ** 2) ** .5

    def setDimension(self, s: tuple):
        self.x = s[0]
        self.y = s[1]

    def inverse(self):
        return Dimension(self.y, self.x)

    def __iter__(self):
        yield self.x
        yield self.y
