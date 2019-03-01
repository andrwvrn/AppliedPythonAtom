#!/usr/bin/env python
# coding: utf-8


def calculator(x, y, operator):
    '''
    Простенький калькулятор в прямом смысле. Работает c числами
    :param x: первый агрумент
    :param y: второй аргумент
    :param operator: 4 оператора: plus, minus, mult, divide
    :return: результат операции или None, если операция не выполнима
    '''
    if (y == 0) and (operator == 'divide'):
        return None
    elif (type(x) not in [int, float]) or (type(y) not in [int, float]):
        return None
    elif (operator == 'plus'):
        return x + y
    elif (operator == 'minus'):
        return x - y
    elif (operator == 'mult'):
        return x * y
    elif (operator == 'divide'):
        return x / y
