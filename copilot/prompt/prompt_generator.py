import os
from string import Template

from copilot.tools.tool_executor import gen_tool_prompts

PROMPT_TEMPLATE = os.path.join(os.path.dirname(__file__), 'prompt_template.txt')
ENHANCER_PROMPT = os.path.join(os.path.dirname(__file__), 'enhancer_prompt.txt')


def generate_init_prompt() -> str:
    with open(PROMPT_TEMPLATE, 'r', encoding='utf-8') as f:
        template = f.read()
    init_prompt = Template(template).substitute(
        TOOL_PROMPT=gen_tool_prompts()
    )
    return init_prompt


def generate_enhancer_prompt() -> str:
    with open(ENHANCER_PROMPT, 'r', encoding='utf-8') as f:
        prompt = f.read()
    return prompt
