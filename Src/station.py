from data import load_population
from utils import glob2img

class SBBGraph:
    def __init__(self, sbb_data) -> None:
        self.sbb_data = sbb_data
        self.sbb_graph = dict()
        for i in sbb_data:
            for key in ['bp_anfang','bp_ende']:
                if (i[key] not in self.sbb_graph.keys()):
                    self.sbb_graph[i[key]] = Station(i)
                if key == 'bp_anfang':
                    self.sbb_graph[i[key]].start = True
                    self.sbb_graph[i[key]].append_neighbour(i['bp_ende'])
                else:
                    self.sbb_graph[i[key]].start = False
                    self.sbb_graph[i[key]].append_neighbour(i['bp_anfang'])

    def plot_sbb_graph(self, ax, borders, image_shape):
        for i in self.sbb_data:            
            img_pos = glob2img(i['geo_shape']['geometry']['coordinates'][0], borders, image_shape)
            img_end_pos = glob2img(i['geo_shape']['geometry']['coordinates'][-1], borders, image_shape)
            ax.plot([img_pos[0],img_end_pos[0]], [img_pos[1],img_end_pos[1]], color='green', markersize=0.9,marker='.', alpha = 0.6) 


class Station:
    def __init__(self, sbb_data_string) -> None:
        self.raw_data = sbb_data_string
        self.start = True

        self.name = ""
        self.pos = []
        self.neighbour = {}
        #self.pos = sbb_data_string

    def init_from_string(self):
        if self.start:
            self.name = self.raw_data['bp_anfang'] 
            self.pos = self.raw_data['geo_shape']['geometry']['coordinates'][0]
        else:
            self.name = self.raw_data['bp_ende'] 
            self.pos = self.raw_data['geo_shape']['geometry']['coordinates'][-1]

    def append_neighbour(self, name):
        self.neighbour[name] = {'duration':0}        
    
    