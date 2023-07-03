from __future__ import annotations
import os
import yaml
from .config import Config


class MemoryConfig:
    # Name of the memory, used for accessing
    name: str

    # Prompt related
    short_memory_length: int = 3  # How many previous prompts to include
    system_prompt: str = ""  # The prompt to use for system messages

    # Stat related
    total_completions: int = 0  # The total number of completions
    total_response_time: float = 0  # The total response time

    @staticmethod
    def get_configs() -> list[dict]:
        memories = []
        for file in os.listdir(Config.data_directory):
            if file.endswith(".yaml"):
                name = file.split(".yaml")[0]
                memories.append(MemoryConfig(name).__dict__())
        return memories

    def __dict__(self) -> dict:
      
        return {
            "name": self.name,
            "short_memory_length": self.short_memory_length,
            "total_completions": self.total_completions,
            "total_response_time": self.total_response_time,
            "average_response_time": self.total_response_time / (self.total_completions or 1),
            "system_prompt": self.system_prompt,
        }

    def __init__(self, name: str) -> None:
        self.load(name)

    def create(self, name: str):
        self.name = name
        self.save()

    def save(self):
        file_path = os.path.join(Config.data_directory, f"{self.name}.yaml")
        with open(file_path, "w") as file:
            yaml.dump(
                self.__dict__(),
                file,
            )

    def load(self, name: str):
        file_path = os.path.join(Config.data_directory, f"{name}.yaml")
        if not os.path.exists(file_path):
            self.create(name)
            return

        with open(file_path, "r") as file:
            memory_config = yaml.safe_load(file)

        self.name = memory_config["name"]
        self.short_memory_length = memory_config["short_memory_length"]
        self.system_prompt = memory_config["system_prompt"]
        self.total_completions = memory_config["total_completions"]
        self.total_response_time = memory_config["total_response_time"]

    def update(self, data: dict):
        if "system_prompt" in data:
            self.system_prompt = data["system_prompt"]
        if "short_memory_length" in data:
            self.short_memory_length = int(data["short_memory_length"])
        self.save()

    def process_completion(self, response_time: int):
        self.total_completions += 1
        self.total_response_time += response_time
        self.save()
