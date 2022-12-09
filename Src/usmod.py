from file import File
from tqdm import tqdm
from data import load_USA_airport_data, load_USA_airroutes_data
from geopy import distance as geodistance
from transportation_node import TransportationNode
class USA_Air_Graph(TransportationNode):
    def __init__(self) -> None:
        super().__init__()
        self.transportation_graph_save_name = 'usa_air_graph.json'
        if File().processed_data_exist(self.transportation_graph_save_name):
            self.load_graph_from_path()
        else:
            self.usa_airport_data = load_USA_airport_data()
            self.usa_airroutes_data = load_USA_airroutes_data()
            self.determine_pos_from_df() #determines position of 'neighbors' in relation to airports
            self.initialize_usa_air_graph()

    def load_graph_from_path(self):
        graph_json = File().load_processed_data(self.transportation_graph_save_name)
        for key, station in tqdm(graph_json.items()):
            self.transportation_graph[key] = USA_Airport()
            self.transportation_graph[key].init_from_processed_json(station)

    def determine_pos_from_df(self):
        for _, row in tqdm(self.usa_airport_data.iterrows()):
            if row['IATA'] not in self.ID2pos.keys():
                self.ID2pos[row['IATA']] = {"pos":[row['Longitude'],row['Latitude']],"airport": {"ID":row['IATA'],"name":row['Name']}, "neighbour":{} }

    def initialize_usa_air_graph(self):    
        for _, rows in tqdm(self.usa_airroutes_data.iterrows()):
            for airport in [rows['Source.airport'], rows['Destination.airport']]:
                if airport == rows['Source.airport']:
                    neighbour_airport = rows['Destination.airport']
                else:
                    neighbour_airport = rows['Source.airport']
                start_pos = self.ID2pos[airport]['pos'][::-1]
                end_pos = self.ID2pos[neighbour_airport]['pos'][::-1]
                duration = geodistance.geodesic(start_pos, end_pos).km /700
                if airport not in self.transportation_graph.keys():
                    self.transportation_graph[airport] = USA_Airport()
                self.transportation_graph[airport].init_from_raw_csv(airport,self.ID2pos[airport]['airport']['name'], self.ID2pos[airport]['pos'] )  
                self.transportation_graph[airport].append_neighbour(neighbour_airport, self.ID2pos[neighbour_airport]['airport']['name'],self.ID2pos[neighbour_airport]['pos'], duration)
        self.save_to_file()

class USA_Airport:
    def __init__(self) -> None:
        self.start = True

        self.name = {"ID":"","name":""}
        self.pos = []
        self.neighbour = {}
    
    def init_from_processed_json(self, usa_airport_data_string):
        self.name = usa_airport_data_string['airport']
        self.pos = usa_airport_data_string['pos']
        self.neighbour = usa_airport_data_string['neighbour']

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

       
