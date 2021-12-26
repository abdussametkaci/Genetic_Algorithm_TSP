class City:
    def __init__(self, index, x, y):
        self.index = index
        self.x = x
        self.y = y

    def __str__(self):
        return self.index

    def __eq__(self, other):
        return self.index == other.index

    def __hash__(self):
        return hash(self.index)
