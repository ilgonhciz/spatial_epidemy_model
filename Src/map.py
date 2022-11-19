from modelunit import ModelUnit
from station import Station
import cv2 
import numpy as np
import math
class Map:
    def __init__(self, population_map) -> None:
        self.original_resolution = [] #format x y
        self.resolution = [240, 160] #format x y
        self.total_population = 0
        self.resample(population_map)
        self.init_model()
        self.sbb_graph = dict()
    
    def resample(self, population , normalizing = True):
        self.original_resolution = population.shape[::-1]
        self.map_array = cv2.resize(population, self.resolution)
        self.map_array *= math.prod(self.original_resolution)/math.prod(self.resolution)
        if normalizing:
            self.map_array /= np.nanmax(self.map_array)
        
    def init_model(self):
        self.model_array = [[ModelUnit(self.map_array[y,x], [y,x]) if self.map_array[y,x]> 0 else None  for x in range(self.resolution[0])] for y in range(self.resolution[1])]
        for rows in self.model_array:
            for unit in rows:
                if unit:
                    unit.parent_model_array = self.model_array

    def get_map_array(self):
        return self.plot_preparation(np.array(self.map_array))

    def plot_preparation(self, default_map):
        offset = 1
        default_map = np.nan_to_num(default_map, nan = 0.8 - offset )
        modified_map = np.log((default_map + offset))
        return modified_map


if __name__ == "__main__":
    CH_map = Map()
    CH_map.resample()
    print("Finished")

  