import re

def input_check(input_string: str):
    if not input_string[0].isupper() or input_string[1] != ')':
        return False
    elements = input_string[2:].split(',')
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

def input_rule_check(input_str):
    stack = []
    for char in input_str:
        if char == '(':
            stack.append(char)
        elif char == ')':
            if not stack:
                return False
            stack.pop()
    if stack:
        return False
    input_str = input_str.replace(" ", "")
    if "(" not in input_str and ")" not in input_str:
        return validate_expression(input_str)
    index = input_str.find("~>")
    if index == -1:
        return False  # Missing "~>" operator
    return (
            validate_expression(input_str[:index]) and
            validate_expression(input_str[index + 2:])
    )

def validate_expression(expr):
    if len(expr) == 1:
        return expr.isalpha()
    if expr.count("~>") != 1:
        return False  # There should be exactly one "~>" operator
    left, right = expr.split("~>")
    if not left or not right:
        return False  # Left and right expressions should not be empty
    if left[0] == '(' and left[-1] == ')':
        # This part is in the format "(X~>Y)", so validate its content
        if not input_rule_check(left[1:-1]):
            return False
    if right[0] == '(' and right[-1] == ')':
        # This part is in the format "(X~>Y)", so validate its content
        if not input_rule_check(right[1:-1]):
            return False
    return True

def input_check_with_regex(input_string: str):
    right_str_form = re.compile(r"^(?:[a-z]\|0\.\d+(?:,\s)?)+$")
    return re.match(right_str_form, input_string)
