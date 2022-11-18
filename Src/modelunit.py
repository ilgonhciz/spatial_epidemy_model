

class ModelUnit:
    def __init__(self,local_population_density, position ,sir_params = None):
        self.pos = position
        self.parent_model_array = None
        self.population = local_population_density if local_population_density > 0 else 0
        self.sir_params = sir_params
        self.s = 0
        self.i = 0
        self.r = 0
        self.neightbour = []
        self.station = None 
        self.on_border = False

    def extract_neighbour(self):
        for delta_x in [-1, 1]:
            for delta_y in [-1, 1]:
                neighbour = self.parent_model_array[self.pos[0] + delta_y, self.pos[1] + delta_x ] 
                if neighbour is not None:
                    self.neightbour.append(neighbour)
                else:
                    self.on_border = True


    def compute_feature(self):
        pass

    def evolution(self):
        pass
