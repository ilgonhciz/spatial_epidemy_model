import pySBB 
import numpy as np
import json
from data import load_population
from utils import glob2img
from file import File


class SBBGraph:
    def __init__(self, sbb_data) -> None:
        self.sbb_data = sbb_data
        self.sbb_graph = dict()

        self.sbb_graph_save_name = 'sbb_graph.json'

        if File().processed_data_exist(self.sbb_graph_save_name) and False:
            self.load_sbb_graph_from_path()
        else:
            self.initialize_sbb_graph()
        """for i in sbb_data:
            connectionInfo = self.getConnectionInfos(i['bp_anf_bez'], i['bp_end_bez'])
            print(connectionInfo)
            if connectionInfo:
                for key in ['bp_anfang','bp_ende']:
                    if (i[key] not in self.sbb_graph.keys()):
                        self.sbb_graph[i[key]] = Station(i)
                    if key == 'bp_anfang':
                        self.sbb_graph[i[key]].start = True
                        self.sbb_graph[i[key]].append_neighbour(i['bp_ende'])
                    else:
                        self.sbb_graph[i[key]].start = False
                        self.sbb_graph[i[key]].append_neighbour(i['bp_anfang'])
        """
    def load_sbb_graph_from_path(self):
        pass
        



    def plot_sbb_graph(self, ax, borders, image_shape):
        for i in self.sbb_data:            
            img_pos = glob2img(i['geo_shape']['geometry']['coordinates'][0], borders, image_shape)
            img_end_pos = glob2img(i['geo_shape']['geometry']['coordinates'][-1], borders, image_shape)
            ax.plot([img_pos[0],img_end_pos[0]], [img_pos[1],img_end_pos[1]], color='green', markersize=0.9,marker='.', alpha = 0.6) 

    def getConnectionInfos(self, start_station_name, ende_station_name ):
        connections = pySBB.get_connections(start_station_name, ende_station_name)
        if len(connections) > 0:
            travel_duration = []
            for connection in connections:
                travel_duration.append(connection.duration.seconds)
                return np.mean(travel_duration)
        else:
            return False 

    def initialize_sbb_graph(self):
        for i in self.sbb_data:
            connectionInfo = self.getConnectionInfos(i['bp_anf_bez'], i['bp_end_bez'])
            print(connectionInfo)
            if connectionInfo:
                for key in ['bp_anfang','bp_ende']:
                    if (i[key] not in self.sbb_graph.keys()):
                        self.sbb_graph[i[key]] = Station(i)
                    if key == 'bp_anfang':
                        self.sbb_graph[i[key]].start = True
                        self.sbb_graph[i[key]].append_neighbour(i['bp_ende'], i['bp_end_bez'],i['geo_shape']['geometry']['coordinates'][-1], connectionInfo )
                    else:
                        self.sbb_graph[i[key]].start = False
                        self.sbb_graph[i[key]].append_neighbour(i['bp_anfang'], i['bp_anf_bez'],i['geo_shape']['geometry']['coordinates'][0], connectionInfo)
                    self.sbb_graph[i[key]].init_from_string()
        self.save_to_file()

    def save_to_file(self):
        export_graph = { key: station.convert2json() for key, station in self.sbb_graph.items()}
        File().save_processed_data(export_graph,self.sbb_graph_save_name)

class Station:
    def __init__(self, sbb_data_string) -> None:
        self.raw_data = sbb_data_string
        self.start = True

        self.name = {"ID":"","name":""}
        self.pos = []
        self.neighbour = {}
        #self.pos = sbb_data_string

    def init_from_string(self):
        if self.start:
            self.name["ID"] = self.raw_data['bp_anfang'] 
            self.name["name"] = self.raw_data['bp_anf_bez'] 
            self.pos = self.raw_data['geo_shape']['geometry']['coordinates'][0]
        else:
            self.name["ID"] = self.raw_data['bp_ende'] 
            self.name["name"] = self.raw_data['bp_end_bez'] 
            self.pos = self.raw_data['geo_shape']['geometry']['coordinates'][-1]

    def append_neighbour(self, ID, name, pos , duration = 0):
        self.neighbour[ID] = {"name": name, "pos":pos,'duration':duration}

    def convert2json(self):
        export_dict = {
            "station":self.name,
            "pos":self.pos,
            "neighbour":self.neighbour
        }
        return export_dict

    def init_from_json(self ):
        pass
                
    
    
def extract_travel_duration():
    pass

if __name__ == "__main__":
    extract_travel_duration()