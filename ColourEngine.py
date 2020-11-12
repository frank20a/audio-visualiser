PURPLE = (128, 0, 128)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class Colour():
    def __init__(self, rgb: tuple):
        self.rgb = rgb
        self.r = rgb[0]
        self.g = rgb[1]
        self.b = rgb[2]
        self.hash = '#' + hex(self.r)[2:] + hex(self.g)[2:] + hex(self.b)[2:]


if __name__ == '__main__':
    Magenta = Colour(MAGENTA)
    print(Magenta.hash)