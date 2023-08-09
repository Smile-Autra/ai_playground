import os
import click

from copilot.agent import LLMAgent


@click.command()
@click.argument('prompt_file')
def run(prompt_file: str):
    with open(prompt_file, 'r') as f:
        prompt = f.read()
    os.chdir('workspace')
    agent = LLMAgent(init_prompt=prompt)
    agent.run()


if __name__ == '__main__':
    run()
