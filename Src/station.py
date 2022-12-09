from geopy import distance as geodistance
from file import File
from tqdm import tqdm
from utils import timeit
from data import load_sbb_data
from transportation_node import TransportationNode
class SBBGraph(TransportationNode):
    def __init__(self) -> None:
        super().__init__()
        self.transportation_graph_save_name = 'sbb_graph.json'        
        if File().processed_data_exist(self.transportation_graph_save_name):
            self.load_graph_from_path()
        else:
            self.sbb_data = load_sbb_data()
            self.determine_pos_from_keys()
            self.initialize_sbb_graph()
    
    @timeit
    def load_graph_from_path(self):
        sbb_graph_json = File().load_processed_data(self.transportation_graph_save_name)
        for key, station in tqdm(sbb_graph_json.items()):
            self.transportation_graph[key] = Station()
            self.transportation_graph[key].init_from_processed_json(station)
    
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
                    if (i[key] not in self.transportation_graph.keys()):
                        self.transportation_graph[i[key]] = Station()
                    if key == 'bp_anfang':
                        self.transportation_graph[i[key]].start = True
                        self.transportation_graph[i[key]].append_neighbour(i['bp_ende'], i['bp_end_bez'],self.ID2pos[i['bp_ende']]['final'], connectionInfo )
                    else:
                        self.transportation_graph[i[key]].start = False
                        self.transportation_graph[i[key]].append_neighbour(i['bp_anfang'], i['bp_anf_bez'],self.ID2pos[i['bp_anfang']]['final'], connectionInfo)
                    self.transportation_graph[i[key]].init_from_raw_json(i, self.ID2pos)
        self.save_to_file()

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