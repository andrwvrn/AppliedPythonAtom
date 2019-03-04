#!/usr/bin/env python
# coding: utf-8

import copy


def calculate_determinant(list_of_lists):
    '''
    Метод, считающий детерминант входной матрицы,
    если это возможно, если невозможно, то возвращается
    None
    Гарантируется, что в матрице float
    :param list_of_lists: список списков - исходная матрица
    :return: значение определителя или None
    '''
    for row in list_of_lists:
        if (len(row) != len(list_of_lists) or len(list_of_lists) == 0):
            return None

        if (len(list_of_lists) == 1):
            return list_of_lists[0][0]

    def det_function(buff_list):
        det = 0

        if (len(buff_list) == 2):
            return buff_list[0][0]*buff_list[1][1] \
                - buff_list[0][1]*buff_list[1][0]
        else:
            row_1 = buff_list[0]

            for i in range(len(row_1)):
                next_list = buff_list[1::]
                for row in next_list:
                    row_copy = copy.deepcopy(row)
                    row_copy.pop(i)
                    next_list[next_list.index(row)] = row_copy
                det += ((-1)**i) * row_1[i] * det_function(next_list)
            return det

    return det_function(list_of_lists)
