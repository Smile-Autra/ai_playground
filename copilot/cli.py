import os

import click
import openai
from prompt_toolkit import prompt as pt_prompt

from copilot.agent import LLMAgent

DEFAULT_API_KEY = 'sk-BOxpA7cacbcTP94LuUXqCIyBauSynr7BLTcIudkAB3hqw9Ru'
OPENAI_COMPLETION_OPTIONS = {
    'temperature': 0.7,
    'max_tokens': 1000,
    'top_p': 1,
    'frequency_penalty': 0,
    'presence_penalty': 0
}


@click.group()
@click.pass_context
def cli(ctx):
    openai.api_base = 'https://api.aiproxy.io/v1'
    openai.api_key = os.environ.get('OPENAI_API_KEY', DEFAULT_API_KEY)


@cli.command()
@click.argument('prompt')
@click.pass_context
def run_agent(ctx, prompt: str):
    if os.path.exists(prompt):
        with open(prompt, 'r') as f:
            prompt = f.read()
    agent = LLMAgent(task_prompt=prompt)
    agent.run()


@cli.command()
@click.argument('prompt')
@click.pass_context
def chat(ctx, prompt: str):
    if os.path.exists(prompt):
        with open(prompt, 'r') as f:
            prompt = f.read()
    messages = [{"role": "user", "content": prompt}]
    while True:
        res = openai.ChatCompletion.create(
            model='gpt-4',
            messages=messages,
            **OPENAI_COMPLETION_OPTIONS)
        reply_content = res.choices[0]['message']['content']
        print('AI: ' + reply_content)
        prompt = pt_prompt('You: ')
        if prompt.lower() == 'q':
            break
        messages += [
            {"role": "assistant", "content": reply_content},
            {"role": "user", "content": prompt}
        ]
