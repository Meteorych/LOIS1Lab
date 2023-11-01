import re

def input_check(input_string: str):
    # Remove leading and trailing whitespace
    input_string = input_string.strip()

    # Check if the input string starts with an uppercase letter followed by "="
    if not (input_string[0].isupper() and input_string[1] == "="):
        return False

    # Extract the content inside the curly braces
    content = input_string[input_string.index("{") + 1:input_string.index("}")]

    # Split the content into key-value pairs using ","
    pairs = split_by_comma(content)

    for pair in pairs:
        # Split each pair into key and value using "(" and ")"
        key_value = pair.strip().strip("()").split(",")

        if len(key_value) != 2:
            return False

        key, value = key_value[0].strip(), key_value[1].strip()

        # Check if the key is a lowercase letter and the value is a valid float between 0 and 1
        if not (len(key) == 1 and key.islower() and (value.isdigit() or
                                                     (0 <= float(value) <= 1))):
            return False

    # If all checks passed, the input is valid
    return True

def input_rule_check(expr):
    if len(expr) == 1:
        return expr.isalpha()
    if expr.count("~>") != 1:
        return False  # There should be exactly one "~>" operator
    left, right = expr.split("~>")
    if not left or not right:
        return False  # Left and right expressions should not be empty
    if len(left) != 1 and len(right) != 1:
        return False
    if not left.isupper() or not right.isupper():
        return False
    return True

def split_by_comma(input_str):
    parts = []
    current_part = ""
    parentheses_count = 0
    for char in input_str:
        if char == ',' and parentheses_count == 0:
            parts.append(current_part.strip())
            current_part = ""
        else:
            current_part += char
            if char == '(':
                parentheses_count += 1
            elif char == ')':
                parentheses_count -= 1
    if current_part:
        parts.append(current_part.strip())
    return parts

def input_check_with_regex(input_string: str):
    right_str_form = re.compile(r"^(?:[a-z]\|0\.\d+(?:,\s)?)+$")
    return re.match(right_str_form, input_string)
