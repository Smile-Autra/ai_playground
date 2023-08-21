from copilot.llm.messages import ChatMessages


def count_token(messages: ChatMessages) -> float:
    # Number of tokens is always 4/3 of number of words
    return len(messages.text_format.split(' ')) * 4 / 3
