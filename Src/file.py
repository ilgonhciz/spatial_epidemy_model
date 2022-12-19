import json
from pathlib import Path
import time
import shutil
from glob import glob


timestr = time.strftime("%Y_%m_%d-%H_%M")

PROJECT_ROOT = './'
CONFIG_PATH = PROJECT_ROOT + "Config/"
PROCESSED_DATA_PATH = PROJECT_ROOT + "processed_data/"
RESULT_PATH = PROJECT_ROOT + "Results/"


class File:
    def __init__(self) -> None:
        self.process_data_path = PROCESSED_DATA_PATH
        self.result_path = RESULT_PATH
        self.config_path = CONFIG_PATH
        self.config_file = None
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
    
    def create_result_folder(self, file_name = 'parameters.json'):
        self.result_folder = self.result_path + parameters_config['file']['result_folder']
        if Path(self.result_folder).exists():
            self.result_folder = self.result_folder[:-1] + "_" + timestr + "/"
        Path(self.result_folder).mkdir(parents=True, exist_ok=True)
        shutil.copyfile(self.config_path + file_name, self.result_folder + file_name)


    def get_fig_path(self, subdirectory = None ,fig_names = []):
        if not subdirectory:
            self.result_folder = self.result_path + parameters_config['file']['result_folder']
        else:
            self.result_folder = subdirectory
        return [sorted(glob(self.result_folder + key + "/" + "*.png"), key=lambda x:float(x.split("_")[-1].split(".")[0]) ) for key in fig_names]

    def append_fig(self, fig, **kwargs):
        self.figures.append([fig, kwargs])

    def save_results(self, index = 0, **kwargs):
        for [fig, fig_args] in self.figures:
            result_folder = self.result_folder + fig_args['name'] + "/"
            Path(result_folder).mkdir(parents=True, exist_ok=True)
            fig.savefig(result_folder + kwargs['country'] + "_" + str(index) + ".png", bbox_inches='tight', dpi=200)

parameters_config = File().load_config()