

class ModelUnit:
    def __init__(self, population, sir_params = None):
        self.pos = []
        self.population = population if population > 0 else 0
        self.sir_params = sir_params
        self.s = 0
        self.i = 0
        self.r = 0
        self.neightbour = []
        self.station = None

    def evolution(self):
        pass
