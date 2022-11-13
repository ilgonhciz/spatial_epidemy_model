from data import load_population, load_sbb_data
from modelunit import ModelUnit
from station import Station
import cv2 
import numpy as np

class Map:
    def __init__(self) -> None:
        self.resolution = [400, 200]
        self.total_population = 0
        self.resample()
        self.init_model()
        self.sbb_graph = dict()
    
    def resample(self):
        _, population = load_population()
        self.map_array = cv2.resize(population, self.resolution)
        
    def init_model(self):
        self.model_array = [[ModelUnit(self.map_array[y,x]) for x in range(self.resolution[0])] for y in range(self.resolution[1])]

    def get_map_array(self):
        return np.array(self.map_array)


if __name__ == "__main__":
    CH_map = Map()
    CH_map.resample()
    print("Finished")

  