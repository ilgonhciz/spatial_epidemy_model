import pySBB 
import numpy as np
from utils import glob2img
from file import File
from utils import timeit

class TransportationNode:
    def __init__(self):
        self.transportation_graph = dict()
        self.border = None
        self.image_size = None
        self.ID2pos={}

    def get_ID_name(self):
        return list(self.transportation_graph.keys())

    def plot_sbb_graph_from_raw(self, ax, borders, image_shape):
        for i in self.sbb_data:    
            img_pos = glob2img(i['geo_shape']['geometry']['coordinates'][0], borders, image_shape)
            img_end_pos = glob2img(i['geo_shape']['geometry']['coordinates'][-1], borders, image_shape)
            ax.plot([img_pos[0],img_end_pos[0]], [img_pos[1],img_end_pos[1]], color='green', markersize=0.9,marker='.', alpha = 0.6) 

    def plot_sub_sbb_graph_connection(self, station_list , ax, **kwargs):
        for i in range(len(station_list)-1):
            img_pos = self.get_img_pos(station_list[i])
            img_end_pos = self.get_img_pos(station_list[i+1])
            ax.plot([img_pos[0],img_end_pos[0]], [img_pos[1],img_end_pos[1]], **kwargs) 

    def plot_sub_sbb_graph(self, station_list , ax, **kwargs):
        for i in range(len(station_list)-1):
            img_pos = self.get_img_pos(station_list[i])
            for neighbourID, neighbour in self.transportation_graph[station_list[i]].neighbour.items():
                kwargs["color"] = "green"
                kwargs["linewidth"] = 1
                img_end_pos = self.get_img_pos(neighbourID)
                ax.plot([img_pos[0],img_end_pos[0]], [img_pos[1],img_end_pos[1]], **kwargs) 

    def save_to_file(self):
        export_graph = { key: station.convert2json() for key, station in self.transportation_graph.items()}
        File().save_processed_data(export_graph,self.transportation_graph_save_name)

    @timeit
    def getGraphConnection(self, startID, endID):
        queue = []
        via_list = [endID]
        queue.append([startID, None])
        explored_stations = {}
        duration = 0
        while len(queue) > 0:
            current_node, parent_node = queue.pop(0)
            if current_node not in explored_stations.keys():
                if endID == current_node:
                    queue = []           
                else:
                    for neighbourID in self.transportation_graph[current_node].neighbour.keys():
                        if neighbourID not in explored_stations.keys():
                            queue.append([neighbourID, current_node])
                if parent_node:
                    duration = self.transportation_graph[parent_node].neighbour[current_node]["duration"]
                else:
                    duration = 0
                explored_stations[current_node] = {"parent":parent_node,"duration":duration} 
        parent_node = explored_stations[endID]['parent']
        while parent_node is not startID and parent_node:
            via_list.append(parent_node)
            parent_node = explored_stations[parent_node]['parent']
            duration += explored_stations[endID]['duration']
        via_list.append(startID)
        return via_list, duration

    def getConnectionInfos(self, start_station_name, ende_station_name ):
        connections = pySBB.get_connections(start_station_name, ende_station_name)
        if len(connections) > 0:
            travel_duration = []
            for connection in connections:
                travel_duration.append(connection.duration.seconds)
                return np.mean(travel_duration)
        else:
            return False 

    def get_img_pos(self,key):
        return glob2img(self.transportation_graph[key].pos,self.border, self.image_size)
        
            