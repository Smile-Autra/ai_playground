from typing import Dict, Optional
from dataclasses import dataclass
from inspect import signature


@dataclass
class Tool:
    name: str
    description: str
    args: Dict[str, str]
    returns: Dict[str, str]


TOOLS = {}


def register_tool(description: str,
                  returns: Optional[Dict[str, str]] = None):
    def wrapper(func):
        name = func.__name__
        sig = signature(func)
        args = {name: param.annotation.__name__ for name, param in sig.parameters.items()}
        TOOLS[name] = Tool(name, description, args, returns)
        return func

    return wrapper


def call_tool(name: str, **kwargs):
    if name not in TOOLS:
        raise ValueError(f'Unknown tool: {name}')

    tool = TOOLS[name]
    return tool(**kwargs)


def _gen_single_prompt(tool: Tool):
    prompt = f'{tool.description}: "{tool.name}", args: '
    prompt += ', '.join([f'<{name}:{type}>' for name, type in tool.args.items()])
    if tool.returns is None:
        prompt += f', returns: None'
    else:
        prompt += ', returns: '
        prompt += ', '.join([f'<{name}:{type}>' for name, type in tool.returns.items()])
    return prompt


def gen_tool_prompts() -> str:
    prompt = ''
    for i, tool in enumerate(TOOLS.values()):
        prompt += f'{i + 1}. {_gen_single_prompt(tool)}\n'
    return prompt.strip('\n')
