def pretty_print(content_json: dict):
    # pretty print recursively json content
    for key, value in content_json.items():
        if isinstance(value, dict):
            print(f'{key}:')
            pretty_print(value)
        else:
            if '\n' in value or len(value) > 100:
                print(f'{key}:\n{value}')
            else:
                print(f'{key}: {value}')
