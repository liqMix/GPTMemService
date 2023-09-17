import os

from hyperdb import HyperDB
from .memory_config import MemoryConfig
from .config import Config


class Memory:
    def __init__(self, name: str):
        self.name = name
        self.short_memory = []
        self.db = self.init_db()

    def init_db(self):
        file_path = os.path.join(Config.data_directory, f"{self.name}.mem.gz")
        if not os.path.exists(file_path):
            return None

        db = HyperDB()
        db.load(file_path)
        return db

    def save(self):
        file_path = os.path.join(Config.data_directory, f"{self.name}.mem.gz")
        self.db.save(file_path)

    # Adds the prompt and response to the memory
    def add_to_memory(self, prompt: str, response: str, config: MemoryConfig):
        self._add_to_long_memory(prompt, response)
        self._add_to_short_memory(prompt, response, config.short_memory_length)

    # Adds to the long term memory
    def _add_to_long_memory(self, prompt: str, response: str):
        memory = f"User: {prompt}\n System: {response}"
        if not self.db:
            self.db = HyperDB()
        self.db.add_document(memory)
        self.save()

    # Adds to the short term memory
    def _add_to_short_memory(self, prompt: str, response: str, stl_length: int):
        memory = f"{prompt}{response}\n"
        self.short_memory.append(memory)
        if len(self.short_memory) > stl_length:
            self.short_memory.pop(0)

    # Gets the response from the memory
    def _get_from_long_memory(self, query: str):
        if self.db:
            return self.db.query(query, 100)
        else:
            return ""

    # Gets the response from the memory
    def _get_from_short_memory(self):
        return "\n".join(self.short_memory)

    def get_system_prompt(self, user_prompt: str, config: MemoryConfig):
        long_term = self._get_from_long_memory(user_prompt)
        short_term = self._get_from_short_memory()

        long_term_length = (
            Config.max_tokens
            - Config.response_reserve
            - len(short_term)
            - len(config.system_prompt)
        )
        while len(str(long_term)) > long_term_length and len(long_term) > 0:
            long_term.pop()
        return f"""
        {config.system_prompt}
          Relative context:
            {long_term}
          Previous conversation:
            {short_term}
        """
