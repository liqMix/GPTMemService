import openai
from .config import Config
from .memory_config import MemoryConfig
from .memory import Memory

class ChatGPT:
    def __init__(self) -> None:
        openai.api_key = Config.gpt_api_key

    def get_response(self, memory: Memory, mem_config: MemoryConfig, prompt: str):
        s_prompt = {"role": "system", "content": memory.get_system_prompt(mem_config, prompt)}
        u_prompt = {"role": "user", "content": prompt}
        completion = openai.ChatCompletion.create(
            model=mem_config.model,
            max_tokens=mem_config.max_tokens,
            messages=[
                s_prompt,
                u_prompt,
            ],
        )
        return completion.choices[0].message["content"]

    def get_no_mem_response(self, prompt: str):
        u_prompt = {"role": "user", "content": prompt}
        max_tokens = Config.max_tokens - len(str(u_prompt))
        completion = openai.ChatCompletion.create(
            model=Config.model,
            max_tokens=max_tokens,
            messages=[
                u_prompt,
            ],
        )
        return completion.choices[0].message["content"]