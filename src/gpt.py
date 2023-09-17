import openai
from .config import Config
from .memory_config import MemoryConfig
from .memory import Memory


class ChatGPT:
    def __init__(self) -> None:
        openai.api_key = Config.gpt_api_key

    def check_moderation(self, prompt: str):
        moderation_resp = openai.Moderation.create(input=prompt)
        for r in moderation_resp["results"]:
            for category in Config.moderation_categories:
                if category in r["categories"] and r["categories"][category]:
                    raise Exception("Prompt contains inappropriate content.")

    def get_response(
        self,
        memory: Memory,
        mem_config: MemoryConfig,
        prompt: str,
        system_prompt: str = "",
    ):
        if not system_prompt:
            s_prompt = memory.get_system_prompt(mem_config, prompt)

        if not prompt:
            raise Exception("Prompt cannot be empty for memory responses.")

        messages = [
            s_prompt,
            {"role": "user", "content": prompt},
        ]
        # max_tokens = mem_config.max_tokens - len(str(s_prompt)) - len(str(prompt))
        completion = openai.ChatCompletion.create(
            model=mem_config.model,
            messages=messages,
        )
        return completion

    def get_no_mem_response(
        self, prompt: str, system_prompt: str = "", model: str = Config.model
    ):
        s_prompt = {"role": "system", "content": system_prompt}
        u_prompt = {"role": "user", "content": prompt}
        # max_tokens = Config.max_tokens - len(str(prompt)) - len(str(s_prompt))

        messages = []
        if system_prompt:
            messages.append(s_prompt)
        if prompt:
            messages.append(u_prompt)

        completion = openai.ChatCompletion.create(model=model, messages=messages)
        return completion

    def get_image(
        self, prompt: str, n: int = 1, size: str = "256x256", response_format="b64_json"
    ):
        image = openai.Image.create(
            prompt=prompt, size=size, n=n, response_format=response_format
        )
        return image
