import json
from pathlib import Path

PROJECT_ROOT = './'
PROCESSED_DATA_PATH = PROJECT_ROOT + "processed_data/"

class File:
    def __init__(self) -> None:
        self.process_data_path = PROCESSED_DATA_PATH

    def save_processed_data(self, data_dict, file_name = "default"):
        filepath = self.process_data_path + file_name
        Path(self.process_data_path).mkdir(parents=True, exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(data_dict,f)

    def processed_data_exist(self, file_name = "default"):
        filepath = self.process_data_path + file_name
        return Path(filepath).exists()