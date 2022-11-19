import math
from random import random

class ModelUnit:
    def __init__(self,local_population_density, position ,sir_params = None, size = [1, 1]):
        self.pos = position
        self.size = size

        self.parent_model_array = None
        self.sbb_graph = None

        self.cutoff_radius = 5 #km
        self.cutoff_delta = [int(self.cutoff_radius//size[0]), int(self.cutoff_radius//size[1])]
        self.population = local_population_density if local_population_density > 0 else 0
        self.sir_params = sir_params

        #percentage of the population in this ModelUnit 
        self.s = self.population
        self.i = 0
        self.r = 0

        self.neightbour = []
        self.stations = []
        self.on_border = False

        self.inflow = 0
        self.outflow = 0
   
    def compute_inflow_sbb(self):
        sbb_inflow = 0
        if self.stations:
            for station in self.stations:
                for neighbourID in station.neighbour.keys():
                    neighbour_pos = self.sbb_graph.get_img_pos(neighbourID)
                    if neighbour_pos[1] >= len(self.parent_model_array) or neighbour_pos[0] >= len(self.parent_model_array[0]):
                        continue
                    neighbour_unit = self.parent_model_array[neighbour_pos[1]][neighbour_pos[0]]
                    if neighbour_unit:
                        sbb_inflow += neighbour_unit.compute_outflow()
            return sbb_inflow
        else:
            return 0
        
    def compute_outflow_sbb(self):
        neighbour_inflow = 0
        if self.stations:
            for station in self.stations:
                for neighbourID in station.neighbour.keys():
                    neighbour_pos = self.sbb_graph.get_img_pos(neighbourID)
                    neighbour_unit = self.parent_model_array[neighbour_pos[1]][neighbour_pos[0]]
                    neighbour_inflow += neighbour_unit.compute_outflow()
        return self.outflow + neighbour_inflow

    def compute_inflow_local(self):
        local_inflow = 0 
        for delta_x in range(-self.cutoff_delta[0],self.cutoff_delta[0]):
            if self.pos[1] + delta_x < len(self.parent_model_array[0]):
                for delta_y in range(-self.cutoff_delta[1],self.cutoff_delta[1]):
                    if self.pos[0] + delta_y < len(self.parent_model_array):
                        if math.sqrt(delta_x**2 + delta_y**2) <= 2*self.cutoff_radius/(self.size[0]+self.size[1]):
                            neighbour = self.parent_model_array[self.pos[0] + delta_y][self.pos[1] + delta_x ] 
                            local_inflow += neighbour.outflow / (math.sqrt(delta_x**2 + delta_y**2)+ 1)
        return local_inflow

    def compute_inflow(self):
        #extract the number of infected people coming from the outside
        self.inflow = self.compute_inflow_sbb() + self.compute_inflow_local()
        return self.inflow

    def compute_outflow(self):
        #compute the number of people who are leaving the current region
        self.outflow = self.population * self.i
        return self.outflow

    def evolution_step(self):
        self.compute_inflow()
        self.compute_outflow()
        self.update_SIR()

    def update_SIR(self):
        input = self.inflow
        self.i = 1.05 * (self.i + 0.1* input/self.population) if self.population > 0 else 0
        self.s = 1 - self.i
        self.r = 0

