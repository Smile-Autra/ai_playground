from typing import Optional

import openai
from retry import retry

from copilot.llm.messages import ChatMessages


class ChatOpenAI:

    def __init__(self, api_key: str, api_base: Optional[str] = None):
        if api_base is not None:
            openai.api_base = api_base
        openai.api_key = api_key

    @retry(tries=3, delay=0.1)
    def chat(self,
             chat_messages: ChatMessages,
             model='gpt-3.5-turbo',
             max_tokens=1000,
             temperature=0.7,
             frequency_penalty=0,
             presence_penalty=0):
        reply = openai.ChatCompletion.create(
            model=model,
            messages=chat_messages.messages,
            max_tokens=max_tokens,
            temperature=temperature,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty)
        return reply['choices'][0]['message']['content']
