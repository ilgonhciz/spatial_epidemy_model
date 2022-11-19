import pySBB 
import numpy as np
from geopy import distance as geodistance
from utils import glob2img
from file import File
from tqdm import tqdm
from utils import timeit
from data import load_sbb_data

class SBBGraph:
    def __init__(self) -> None:
        #Total list elements 3117
        self.sbb_graph = dict()
        self.sbb_graph_save_name = 'sbb_graph.json'
        self.ID2pos={}

        self.border = None
        self.image_size = None

        if File().processed_data_exist(self.sbb_graph_save_name):
            self.load_sbb_graph_from_path()
        else:
            self.sbb_data = load_sbb_data()
            self.determine_pos_from_keys()
            self.initialize_sbb_graph()
    
    def get_ID_name(self):
        return list(self.sbb_graph.keys())
        #return [station.name['ID'] for station in self.sbb_graph.keys()]

    @timeit
    def load_sbb_graph_from_path(self):
        sbb_graph_json = File().load_processed_data(self.sbb_graph_save_name)
        for key, station in tqdm(sbb_graph_json.items()):
            self.sbb_graph[key] = Station()
            self.sbb_graph[key].init_from_processed_json(station)

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
            for neighbourID, neighbour in self.sbb_graph[station_list[i]].neighbour.items():
                if station_list[i] =="PLP":
                    kwargs["color"] = "red"
                    kwargs["linewidth"] = 3
                else:
                    kwargs["color"] = "green"
                    kwargs["linewidth"] = 1
                img_end_pos = self.get_img_pos(neighbourID)
                ax.plot([img_pos[0],img_end_pos[0]], [img_pos[1],img_end_pos[1]], **kwargs) 

    def determine_pos_from_keys(self):
        for i in tqdm(self.sbb_data):
            for key in ['bp_anfang','bp_ende']:
                if (i[key] not in self.ID2pos.keys()):
                    self.ID2pos[i[key]] = {"pos":[], "final":[]}
                for pos in [i['geo_shape']['geometry']['coordinates'][index] for index in [0, -1]]:
                    if len(self.ID2pos[i[key]]['pos'])<2 :
                        self.ID2pos[i[key]]['pos'].append(pos)
                    else:
                        for potential_coordinate in self.ID2pos[i[key]]['pos']: 
                            if geodistance.geodesic(pos, potential_coordinate).km < 0.3:
                                self.ID2pos[i[key]]['final'] = pos
                        self.ID2pos[i[key]]['pos'].append(pos)
        for key, pos in tqdm(self.ID2pos.items()):
            if not pos['final']:
                print(pos['pos'])
                pos['final'] = pos['pos'][-1] 

    def getConnectionInfos(self, start_station_name, ende_station_name ):
        connections = pySBB.get_connections(start_station_name, ende_station_name)
        if len(connections) > 0:
            travel_duration = []
            for connection in connections:
                travel_duration.append(connection.duration.seconds)
                return np.mean(travel_duration)
        else:
            return False 
    @timeit
    def initialize_sbb_graph(self):
        for i in tqdm(self.sbb_data):
            #connectionInfo = self.getConnectionInfos(i['bp_anf_bez'], i['bp_end_bez'])
            start_pos = i['geo_shape']['geometry']['coordinates'][0]
            end_pos = i['geo_shape']['geometry']['coordinates'][-1]
            distance = geodistance.geodesic(start_pos, end_pos).km
            if distance < 5:
                speed = 50
            elif distance < 10:
                speed = 80
            else:
                speed = 100    
            connectionInfo = distance/speed

            if connectionInfo:
                for key in ['bp_anfang','bp_ende']:
                    if (i[key] not in self.sbb_graph.keys()):
                        self.sbb_graph[i[key]] = Station()
                    if key == 'bp_anfang':
                        self.sbb_graph[i[key]].start = True
                        self.sbb_graph[i[key]].append_neighbour(i['bp_ende'], i['bp_end_bez'],self.ID2pos[i['bp_ende']]['final'], connectionInfo )
                    else:
                        self.sbb_graph[i[key]].start = False
                        self.sbb_graph[i[key]].append_neighbour(i['bp_anfang'], i['bp_anf_bez'],self.ID2pos[i['bp_anfang']]['final'], connectionInfo)
                    self.sbb_graph[i[key]].init_from_raw_json(i, self.ID2pos)
        self.save_to_file()

    def save_to_file(self):
        export_graph = { key: station.convert2json() for key, station in self.sbb_graph.items()}
        File().save_processed_data(export_graph,self.sbb_graph_save_name)

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
                    for neighbourID in self.sbb_graph[current_node].neighbour.keys():
                        if neighbourID not in explored_stations.keys():
                            queue.append([neighbourID, current_node])
                if parent_node:
                    duration = self.sbb_graph[parent_node].neighbour[current_node]["duration"]
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

    def get_img_pos(self,key):
        return glob2img(self.sbb_graph[key].pos,self.border, self.image_size)

class Station:
    def __init__(self) -> None:
        self.start = True

        self.name = {"ID":"","name":""}
        self.pos = []
        self.neighbour = {}
        #self.pos = sbb_data_string
    
    def init_from_processed_json(self, sbb_data_string):
        self.name = sbb_data_string['station']
        self.pos = sbb_data_string['pos']
        self.neighbour = sbb_data_string['neighbour']

    def init_from_raw_json(self, sbb_data_string, ID2pos):       
        if self.start:
            self.name["ID"] = sbb_data_string['bp_anfang'] 
            self.name["name"] = sbb_data_string['bp_anf_bez'] 
            self.pos = ID2pos[sbb_data_string['bp_anfang']]['final']
        else:
            self.name["ID"] = sbb_data_string['bp_ende'] 
            self.name["name"] = sbb_data_string['bp_end_bez'] 
            self.pos = ID2pos[sbb_data_string['bp_ende']]['final']

    def append_neighbour(self, ID, name, pos , duration = 0):
        self.neighbour[ID] = {"name": name, "pos":pos,'duration':duration}

    def convert2json(self):
        export_dict = {
            "station":self.name,
            "pos":self.pos,
            "neighbour":self.neighbour
        }
        return export_dict
        
                
    
    
def extract_travel_duration():
    pass

if __name__ == "__main__":
    extract_travel_duration()