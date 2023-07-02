import openai
from .config import Config


class ChatGPT:
    def __init__(self) -> None:
      openai.api_key = Config.gpt_api_key

    def get_response(self, system_prompt: str, prompt: str):
        max_tokens = Config.max_tokens - len(system_prompt) - len(prompt)
        completion = openai.ChatCompletion.create(
            model=Config.gpt_model,
            max_tokens=max_tokens,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
        )
        return completion.choices[0].message["content"]
