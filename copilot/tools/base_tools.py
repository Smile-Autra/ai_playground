import os
import subprocess
from typing import Tuple

from prompt_toolkit import prompt as pt_prompt

from copilot.tools.tool_executor import register_tool


@register_tool(description='Write content to file')
def write_file(content: str, file_path: str, overwrite: bool = False):
    if os.path.exists(file_path) and overwrite is not True:
        raise RuntimeError(f'File {file_path} already exists, you cannot overwrite it.')
    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w') as f:
        f.write(content)


@register_tool(description='Read content from file',
               returns={'content': 'str'})
def read_file(file_path: str):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f'File {file_path} not found.')
    with open(file_path, 'r') as f:
        return f.read()


@register_tool(description='List files in directory',
               returns={'files': 'list'})
def list_dir(dir_path: str):
    if not os.path.exists(dir_path):
        raise FileNotFoundError(f'Directory {dir_path} not found.')
    return os.listdir(dir_path)


@register_tool(description='Run pytest on code',
               returns={'success': 'bool', 'output': 'str'})
def pytest_code(code_path: str) -> Tuple[bool, str]:
    try:
        output = subprocess.check_output(['python3', '-m', 'pytest', '-v', code_path])
    except subprocess.CalledProcessError as e:
        return False, e.output.decode('utf-8')
    return True, output.decode('utf-8')


@register_tool(description='Run python code by module mode: python -m <module_path>',
               returns={'success': 'bool', 'output': 'str'})
def exec_py_code(module_path: str) -> Tuple[bool, str]:
    result = subprocess.run(['python3', '-m', module_path], capture_output=True)
    if result.stderr:
        return False, f'Execute python code error:\n{result.stderr.decode("utf-8")}'
    return True, result.stdout.decode('utf-8')


@register_tool(description='Execute command in shell',
               returns={'success': 'bool', 'output': 'str'})
def exec_command(command: str) -> Tuple[bool, str]:
    result = subprocess.run(command.split(' '), capture_output=True)
    if result.stderr:
        return False, f'Execute command error:\n{result.stderr.decode("utf-8")}'
    return True, result.stdout.decode('utf-8')


@register_tool(description='Ask human question',
               returns={'answer': 'str'})
def ask_human(question: str) -> str:
    return pt_prompt(f'AI: {question}')


@register_tool(description='Task complete')
def task_complete(reason: str):
    print(f'Task complete, reason: {reason}')
    exit(0)


if __name__ == '__main__':
    print(exec_command('ls copilot/utils/*.py'))
