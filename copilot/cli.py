import os

import click
import openai
from prompt_toolkit import prompt as pt_prompt

from copilot.agent import MainAgent
from copilot.llm import ChatOpenAI, ChatMessages


@click.group()
@click.pass_context
def cli(ctx):
    openai.api_key = os.environ.get('OPENAI_API_KEY')
    ctx.obj = ChatOpenAI(api_key=openai.api_key)


@cli.command()
@click.argument('prompt')
@click.pass_context
def run_agent(ctx, prompt: str):
    if os.path.exists(prompt):
        with open(prompt, 'r') as f:
            prompt = f.read()
    main = MainAgent(task_prompt=prompt, llm=ctx.obj)
    main.run()


@cli.command()
@click.argument('prompt')
@click.pass_context
def chat(ctx, prompt: str):
    if os.path.exists(prompt):
        with open(prompt, 'r') as f:
            prompt = f.read()
    messages = ChatMessages()
    messages.add_user_message(prompt)
    while True:
        reply_str = ctx.obj.chat(messages, model='gpt-4', max_tokens=1000)
        print('AI: ' + reply_str)
        prompt = pt_prompt('You: ')
        if prompt.lower() == 'q':
            break
        messages.add_assistant_message(reply_str)
        messages.add_user_message(prompt)


if __name__ == '__main__':
    cli()
