import os
import yaml


class ServiceConfig:
    data_directory: str = "data"
    gpt_api_key: str = ""
    model: str = "gpt-3.5-turbo"
    max_tokens: int = 4096
    response_reserve: int = 2048
    max_loaded_mem: int = 1
    moderation_categories: [str] = []

    def __init__(self):
        # Read in the settings.yaml file
        with open("config.yaml", "r") as file:
            settings = yaml.safe_load(file)
        for key in settings:
            if getattr(self, key) is not None:
                setattr(self, key, settings[key])

        # Make the data directory if it doesn't exist
        if not os.path.exists(self.data_directory):
            os.mkdir(self.data_directory)


Config = ServiceConfig()
