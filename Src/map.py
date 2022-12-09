import cv2 
import numpy as np
import math
from utils import glob2img, timeit
from modelunit import ModelUnit
from dataclasses import dataclass
from file import parameters_config
@dataclass
class BoundingBox:
    left:float = 0
    bottom: float = 0
    right:float = 0
    top:float = 0 
class Map:
    def __init__(self, population_map, graph, border, country = "CH"):
        self.resolution = parameters_config['map']['resolution'] #format x y
        
        self.transportation_graph = graph
        self.country = country
        self.border = border#BoundingBox(border.left,border.bottom, border.right, border.top)
        if country == "CH":
            self.original_resolution = population_map.shape[::-1] #format x y
        elif country == "USA":
            crop_left = 5800
            crop_right = 14000
            crop_top = 2400
            crop_bottom = 5800
            cropped_border = BoundingBox()
            cropped_border.left = self.border.left + (self.border.right - self.border.left) * crop_left / population_map.shape[1]
            cropped_border.right = self.border.left + (self.border.right - self.border.left) * crop_right / population_map.shape[1]
            cropped_border.top = self.border.top + (self.border.bottom - self.border.top) * crop_top / population_map.shape[0]
            cropped_border.bottom = self.border.top + (self.border.bottom - self.border.top) * crop_bottom / population_map.shape[0]
            self.border = cropped_border
            population_map = population_map[crop_top:crop_bottom,crop_left:crop_right]
            self.original_resolution = population_map.shape[::-1]


        self.total_population = 0
        self.resample(population_map)
        self.init_model()
        self.init_sbb_station()
        print("finished initializing")    

    def resample(self, population , normalizing = True):
        self.map_array = cv2.resize(population, self.resolution)
        #self.map_array = cv2.GaussianBlur(self.map_array,(1,1),0)
        self.map_array *= math.prod(self.original_resolution)/math.prod(self.resolution)
        if normalizing:
            self.map_array /= np.nanmax(self.map_array)
        
    def init_model(self):
        size = [0.1 *self.original_resolution[0]/self.resolution[0],0.1 *self.original_resolution[1]/self.resolution[1]]
        self.model_array = [[ModelUnit(self.map_array[y,x], [y,x], size=size) for x in range(self.resolution[0])] for y in range(self.resolution[1])]
        for rows in self.model_array:
            for unit in rows:
                unit.parent_model_array = self.model_array
                unit.transportation_graph = self.transportation_graph
                unit.isBorder()

    def init_sbb_station(self):
        station_to_delete = []
        for key, station in self.transportation_graph.transportation_graph.items():
            img_pos = glob2img(station.pos, self.border,self.resolution[::-1])
            if (0 < img_pos[0] < self.resolution[0]) and (0 < img_pos[1] < self.resolution[1]):
                if self.model_array[img_pos[1]][img_pos[0]].on_border:
                    new_posx = img_pos[0] + self.model_array[img_pos[1]][img_pos[0]].neighbour_rel_pos[1]
                    new_posy = img_pos[1] + self.model_array[img_pos[1]][img_pos[0]].neighbour_rel_pos[0]
                    img_pos = [new_posx, new_posy]   
                if not self.model_array[img_pos[1]][img_pos[0]].empty:
                    self.model_array[img_pos[1]][img_pos[0]].stations.append(station)
                    #self.model_array[img_pos[1]][img_pos[0]].population = 0.1
                else:
                    #pass
                    station_to_delete.append(key)
            else:   
                station_to_delete.append(key)
                #print("station outside switzerland")    
        for key in station_to_delete:
            for neighbour in self.transportation_graph.transportation_graph[key].neighbour.keys():
                del self.transportation_graph.transportation_graph[neighbour].neighbour[key]
            del self.transportation_graph.transportation_graph[key]
        for rows in self.model_array:
            for unit in rows:
                unit.init_neighbour_station() 

    def get_map_array(self, visualize_type="p_raw"):
        if visualize_type=="p_raw":
            return self.plot_preparation(np.array(self.map_array), base_map=True)
        if visualize_type=="p":
            return self.plot_preparation(np.array([[ unit.population for unit in row] for row in self.model_array]))
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
            
    def plot_preparation(self, default_map, base_map = False):
        offset = 1
        scaling = parameters_config['map']['plot_offset']
        #default_map = np.nan_to_num(default_map, nan = 0.5 - offset )
        if base_map:
            default_map[default_map == 0] = (0.5 - offset)/scaling
        #default_map[ default_map<= 0.001] = 0.5
        #default_map[default_map<1e-5]=1e-5
        modified_map = np.log((scaling*default_map + offset))/np.log(scaling + offset)
        modified_map[0,0] = -1
        modified_map[-1,-1] = 1
        return modified_map

    @timeit
    def update_map(self):
        for rows in self.model_array:
            for unit in rows:
                if not unit.empty:
                    unit.evolution_step()
        for rows in self.model_array:
            for unit in rows:
                if not unit.empty:
                    unit.update()
        

if __name__ == "__main__":
    CH_map = Map()
    CH_map.resample()
    print("Finished")

  