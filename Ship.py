class Ship:
    pos_x = 0
    pos_y = 0
    size = 0

    #every ship has the origin in the head of the body
    #direction is moving clockwise from 0 to 3
    #   0   x000    x   000x
    #   0           0
    #   0           0
    #   x           0
    dir = 0

    def __init__(self, pos_x, pos_y, size, dir):
        self.x = pos_x
        self.y = pos_y
        self.size = size
        self.dir = dir

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_size(self):
        return self.size

    def get_dir(self):
        return self.dir


