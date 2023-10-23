import re

def input_check(input_string: str):
    if not input_string[0].isupper() or input_string[1] != ')':
        return False
    elements = input_string[1:].split(',')
    for element in elements:
        parts = element.strip().split('|')
        if len(parts) != 2:
            return False
        key, value = parts
        if not key.isalpha() or key.isupper():
            return False
        try:
            float_value = float(value)
            if not (0.0 <= float_value <= 1.0):
                return False
        except ValueError:
            return False
    return True

def input_rule_check(input_rule: str):
    pass

def input_check_with_regex(input_string: str):
    right_str_form = re.compile(r"^(?:[a-z]\|0\.\d+(?:,\s)?)+$")
    return re.match(right_str_form, input_string)
