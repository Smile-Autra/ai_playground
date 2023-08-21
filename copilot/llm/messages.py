from typing import List


class ChatMessages:

    def __init__(self):
        self._messages = []

    def add_system_message(self, content: str):
        self._messages.append({'role': 'system', 'content': content})

    def add_user_message(self, content: str):
        self._messages.append({'role': 'user', 'content': content})

    def add_assistant_message(self, content: str):
        self._messages.append({'role': 'assistant', 'content': content})

    @property
    def messages(self) -> List[str]:
        return self._messages

    @property
    def text_format(self):
        return '\n\n'.join([f'{msg["role"]}: {msg["content"]}' for msg in self._messages])
