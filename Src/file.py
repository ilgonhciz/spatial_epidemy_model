import json
from pathlib import Path
import time
timestr = time.strftime("%Y_%m_%d-%H:%M")

PROJECT_ROOT = './'
CONFIG_PATH = PROJECT_ROOT + "Config/"
PROCESSED_DATA_PATH = PROJECT_ROOT + "processed_data/"
RESULT_PATH = PROJECT_ROOT + "Results/"


class File:
    def __init__(self) -> None:
        self.process_data_path = PROCESSED_DATA_PATH
        self.result_path = RESULT_PATH
        self.config_path = CONFIG_PATH
        self.figures = []
        self.result_folder = None

    def processed_data_exist(self, file_name = "default"):
        filepath = self.process_data_path + file_name
        return Path(filepath).exists()


    def load_processed_data(self, file_name = "default"):
        filepath = self.process_data_path + file_name
        with open(filepath) as f:
            data = json.load(f)
        return data

    def load_config(self, file_name = 'parameters.json'):
        filepath = self.config_path + file_name
        with open(filepath) as f:
            config = json.load(f)
        return config 
    
    def save_processed_data(self, data_dict, file_name = "default"):
        filepath = self.process_data_path + file_name
        Path(self.process_data_path).mkdir(parents=True, exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(data_dict,f)
    
    def create_result_folder(self):
        self.result_folder = self.result_path + parameters_config['file']['result_folder']
        if Path(self.result_folder).exists():
            self.result_folder = self.result_folder[:-1] + "_" + timestr + "/"
        Path(self.result_folder).mkdir(parents=True, exist_ok=True)


    def append_fig(self, fig):
        self.figures.append(fig)

    def save_results(self, index = 0, **kwargs):
        for fig in self.figures:
            fig.savefig(self.result_folder + kwargs['country'] + "_" + str(index) + ".png")

parameters_config = File().load_config()