#!/usr/bin/env python
# coding: utf-8


def invert_dict(source_dict):
    '''
    Функция которая разворачивает словарь, т.е.
    каждому значению ставит в соответствие ключ.
    :param source_dict: dict
    :return: new_dict: dict
    '''
    if (type(source_dict) == dict):

        new_dict = {}

        def unpack(values):
            list_of_values = []

            if (type(values) not in [list, tuple, set]):
                return [values]

            else:
                for value in values:
                    list_of_values += unpack(value)
            return list_of_values

        for (key, values) in source_dict.items():
            list_of_values = unpack(values)
            source_dict[key] = list_of_values

        for (key, values) in source_dict.items():
            for value in values:

                if (value not in new_dict.keys()):
                    new_dict[value] = key
                else:
                    key_list = []

                    if (type(new_dict[value]) != list):
                        key_list.append(new_dict[value])
                    else:
                        key_list += new_dict[value]

                    key_list.append(key)
                    new_dict[value] = key_list

        return new_dict
