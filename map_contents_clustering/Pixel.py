class Pixel:
    def __init__(self, x, y, r, g, b, layer=None):
        """ Arguments:
        x, y - coordinates, starting from top left corner,
        r, g, b - stands for red, green and blue, respectively - are RGB
        color values"""
        self._x, self._y = x, y
        self._r, self._g, self._b = r, g, b
        self.layer = layer

    def __str__(self):
        return f'Pixel at (x, y) : ({self._x}, {self._y}) has R: {self._r}, '\
               f'G: {self._g}, B: {self._b}, layer: {self.layer}'

    def rgb_to_string(self):
        return f'{self._r} {self._g} {self._b}'

    def to_list(self):
        return [self._x, self._y, self._r, self._g, self._b, self.layer]

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def r(self):
        return self._r

    @r.setter
    def r(self, value):
        if self.layer == 'cluster center':
            r = value

    @property
    def g(self):
        return self._g

    @g.setter
    def g(self, value):
        if self.layer == 'cluster center':
            g = value

    @property
    def b(self):
        return self._b

    @b.setter
    def b(self, value):
        if self.layer == 'cluster center':
            b = value
