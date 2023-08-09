import json
from typing import Tuple, Optional

import openai
from prompt_toolkit import prompt as pt_prompt

from copilot.tools.entry import call_tool

openai.api_base = 'https://api.aiproxy.io/v1'
openai.api_key = 'sk-BOxpA7cacbcTP94LuUXqCIyBauSynr7BLTcIudkAB3hqw9Ru'

OPENAI_COMPLETION_OPTIONS = {
    'temperature': 0.7,
    'max_tokens': 1000,
    'top_p': 1,
    'frequency_penalty': 0,
    'presence_penalty': 0
}


def _process_llm_reply(reply_str: str) -> dict:
    try:
        reply_json = json.loads(reply_str)
    except json.JSONDecodeError as e:
        raise ValueError(f'Cannot decode reply using json.loads, error\n:{e}')
    return reply_json


def parse_command_from_reply(reply: dict) -> Tuple[str, dict]:
    try:
        command_info = reply['command']
        command_name = command_info['name']
        command_args = command_info['args']
    except KeyError as e:
        raise ValueError(f'Parse command error from reply, error:\n{reply}')
    return command_name, command_args


def convert_tool_result_to_string(name: str, returns: Optional[tuple]):
    if returns is None:
        return f'Execute tool {name} successfully, returns: None'
    content = f'Execute tool {name} successfully, returns:\n'
    for value in returns:
        content += f'{value}\n'
    return content


class LLMAgent:
    def __init__(self, init_prompt: str):
        self.messages = [
            {'role': 'user', 'content': init_prompt}
        ]

    def run(self):
        while True:
            res = openai.ChatCompletion.create(
                model='gpt-4',
                messages=self.messages,
                **OPENAI_COMPLETION_OPTIONS)
            reply_content = res.choices[0]['message']['content']
            print('AI: ' + reply_content)
            need_stop = pt_prompt('Continue to run? (y/n): ')
            if need_stop.lower() == 'n':
                break
            self.messages += [
                {'role': 'assistant', 'content': reply_content},
            ]
            try:
                reply_json = _process_llm_reply(reply_content)
                command_name, command_args = parse_command_from_reply(reply_json)
                result = call_tool(command_name, **command_args)
                command_reply = convert_tool_result_to_string(command_name, result)
            except Exception as e:
                command_reply = f'Occur error:\n{e}'
            print(f'Command result: {command_reply}')
            self.messages += [
                {'role': 'user', 'content': command_reply},
            ]