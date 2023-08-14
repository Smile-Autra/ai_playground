import os

import click
import openai

from copilot.agent import LLMAgent


@click.group()
@click.pass_context
def cli(ctx):
    openai.api_key = os.environ['OPENAI_API_KEY']


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
@click.argument('prompt_file')
@click.pass_context
def chat(ctx, prompt_file: str):
    pass
