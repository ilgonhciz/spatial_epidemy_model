import math
import numpy as np
from random import random
from file import parameters_config
class ModelUnit:
    def __init__(self,local_population_density, position, size = [1, 1]):
        self.cutoff_radius = parameters_config["modelunit"]["cutoff_radius"] #km
        self.delta = parameters_config["modelunit"]["delta"]
        self.gamma = parameters_config["modelunit"]["gamma"]
        self.alpha = parameters_config["modelunit"]["alpha"]
        self.beta = parameters_config["modelunit"]["beta"]
        
        self.pos = position
        self.size = size

        self.parent_model_array = None
        self.transportation_graph = None


        self.cutoff_delta = [int(self.cutoff_radius//size[0]), int(self.cutoff_radius//size[1])]
        self.population = local_population_density if local_population_density > 1e-5 else 0
        self.empty = False if local_population_density > 1e-5 else True
        

        #percentage of the population in this ModelUnit 
        self.s = self.population
        self.i = 0
        self.r = 0
        self.v = 0
        self.d = 0

        self.neightbour_stations = []
        self.stations = []
        self.on_border = False
        self.neighbour_rel_pos = [0,0]

        self.inflow = 0
        self.outflow = 0

    def init_neighbour_station(self):
        if self.stations:
            for station in self.stations:
                for neighbourID, neighbour in station.neighbour.items():
                    if neighbourID not in self.neightbour_stations and neighbourID not in [station.name["ID"] for station in self.stations]:
                        self.neightbour_stations.append([neighbourID, neighbour['duration']])
    
    def compute_inflow_transport(self):
        transportation_inflow = 0
        if self.stations:
            for neighbourID, duration in self.neightbour_stations:
                neighbour_pos = self.transportation_graph.get_img_pos(neighbourID)
                if neighbour_pos[1] >= len(self.parent_model_array) or neighbour_pos[0] >= len(self.parent_model_array[0]):
                    continue
                neighbour_unit = self.parent_model_array[neighbour_pos[1]][neighbour_pos[0]]
                if neighbour_unit:
                    transportation_inflow += (neighbour_unit.compute_outflow() if neighbour_unit.i < 0.00001 else 0) * (self.cutoff_radius/ 10) / (duration) 
            return transportation_inflow
        else:
            return 0


    def compute_inflow_local(self):
        local_inflow = 0 
        for delta_x in range(-self.cutoff_delta[0],self.cutoff_delta[0]+1):
            if self.pos[1] + delta_x >= len(self.parent_model_array[0]) or self.pos[1] + delta_x < 0:
                continue
            for delta_y in range(-self.cutoff_delta[1],self.cutoff_delta[1]+1):
                if self.pos[0] + delta_y >= len(self.parent_model_array) or self.pos[0] + delta_y < 0:
                    continue
                if math.sqrt(delta_x**2 + delta_y**2) <= 2*self.cutoff_radius/(self.size[0]+self.size[1]):
                    if delta_x != 0 or delta_y!=0:
                        if not self.parent_model_array[self.pos[0] + delta_y][self.pos[1] + delta_x ].empty:
                            neighbour = self.parent_model_array[self.pos[0] + delta_y][self.pos[1] + delta_x ] 
                            local_inflow += neighbour.outflow / ( math.sqrt(delta_x**2 + delta_y**2))
        return local_inflow

    def compute_inflow(self):
        #extract the number of infected people coming from the outside
        self.inflow = self.compute_inflow_transport() + self.compute_inflow_local() # +
        return self.inflow * self.population
        #return 0

    def compute_outflow(self):
        #compute the number of people who are leaving the current region
        self.outflow = self.i * 0.1 
        return self.outflow

    def evolution_step(self):
        self.compute_inflow()
        self.compute_outflow()

    def update(self):
        self.update_SIR()

    def isBorder(self):
        has_neighbour = False
        if self.empty:
            for delta_pos in [[0,1],[0,-1],[1,0],[-1,0],[-1,1],[-1,-1],[1,1],[1,-1]]: 
                if self.pos[1]+ delta_pos[1] >= len(self.parent_model_array[0]) or self.pos[1]+ delta_pos[1] < 0:
                    continue
                if self.pos[0]+ delta_pos[0] >= len(self.parent_model_array) or self.pos[0]+ delta_pos[0] < 0:
                    continue
                if not self.parent_model_array[self.pos[0]+ delta_pos[0]][self.pos[1]+ delta_pos[1]].empty:
                    has_neighbour = True
                    self.neighbour_rel_pos = delta_pos
                    #self.population = 1
                    break
        self.on_border = self.empty and has_neighbour

    def update_SIR(self):
        input = min(self.s, self.inflow)
        s = self.s
        i = self.i
        r = self.r
        v = self.v
        p = self.population
        if p>0:
            self.s = s - self.alpha * i * s / p - self.delta[0]*s - input
            self.i = i + self.alpha * i * s / p - (self.beta + self.gamma) * i - self.delta[1] * i + input
            self.r = r + self.beta * i - self.delta[2] * r
            self.v = v + self.delta[0] * s + self.delta[1] * i + self.delta[2] * r
            self.s = min(max(0, self.s), self.population)
            self.i = min(max(0, self.i), self.population)
            self.r = min(max(0, self.r), self.population)
            self.v = min(max(0, self.v), self.population)
            self.population = self.s + self.i + self.r + self.v

            self.d += self.gamma * i
