import json
from typing import Optional

from prompt_toolkit import prompt as pt_prompt

from copilot.agents.task_refine import refine_task_description
from copilot.llm import ChatOpenAI, ChatMessages
from copilot.prompt.prompt_generator import generate_init_prompt
from copilot.tools.tool_executor import call_tool
from copilot.utils import ReplyFormatError, pretty_print


def _process_llm_reply(reply_str: str) -> dict:
    try:
        reply_json = json.loads(reply_str)
    except json.JSONDecodeError as e:
        raise ReplyFormatError(f'Cannot decode reply using json.loads, error\n:{str(e)}')
    return reply_json


def convert_tool_result_to_string(name: str, returns: Optional[tuple]):
    if returns is None:
        return f'Execute tool {name} successfully, returns: None'
    content = f'Execute tool {name} successfully, returns:\n'
    if not isinstance(returns, tuple):
        returns = (returns,)
    for value in returns:
        content += f'{value}\n'
    return content


def run_commands(reply: dict) -> str:
    return_str_list = []
    try:
        command_list = reply['commands']
        for cmd in command_list:
            command_name = cmd['name']
            command_args = cmd['args']
            res = call_tool(command_name, **command_args)
            return_str_list.append(convert_tool_result_to_string(command_name, res))
    except KeyError as e:
        raise ReplyFormatError(f'Parse command error from reply, error:\n{str(e)}')
    return '\n\n'.join(return_str_list)


class MainAgent:

    def __init__(self, task_prompt: str, llm: ChatOpenAI):
        self._llm = llm
        task_prompt = refine_task_description(self._llm, task_prompt, model='gpt-3.5-turbo')
        init_prompt = generate_init_prompt()
        print('System:')
        print(init_prompt)
        print('User:')
        print(task_prompt)
        self.messages = ChatMessages()
        self.messages.add_system_message(init_prompt)
        self.messages.add_user_message(task_prompt)

    def run(self):
        while True:
            reply_str = self._llm.chat(self.messages, model='gpt-4', max_tokens=1000)
            print('AI:')
            try:
                reply_json = _process_llm_reply(reply_str)
                pretty_print(reply_json)
            except ReplyFormatError:
                print(reply_str)
            need_stop = pt_prompt('Continue to run? (y/n): ')
            if need_stop.lower() == 'n':
                break
            self.messages.add_assistant_message(reply_str)
            try:
                reply_json = _process_llm_reply(reply_str)
                command_reply = run_commands(reply_json)
            except Exception as e:
                command_reply = f'Occur error:\n{e}'
            print(f'Tool:\n{command_reply}')
            self.messages.add_user_message(command_reply)
