from modelunit import ModelUnit
import cv2 
import numpy as np
import math
from utils import glob2img
from station import SBBGraph
class Map:
    def __init__(self, population_map, sbb_graph, border):
        self.sbb_graph = sbb_graph
        self.border = border
        self.original_resolution = [] #format x y
        self.resolution = [160, 80] #format x y
        self.total_population = 0
        self.resample(population_map)
        self.init_model()
        self.init_sbb_station()
        print("finished initializing")
    
    def resample(self, population , normalizing = True):
        self.original_resolution = population.shape[::-1]
        self.map_array = cv2.resize(population, self.resolution)
        self.map_array *= math.prod(self.original_resolution)/math.prod(self.resolution)
        if normalizing:
            self.map_array /= np.nanmax(self.map_array)
        
    def init_model(self):
        size = [0.1 *self.original_resolution[0]/self.resolution[0],0.1 *self.original_resolution[1]/self.resolution[1]]
        self.model_array = [[ModelUnit(self.map_array[y,x], [y,x], size=size) for x in range(self.resolution[0])] for y in range(self.resolution[1])]
        for rows in self.model_array:
            for unit in rows:
                if unit:
                    unit.parent_model_array = self.model_array
                    unit.sbb_graph = self.sbb_graph
    
    def init_sbb_station(self):
        station_to_delete = []
        for key, station in self.sbb_graph.sbb_graph.items():
            img_pos = glob2img(station.pos, self.border,self.resolution[::-1])
            if (0 < img_pos[0] < self.resolution[0]) and (0 < img_pos[1] < self.resolution[1]):
                if isinstance(self.model_array[img_pos[1]][img_pos[0]], ModelUnit):   
                    self.model_array[img_pos[1]][img_pos[0]].stations.append(station)
                    #self.model_array[img_pos[1]][img_pos[0]].population = 0.1
                else:
                    station_to_delete.append(key)
            else:   
                station_to_delete.append(key)
                #print("station outside switzerland")    
        for key in station_to_delete:
            for neighbour in self.sbb_graph.sbb_graph[key].neighbour.keys():
                del self.sbb_graph.sbb_graph[neighbour].neighbour[key]
            del self.sbb_graph.sbb_graph[key]

    def get_map_array(self, visualize_type="p"):
        if visualize_type=="p":
            return self.plot_preparation(np.array(self.map_array))
        elif visualize_type=="i":
            return self.plot_preparation(np.array([[ unit.i for unit in row] for row in self.model_array]))
        elif visualize_type=="s":
            return self.plot_preparation(np.array([[ unit.s for unit in row] for row in self.model_array]))
        elif visualize_type=='r':
            return self.plot_preparation(np.array([[unit.r for unit in row] for row in self.model_array]))
        elif visualize_type=='v':
            return self.plot_preparation(np.array([[unit.v for unit in row] for row in self.model_array]))
        else:
            return self.plot_preparation(np.array([[unit.d for unit in row] for row in self.model_array]))
    def plot_preparation(self, default_map):
        offset = 1
        default_map = np.nan_to_num(default_map, nan = 0.8 - offset )
        #default_map[default_map<1e-5]=1e-5
        modified_map = np.log((default_map + offset))
        return modified_map

    def update_map(self):
        for rows in self.model_array:
            for unit in rows:
                if unit:
                    unit.evolution_step()
        


if __name__ == "__main__":
    CH_map = Map()
    CH_map.resample()
    print("Finished")

  