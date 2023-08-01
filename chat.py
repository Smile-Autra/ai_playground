import click
import openai
from prompt_toolkit import prompt as pt_prompt

openai.api_base = 'https://api.aiproxy.io/v1'
openai.api_key = 'sk-BOxpA7cacbcTP94LuUXqCIyBauSynr7BLTcIudkAB3hqw9Ru'

OPENAI_COMPLETION_OPTIONS = {
    'temperature': 0.7,
    'max_tokens': 1000,
    'top_p': 1,
    'frequency_penalty': 0,
    'presence_penalty': 0
}


@click.command()
@click.argument('prompt_file')
def entry(prompt_file: str):
    print('Start chat with LLM, press q/Q to exit.')
    with open(prompt_file, 'r') as f:
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


if __name__ == '__main__':
    entry()
