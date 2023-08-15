import json
from typing import Tuple, Optional

import openai
from prompt_toolkit import prompt as pt_prompt

from copilot.tools.tool_executor import call_tool
from copilot.prompt.prompt_generator import generate_init_prompt
from copilot.utils import ReplyFormatError, pretty_print

openai.api_key = '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'

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
        raise ReplyFormatError(f'Cannot decode reply using json.loads, error\n:{str(e)}')
    return reply_json


def parse_command_from_reply(reply: dict) -> Tuple[str, dict]:
    try:
        command_info = reply['command']
        command_name = command_info['name']
        command_args = command_info['args']
    except KeyError as e:
        raise ReplyFormatError(f'Parse command error from reply, error:\n{str(e)}')
    return command_name, command_args


def convert_tool_result_to_string(name: str, returns: Optional[tuple]):
    if returns is None:
        return f'Execute tool {name} successfully, returns: None'
    content = f'Execute tool {name} successfully, returns:\n'
    if not isinstance(returns, tuple):
        returns = (returns,)
    for value in returns:
        content += f'{value}\n'
    return content


class LLMAgent:

    def __init__(self, task_prompt: str):
        init_prompt = generate_init_prompt(
            task_prompt
        )
        self.messages = [
            {'role': 'user', 'content': init_prompt}
        ]
        print('System:')
        print(init_prompt)

    def run(self):
        while True:
            res = openai.ChatCompletion.create(
                model='gpt-4',
                messages=self.messages,
                **OPENAI_COMPLETION_OPTIONS)
            reply_content = res.choices[0]['message']['content']
            print('AI:')
            try:
                reply_json = _process_llm_reply(reply_content)
                pretty_print(reply_json)
            except ReplyFormatError:
                print(reply_content)
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
            print(f'Tool:\n{command_reply}')
            self.messages += [
                {'role': 'user', 'content': command_reply},
            ]
