from __future__ import annotations

from .memory import Memory
from .memory_config import MemoryConfig
from .config import Config


class MemoryManager:
    max_loaded: int
    loaded_memory: list[Memory] = []

    def __init__(self) -> None:
        self.max_loaded = Config.max_loaded_mem

    ## Memory Management
    # Loads a memory from file
    def _load_memory(self, name: str) -> Memory:
        memory = Memory(name)

        # Add it to the loaded memory
        self.loaded_memory.append(memory)

        # If we have too many loaded, remove the oldest
        if len(self.loaded_memory) > self.max_loaded:
            self.loaded_memory.pop(0)
        return memory

    # Gets a memory from the loaded memory, or loads it
    def get_memory(self, name: str) -> Memory:
        memory = next((m for m in self.loaded_memory if m.name == name), None)
        if not memory:
            memory = self._load_memory(name)

        return memory

    # Updates the memory if it's loaded
    def update_memory(self, config: MemoryConfig):
        memory = next((m for m in self.loaded_memory if m.name == config.name), None)
        if memory:
            memory.update_config(config)
