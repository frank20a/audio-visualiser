class Dimension:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def getDiagonal(self):
        return (self.x ** 2 + self.y ** 2) ** .5

    def setDimension(self, s: tuple):
        self.x = s[0]
        self.y = s[1]


class Screen():
    def __init__(self, size: Dimension, pixel: Dimension, pxDist: int) -> None:

        self.updateSize(size, pixel, pxDist)
        self.settings = None

    def render(self):
        raise NotImplementedError()

    def updateSize(self, size: Dimension = None, pixel: Dimension = None, pxDist: int = None):
        if size is not None: self.size = size
        if pixel is not None: self.pixel = pixel
        if pxDist is not None: self.pxDist = pxDist
        self.resolution = Dimension(self.size.x * (self.pixel.x + self.pxDist) - self.pxDist,
                                    self.size.y * (self.pixel.y + self.pxDist) - self.pxDist)

    def createSettings(self, parent):
        raise NotImplementedError()
