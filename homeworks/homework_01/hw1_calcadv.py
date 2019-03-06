#!/usr/bin/env python
# coding: utf-8


def calc(x, y, operator):

    if (y == '0') and (operator == '/'):
        return None
    elif (operator == '+'):
        return float(x) + float(y)
    elif (operator == '-'):
        return float(x) - float(y)
    elif (operator == '*'):
        return float(x) * float(y)
    elif (operator == '/'):
        return float(x) / float(y)


def delete_quotes(tok_list):

    without_quotes = []
    for token in tok_list:
        if (token != ''):
            without_quotes.append(token)
        else:
            continue

    return without_quotes


def advanced_calculator(input_string):
    '''
    Калькулятор на основе обратной польской записи.
    Разрешенные операции: открытая скобка, закрытая скобка,
     плюс, минус, умножить, делить
    :param input_string: строка, содержащая выражение
    :return: результат выполнение операции, если строка валидная - иначе None
    '''
    acc_dict = {'*': 2, '/': 2, '+': 1, '-': 1, '(': 0, ')': 0,
                ' ': 0, '.': 0, '\t': 0}

    oper_dict = {'*': 2, '/': 2, '+': 1, '-': 1, '(': 0, ')': 0}

    num_list = [str(i) for i in range(10)]

    for token in input_string:
        if (token not in acc_dict and token not in num_list):
            return None
        elif (token in oper_dict):
            input_string = input_string.replace(token, ' ' + token + ' ')

    token_list = input_string.split(' ')
    token_list = delete_quotes(token_list)
    if not token_list:
        return None

    for i in range(len(token_list)):
        if (token_list[i] not in acc_dict and i != (len(token_list)-1)):
            if token_list[i+1] not in acc_dict:
                return None
        else:
            continue

    token_string = ''.join(token_list)

    while True:
        if ('++' in token_string):
            token_string = token_string.replace('++', '+')
        elif ('--' in token_string):
            token_string = token_string.replace('--', '+')
        elif ('+-' in token_string):
            token_string = token_string.replace('+-', '-')
        elif ('-+' in token_string):
            token_string = token_string.replace('-+', '-')
        elif ('*-' in token_string):
            token_string = token_string.replace('*-', '*(0-1)*')
        elif ('*+' in token_string):
            token_string = token_string.replace('*+', '*')
        elif ('/-' in token_string):
            token_string = token_string.replace('/-', '*(0-1)/')
        elif ('/+' in token_string):
            token_string = token_string.replace('/+', '/')
        elif ('(-' in token_string):
            token_string = token_string.replace('(-', '(0-')
        elif ('(+' in token_string):
            token_string = token_string.replace('(+', '(0+')
        elif ('\\t' in token_string):
            token_string = token_string.replace('\\t', ' ')
        else:
            break

    if (token_string[0] in ('+', '-')):
        token_string = '0' + token_string

    for token in token_string:
        if (token in oper_dict):
            token_string = token_string.replace(token, ' ' + token + ' ')

    token_list = token_string.split(' ')
    token_list = delete_quotes(token_list)

    for token in token_list:
        point_count = 0

        for symbol in token:
            if (symbol == '.'):
                point_count += 1

        if (point_count > 1):
            return None

    brackets_count = 0
    for token in token_list:
        if (token == '('):
            brackets_count += 1

        elif (token == ')'):
            brackets_count -= 1

    if (brackets_count != 0):
        return None

    oper_stack = []
    rpn_stack = []

    for token in token_list:
        if (token == '('):
            oper_stack.append(token)

        elif (token == ')' and len(oper_stack) < 2):
            return None

        elif (token == ')' and '(' not in oper_stack):
            return None

        elif (token == ')'):
            for i in range(len(oper_stack)-1, -1, -1):
                if (oper_stack[i] != '('):
                    rpn_stack.append(oper_stack.pop(i))
                else:
                    oper_stack.pop(i)
                    break

        elif (token not in oper_dict):
            rpn_stack.append(token)

        elif (token in oper_dict and oper_stack):
            while oper_stack:
                if (oper_dict.get(token) <= oper_dict.get(oper_stack[-1])):
                    rpn_stack.append(oper_stack.pop())
                else:
                    break
            oper_stack.append(token)

        elif (token in oper_dict):
            oper_stack.append(token)

        else:
            return None

    rpn_stack = rpn_stack + oper_stack[::-1]

    if (len(rpn_stack) == 1 and rpn_stack[0] not in oper_dict):
        return float(rpn_stack[0])

    elif (len(rpn_stack) < 3):
        return None

    res = []

    for token in rpn_stack:

        if (token not in oper_dict):
            res.append(token)

        elif (token in oper_dict and len(res) >= 2):
            operator = token
            right_op, left_op = res.pop(), res.pop()

            if (right_op in oper_dict or left_op in oper_dict):
                return None
            res.append(calc(left_op, right_op, operator))

        else:
            return None

    return res[0] if (len(res) == 1) else None
