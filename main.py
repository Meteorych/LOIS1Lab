"""
Лабораторная работа 1 по ЛОИС.
Вариант 2 (Импликация Гогена)
Выполнили Евегений Самохвал, Вячеслав Свяцкий и Иван Титлов.
Дата выполнения: 03.10.2023
"""

import input_validator

def user_input_to_array(user_input: str):
    name_buffer = ""
    for sign in user_input:
        name_buffer+=sign
        if sign == ')':
            break
    user_input = user_input.removeprefix(name_buffer + ')')
    starting_array = user_input.split(', ')
    divided_elements_array = [pair.split('|') for pair in starting_array]
    return [name_buffer, [[pair[0], float(pair[1])] for pair in divided_elements_array]]


def get_set():
    user_input_set_1 = input('Введите нечёткое множество в формате A)a|0.5, b|0.4 ...\n')
    while True:
        if input_validator.input_check(user_input_set_1):
            processed_set_1 = user_input_to_array(user_input_set_1)
            break
        else:
            user_input_set_1 = input("Неправильный формат нечёткого множества")
    print(processed_set_1)
    return processed_set_1

# Implication rule
def table_construction(starting_set_1, starting_set_2):
    result_table = [[] for pair in starting_set_1]
    for pair_x in range(len(starting_set_1)):
        for pair_y in range(len(starting_set_2)) :
            if starting_set_1[pair_x][1] < starting_set_2[pair_y][1]:
                result_table[pair_x].append(1)
            else:
                result_table[pair_x].append(starting_set_2[pair_y][1])
    return result_table


def table_solver(x_y_table):
    processed_table = []
    for set_x_sign in range(len(x_y_table[0])):
        processed_table.append([])
        for table_sign in range(len(x_y_table[2][0])):
            processed_table[set_x_sign].append(x_y_table[0][set_x_sign][1] * x_y_table[2][set_x_sign][table_sign])
    resulting_set = [[x_y_table[1][max_possibility][0],
                      max(processed_table[max_possibility])] for max_possibility in range(len(processed_table))]
    return resulting_set

def divide_name_set(starting_sets):
    list_of_names = []
    list_of_sets = []
    for pair in starting_sets:
        list_of_names.append(pair[0])
        list_of_sets.append(pair[1])
    return list_of_sets, list_of_names


def get_rule():
    user_input = input("Введите правило в формате (1~>2)")



def main():
    cycle = 'Да'
    while cycle == 'Да':
        number_of_sets = int(input("Введите количество посылок: \n"))
        starting_sets, list_of_names = divide_name_set([get_set() for current_set in range(number_of_sets)])
        all_tables = []
        for set_x in starting_sets:
            for set_y in starting_sets:
                if set_x != set_y:
                    temp_sets_array = [set_x, set_y, table_construction(set_x, set_y)]
                    if all_tables.count(temp_sets_array) == 0:
                        all_tables.append(temp_sets_array)
        for table in all_tables:
            print("Вывод: \n", table_solver(table))
        cycle = input('Продолжить?\n')


if __name__ == '__main__':
    main()

