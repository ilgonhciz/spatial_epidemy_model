import math
from random import random
import numpy as np
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
        #infection rate
        self.alpha = 0.01
        #recovery rate
        self.beta = 0.01
        #death rate
        self.gamma = 0.001
        #vaccination rate
        self.delta = [0.7, 0.7, 0.0]
        #percentage of the population in this ModelUnit
        self.s = self.population
        self.i = 0
        self.r = 0
        self.v = 0
        self.d = 0
        #gravity constant(first between trains, then between cells)
        self.k=[1,100]
        self.neightbour = []
        self.stations = []
        self.on_border = False

        self.inflow = 0
        self.outflow = 0

    def compute_inflow_sbb(self):
        sbb_inflow_s = 0
        sbb_inflow_i = 0
        sbb_inflow_r = 0
        sbb_inflow_v = 0
        if self.stations:
            for station in self.stations:
                for neighbourID in station.neighbour.keys():
                    neighbour_pos = self.sbb_graph.get_img_pos(neighbourID)
                    if neighbour_pos[1] >= len(self.parent_model_array) or neighbour_pos[0] >= len(
                            self.parent_model_array[0]):
                        continue
                    neighbour = self.parent_model_array[neighbour_pos[1]][neighbour_pos[0]]
                    if neighbour:
                        sbb_inflow_s += self.k[0] * neighbour.s * self.population
                        sbb_inflow_i += self.k[0] * neighbour.i * self.population
                        sbb_inflow_r += self.k[0] * neighbour.r * self.population
                        sbb_inflow_v += self.k[0] * neighbour.v * self.population
            return np.array([sbb_inflow_s, sbb_inflow_i, sbb_inflow_r, sbb_inflow_v])
        else:
            return np.array([0,0,0,0])
    def compute_outflow_sbb(self):
        sbb_outflow_s = 0
        sbb_outflow_i = 0
        sbb_outflow_r = 0
        sbb_outflow_v = 0
        if self.stations:
            for station in self.stations:
                for neighbourID in station.neighbour.keys():
                    neighbour_pos = self.sbb_graph.get_img_pos(neighbourID)
                    if neighbour_pos[1] >= len(self.parent_model_array) or neighbour_pos[0] >= len(
                        self.parent_model_array[0]):
                        continue
                    neighbour = self.parent_model_array[neighbour_pos[1]][neighbour_pos[0]]
                    if neighbour:
                        #distance not defined
                        sbb_outflow_s += self.k[0] * neighbour.population * self.s
                        sbb_outflow_i += self.k[0] * neighbour.population * self.i
                        sbb_outflow_r += self.k[0] * neighbour.population * self.r
                        sbb_outflow_v += self.k[0] * neighbour.population * self.v
            return np.array([sbb_outflow_s,sbb_outflow_i,sbb_outflow_r,sbb_outflow_v])
        else:
            return np.array([0,0,0,0])

    def compute_inflow_local(self):
        local_inflow_s = 0
        local_inflow_i = 0
        local_inflow_r = 0
        local_inflow_v = 0
        for delta_x in range(-self.cutoff_delta[0],self.cutoff_delta[0]):
            if self.pos[1] + delta_x < len(self.parent_model_array[0]):
                for delta_y in range(-self.cutoff_delta[1],self.cutoff_delta[1]):
                    if self.pos[0] + delta_y < len(self.parent_model_array):
                        if delta_x!=0 and delta_y!=0:
                            if math.sqrt(delta_x**2 + delta_y**2) <= 2*self.cutoff_radius/(self.size[0]+self.size[1]):
                                neighbour = self.parent_model_array[self.pos[0] + delta_y][self.pos[1] + delta_x ]
                                local_inflow_s += self.k[1]*neighbour.s * self.population / (delta_x ** 2 + delta_y ** 2)
                                local_inflow_i += self.k[1]*neighbour.i * self.population / (delta_x ** 2 + delta_y ** 2)
                                local_inflow_r += self.k[1]*neighbour.r * self.population / (delta_x ** 2 + delta_y ** 2)
                                local_inflow_v += self.k[1]*neighbour.v * self.population / (delta_x ** 2 + delta_y ** 2)

        return np.array([local_inflow_s,local_inflow_i,local_inflow_r,local_inflow_v])



    def compute_outflow_local(self):
        local_outflow_s = 0
        local_outflow_i = 0
        local_outflow_r = 0
        local_outflow_v = 0
        for delta_x in range(-self.cutoff_delta[0],self.cutoff_delta[0]):
            if self.pos[1] + delta_x < len(self.parent_model_array[0]):
                for delta_y in range(-self.cutoff_delta[1],self.cutoff_delta[1]):
                    if self.pos[0] + delta_y < len(self.parent_model_array):
                        if delta_x!=0 and delta_y!=0:
                            if math.sqrt(delta_x**2 + delta_y**2) <= 2*self.cutoff_radius/(self.size[0]+self.size[1]):
                                neighbour = self.parent_model_array[self.pos[0] + delta_y][self.pos[1] + delta_x]
                                local_outflow_s += self.k[1]*neighbour.population*self.s /(delta_x**2 + delta_y**2)
                                local_outflow_i += self.k[1]*neighbour.population*self.i /(delta_x**2 + delta_y**2)
                                local_outflow_r += self.k[1]*neighbour.population*self.r /(delta_x**2 + delta_y**2)
                                local_outflow_v += self.k[1]*neighbour.population*self.v /(delta_x**2 + delta_y**2)
        return np.array([local_outflow_s,local_outflow_i,local_outflow_r,local_outflow_v])

    def compute_outflow(self):
        #compute the number of people who are leaving the current region
        self.outflow = self.population
        return self.outflow

    def evolution_step(self):
        self.update_SIR()

    def update_SIR(self):
        s = self.s
        i = self.i
        r = self.r
        v = self.v
        p = self.population
        if p>0:
            x=self.compute_inflow_sbb()-self.compute_outflow_sbb()-self.compute_outflow_sbb()+self.compute_inflow_sbb()
            self.s += self.alpha * i * s / p - self.delta[0]*s+x[0]
            self.i += self.alpha * i * s / p - (self.beta + self.gamma) * i - self.delta[1] * i+x[1]
            self.r += self.beta * i - self.delta[2] * r+x[2]
            self.v += self.delta[0] * s + self.delta[1] * i + self.delta[2] * r+x[3]
           # self.s = max(0, self.s)
           # self.i = max(0, self.i)
           # self.r = max(0, self.r)
           # self.v = max(0, self.v)

            self.population = self.s + self.i + self.r + self.v
            self.d += self.gamma * i
