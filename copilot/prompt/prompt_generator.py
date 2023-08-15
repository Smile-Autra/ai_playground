import os
from string import Template

from copilot.tools.tool_executor import gen_tool_prompts

PROMPT_TEMPLATE = os.path.join(os.path.dirname(__file__), 'prompt_template.txt')


def generate_init_prompt(task: str) -> str:
    with open(PROMPT_TEMPLATE, 'r', encoding='utf-8') as f:
        template = f.read()
    init_prompt = Template(template).substitute(
        TASK_PROMPT=task,
        TOOL_PROMPT=gen_tool_prompts()
    )
    return init_prompt
