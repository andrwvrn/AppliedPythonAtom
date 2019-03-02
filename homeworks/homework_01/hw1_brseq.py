#!/usr/bin/env python
# coding: utf-8


def is_bracket_correct(input_string):
    '''
    Метод проверяющий является ли поданная скобочная
     последовательность правильной (скобки открываются и закрываются)
     не пересекаются
    :param input_string: строка, содержащая 6 типов скобок (,),[,],{,}
    :return: True or False
    '''
    if (len(input_string) == 0):
        return True
    elif ('()' in input_string):
        return is_bracket_correct(input_string.replace('()', ''))
    elif ('[]' in input_string):
        return is_bracket_correct(input_string.replace('[]', ''))
    elif ('{}' in input_string):
        return is_bracket_correct(input_string.replace('{}', ''))
    else:
        return False
