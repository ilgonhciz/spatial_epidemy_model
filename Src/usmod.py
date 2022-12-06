import numpy
from geopy import distance
from utils import glob2img
from file import File
from tqdm import tqdm
from data import load_USA_airport_data, load_USA_airroutes_data

class USA_Air_Graph:
    def __init__(self) -> None:
        self.usa_air_graph = dict()
        self.usa_air_graph_save_name = 'usa_air_graph.json'

        self.ID2pos={"id","name","pos"}
        self.destindex = int()

        self.border = None
        self.image_size = None

        if File().processed_data_exist(self.usa_air_graph_save_name) and False:
            self.load_usa_air_graph_from_path()
        else:
            self.usa_airport_data = load_USA_airport_data()
            self.usa_airroutes_data = load_USA_airroutes_data()
            self.determine_pos() #determines position of 'neighbors' in relation to airports
            self.initialize_usa_air_graph()

    def get_ID_name(self):
        return list(self.usa_air_graph.indices())
    
    def load_usa_air_graph_from_path(self):
        usa_air_graph_json = File().load_processed_data(self.usa_air_graph_save_name)
        for key, airport in tqdm(usa_air_graph_json.items()):
            self.usa_air_graph[key] = USA_Airports()
            self.usa_air_graph[key].init_from_processed_json(airport)

    def plot_usa_air_graph_from_raw(self, ax, borders, image_shape):
        for i in self.usa_airport_data:   
            img_pos = glob2img(i['Latitude','Longitude'][0], borders, image_shape)
            img_end_pos = glob2img(i['Latitude','Longtitude'][-1], borders, image_shape)
            ax.plot([img_pos[0],img_end_pos[0]], [img_pos[1],img_end_pos[1]], color='red', markersize=0.9,marker='.', alpha = 0.6) 
    
    def plot_sub_usa_air_graph_connection(self, airport_list , ax, **kwargs):
        for i in range(len(airport_list)-1):
            img_pos = self.get_img_pos(airport_list[i])
            img_end_pos = self.get_img_pos(airport_list[i+1])
            ax.plot([img_pos[0],img_end_pos[0]], [img_pos[1],img_end_pos[1]], **kwargs)
    
    def plot_sub_usa_air_graph(self, airport_list , ax, **kwargs):
        for i in range(len(airport_list)-1):
            img_pos = self.get_img_pos(airport_list[i])
            for neighbourID, neighbour in self.usa_air_graph[airport_list[i]].neighbour.items():
                if airport_list[i] =="PLP":
                    kwargs["color"] = "red"
                    kwargs["linewidth"] = 3
                else:
                    kwargs["color"] = "green"
                    kwargs["linewidth"] = 1
                img_end_pos = self.get_img_pos(neighbourID)
                ax.plot([img_pos[0],img_end_pos[0]], [img_pos[1],img_end_pos[1]], **kwargs) 

    def determine_pos(self):
        for i in tqdm(self.usa_airport_data):
            if self.usa.airport_data['IATA'](i) not in self.ID2pos[i[key]['id']]:
                self.ID2pos[i[key]['id']] = self.usa.airport_data['IATA'](i)
                self.ID2pos[i[key]['id']['name']] = self.usa.airport_data['IATA'](i)
                self.ID2pos[i[key]['id']['name']['pos']] = self.usa.airport_data['Latitude','Longitude'](i)
            for j in tqdm(self.usa_airroutes_data):
                if self.usa.airport_data['IATA'](i) not in self.usa_airroutes_data['Source.airport'](j):   
                        
                    if self.usa.airport_data['IATA'](i) in self.ID2pos[i[key]['id']]:
                        if self.usa.airroutes_data['Source.airport'](j) in self.ID2pos[i[key]['id']['name']]: 
                            return
                        elif self.usa.airroutes_data['Destination.airport'](j) in self.ID2pos[i[key]['id']['name']]:
                            return
                        else:
                            self.ID2pos[i[key]['id']['name']] = self.usa.airroutes_data['Destination.airport'](j)
                            self.destindex = self.usa.airport_data.index(self.usa.airroutes_data['Destination.airport'](j))
                            self.ID2pos[i[key]['id']['name']['pos']] = self.usa.airport_data['Latitude','Longitude'](self.destindex)

   
    def getConnections(self):
       connections = self.usa_airroutes_data('Source.airport','Destination.airport')
       return connections

    def initialize_usa_air_graph(self, connections):
        for i in tqdm(connections):
            start_pos = i['Source.airport']
            end_pos = i['Destination.airport']
            distance = distance.geodesic(start_pos, end_pos).km
            
        for i in connections:
            if (i not in self.usa_air_graph.keys()):
                self.usa_air_graph[i[key]] = USA_Airports()
            if self.usa_air_graph.keys[i] == i['Source.airport']:
                self.usa_air_graph[i[key]].start = True
                self.usa_air_graph[i[key]].append_neighbour(i['Source.airport'], i['Destination.airport'])
            else:
                self.usa_air_graph[i[key]].start = False    
            self.usa_air_graph[i[key]].init_from_raw_json(i, self.ID2pos)
        self.save_to_file()

    def save_to_file(self,):
        export_graph = {key: airport.convert2json() for key, airport in self.usa_air_graph.items()}
        File().save_processed_data(export_graph,self.usa_air_graph_save_name)

    def getGraphConnection(self, startID, endID):
        queue = []
        via_list = [endID]
        queue.append([startID, None])
        explored_airports = {}
        while len(queue) > 0:
            current_node, parent_node = queue.pop(0)
            if current_node not in explored_airports.keys():
                if endID == current_node:
                    queue = []           
                else:
                    for neighbourID in self.usa_air_graph[current_node].neighbour.keys():
                        if neighbourID not in explored_airports.keys():
                            queue.append([neighbourID, current_node])
                explored_airports[current_node] = {"parent":parent_node,"duration":duration} 
        parent_node = explored_airports[endID]['parent']
        while parent_node is not startID and parent_node:
            via_list.append(parent_node)
            parent_node = explored_airports[parent_node]['parent']
            duration += explored_airports[endID]['duration']
        via_list.append(startID)
        return via_list, duration

    def get_img_pos(self,key):
        return glob2img(self.usa_air_graph[key].pos,self.border, self.image_size)


class USA_Airports:
    def __init__(self) -> None:
        self.start = True

        self.name = {"ID":"","name":""}
        self.pos = []
        self.connection = {}
    
    def init_from_processed_json(self, usa_airport_data_string):
        self.name = usa_airport_data_string['airport']
        self.pos = usa_airport_data_string['pos']
        self.connection = usa_airport_data_string['connection']

    def init_from_raw_csv(self, usa_airport_data_string, ID2pos):       
        self.name["ID"] = usa_airport_data_string['IATA'] 
        self.name["name"] = usa_airport_data_string['City'] 
        self.pos = ID2pos[usa_airport_data_string['Latitude']]['Longitude']
        
    def append_neighbour(self, ID, name, pos):
        self.neighbour[ID] = {"name": name, "pos":pos}

    def convert2json(self):
        export_dict = {
            "airport":self.name,
            "pos":self.pos,
            "neighbour":self.neighbour
        }
        return export_dict

       
