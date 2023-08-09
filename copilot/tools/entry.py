from copilot.tools.write_file import write_file
from copilot.tools.code_runner import pytest_code, exec_code


def task_complete(reason: str):
    print(f'Task completed: {reason}')
    exit(0)


TOOLS = {
    'write_file': write_file,
    'task_complete': task_complete,
    'pytest_code': pytest_code,
    'exec_code': exec_code,
}


def call_tool(name: str, **kwargs):
    if name not in TOOLS:
        raise ValueError(f'Unknown tool: {name}')

    tool = TOOLS[name]
    return tool(**kwargs)
