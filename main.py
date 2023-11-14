"""
Лабораторная работа 1 по ЛОИС.
Вариант 2 (Импликация Гогена)
Выполнили Евегений Самохвал, Вячеслав Свяцкий и Иван Титлов.
Дата выполнения: 03.10.2023
"""

# A={(a, 0.5), (b, 0.6)}
# B={(c, 0.3), (d, 0.7)}
# C={(e, 0.1), (f, 0.8)}
# A~>B
import prettytable
import input_validator
LatinAlphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K",
                 "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

layers = []


def user_input_to_array(user_input: str):
    name_buffer = ""
    for sign in user_input:
        name_buffer += sign
        if sign == '=':
            break
    user_input = user_input.removeprefix(name_buffer + '{')
    name_buffer: str
    name_buffer = name_buffer.removesuffix('=')
    starting_array = user_input.strip(' ')
    starting_array = starting_array.removesuffix('}')
    divided_elements_array = []
    temp_string = ''
    for sign in starting_array:
        match sign:
            case '(': pass
            case ' ': pass
            case ',': temp_string += ','
            case ')':
                divided_elements_array.append(temp_string.removeprefix(','))
                temp_string = ''
            case _:
                temp_string += sign
    divided_elements_array = [pair.split(',')
                              for pair in divided_elements_array]
    return [name_buffer, [[pair[0], float(pair[1])] for pair in divided_elements_array]]


def get_set():
    while True:
        user_input_set_1 = input(
            'Введите нечёткое множество в формате A={(a, 0.5), (b, 0.6)} ...\n')
        if input_validator.input_check(user_input_set_1):
            processed_set_1 = user_input_to_array(user_input_set_1)
            break
        else:
            print("Неправильный ввод")
    print(processed_set_1)
    return processed_set_1

# Implication rule


def table_construction(starting_set_1, starting_set_2):
    result_table = [[] for pair in starting_set_1]
    for pair_x in range(len(starting_set_1)):
        for pair_y in range(len(starting_set_2)):
            result_table[pair_x].append(
                min(starting_set_2[pair_y][1]/starting_set_1[pair_x][1], 1))
    table_view = prettytable.PrettyTable()
    table_view.add_rows(result_table)
    layers[len(layers)-2].append(table_view)
    return result_table


def table_solver(x_y_table):
    processed_table = []
    for set_x_sign in range(len(x_y_table[0])):
        processed_table.append([])
        for table_sign in range(len(x_y_table[2][0])):
            processed_table[set_x_sign].append(
                x_y_table[0][set_x_sign][1] * x_y_table[2][set_x_sign][table_sign])
    table_view = prettytable.PrettyTable()
    table_view.add_rows(processed_table)
    layers[len(layers)-1].append(table_view)
    list_of_max = []
    for column in range(len(processed_table[0])):
        temp_container = []
        for row in range(len(processed_table)):
            temp_container.append(processed_table[row][column])
        list_of_max.append(max(temp_container))
    resulting_set = [[x_y_table[1][max_possibility][0], list_of_max[max_possibility]]
                     for max_possibility in range(len(list_of_max))]
    return resulting_set


def divide_name_set(starting_sets):
    list_of_names = []
    list_of_sets = dict()
    for pair in starting_sets:
        list_of_names.append(pair[0])
        list_of_sets[pair[0]] = pair[1]
    return list_of_sets, list_of_names


def rule_to_machine(user_rule):
    result = ""
    for sign in range(len(user_rule)):
        if user_rule[sign] == '~':
            result += "@"
        elif user_rule[sign] == '>':
            pass
        else:
            result += user_rule[sign]
    return result


def postfix_writing(poland_writing, list_of_names):
    result = []
    stack = []
    for sign in poland_writing:
        if list_of_names.count(sign):
            result.append(sign)
        elif sign == '@' or sign == '(':
            stack.insert(0, sign)
        elif sign == ')':
            while stack[0] != '(':
                result.append(stack.pop(0))
            stack.pop(0)
    while len(stack):
        result.append(stack.pop(0))
    return result


def get_rule(list_of_names):
    rule = (input("Введите правило в формате A~>B\n"))
    if not input_validator.input_rule_check(rule):
        print("Неправильный формат")
    else:
        machine_version = rule_to_machine(rule)
        return postfix_writing(machine_version, list_of_names)


def use_rule(postfix_rule, dict_of_sets, list_of_names):
    stack = []
    for sign in postfix_rule:
        if sign in list_of_names:
            stack.insert(0, dict_of_sets.get(sign))
        else:
            solution = table_solver(
                [stack[1], stack[0], table_construction(stack[1], stack[0])])
            stack.pop(0)
            stack.pop(0)
            stack.insert(0, solution)
    return stack[0]


def main():
    cycle = 'Да'
    number_of_sets = int(input("Введите количество посылок: "))
    try:
        starting_sets, list_of_names = divide_name_set(
            [get_set() for current_set in range(number_of_sets)])
    except ValueError:
        pass
    while cycle == 'Да':
        layers.append([])
        layers.append([])
        number_of_rules = int(input("\nВведите количество правил: "))
        for i in range(number_of_rules):
            try:
                rule = get_rule(list_of_names)
                result = use_rule(rule, starting_sets, list_of_names)
                for sign in LatinAlphabet:
                    if not (sign in list_of_names):
                        list_of_names.append(sign)
                        print(sign)
                        break
                starting_sets[list_of_names[-1]] = result
                print(result)
            except BaseException:
                continue
        cycle = input('Продолжить?\n')
    print(end=' ', sep=' ')
    counter = 0
    for layer in layers:
        print(f"Layer {counter}")
        for table in layer:
            print(table)
        print('\n')
        counter += 1


if __name__ == '__main__':
    main()
