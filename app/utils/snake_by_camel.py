import re

def snake_to_camel(snake_str):
    leading_underscores = ''
    if snake_str.startswith('_'):
        leading_underscores = re.match(r'^_+', snake_str).group()
        snake_str = snake_str[len(leading_underscores):]
    
    components = snake_str.split('_')
    camel_case_str = components[0] + ''.join(x.title() for x in components[1:])
    
    return leading_underscores + camel_case_str

def convert_keys_to_camel_case(data):
    if isinstance(data, list):
        return [convert_keys_to_camel_case(item) for item in data]
    elif isinstance(data, dict):
        new_dict = {}
        for key, value in data.items():
            new_key = snake_to_camel(key) if '_' in key else key
            new_dict[new_key] = convert_keys_to_camel_case(value) if isinstance(value, (dict, list)) else value
        return new_dict
    else:
        return data