import openai
from .config import Config


class ChatGPT:
    def __init__(self) -> None:
        openai.api_key = Config.gpt_api_key

    def get_response(self, system_prompt: str, prompt: str):
        s_prompt = {"role": "system", "content": system_prompt}
        u_prompt = {"role": "user", "content": prompt}
        max_tokens = Config.max_tokens - len(str(s_prompt)) - len(str(u_prompt))
        completion = openai.ChatCompletion.create(
            model=Config.gpt_model,
            max_tokens=max_tokens,
            messages=[
                s_prompt,
                u_prompt,
            ],
        )
        return completion.choices[0].message["content"]
