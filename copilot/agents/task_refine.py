import json
import logging

from copilot.llm import ChatOpenAI, ChatMessages
from copilot.prompt.prompt_generator import generate_enhancer_prompt


def refine_task_description(llm: ChatOpenAI,
                            task_description: str,
                            model='gpt-3.5-turbo') -> str:
    messages = ChatMessages()
    messages.add_system_message(generate_enhancer_prompt())
    messages.add_user_message(task_description)
    for _ in range(3):
        reply = llm.chat(messages, model=model, max_tokens=500)
        try:
            reply_json = json.loads(reply)
            objective = reply_json['objective']
            best_practices = reply_json['best_practices']
            guidelines = reply_json['guidelines']
            refined_description = f'Objective: {objective}\n\nBest practices:\n{best_practices}\n\nGuidelines:\n'
            for guideline in guidelines:
                refined_description += f'- {guideline}\n'
            return refined_description
        except json.JSONDecodeError as e:
            error_msg = f'Cannot decode reply using json.loads, error\n:{str(e)}'
        except KeyError as e:
            error_msg = f'Parse result error from reply, error:\n{str(e)}'
        messages.add_user_message(error_msg)
        logging.error(error_msg)
    raise RuntimeError('Cannot refine task description by LLM in 3 iterations')
