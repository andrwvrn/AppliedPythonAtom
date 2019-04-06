#!/usr/bin/env python
# coding: utf-8

import numpy as np


def simplex_method(a, b, c):
    """
    Почитать про симплекс метод простым языком:
    * https://  https://ru.wikibooks.org/wiki/Симплекс-метод._Простое_объяснение
    Реализацию алгоритма взять тут:
    * https://youtu.be/gRgsT9BB5-8 (это ссылка на 1-ое из 5 видео).

    Используем numpy и, в целом, векторные операции.

    a * x.T <= b
    c * x.T -> max
    :param a: np.array, shape=(n, m)
    :param b: np.array, shape=(n, 1)
    :param c: np.array, shape=(1, m)
    :return x: np.array, shape=(1, m)
    """

    new_a = np.vstack((a, -c))
    simplex_tab = np.hstack((new_a, np.eye(b.shape[0]+1), np.append(b, 0)[:, None]))

    res = np.zeros((c.shape[0]))
    while np.any(simplex_tab[-1] < 0):
        ind_col = np.argmin(simplex_tab[-1])

        with np.errstate(divide='ignore'):
            ind_row = np.argmin(np.divide(simplex_tab[:-1, -1],
                                          simplex_tab[:-1, ind_col]))

        simplex_tab[ind_row] = simplex_tab[ind_row]/simplex_tab[ind_row, ind_col]
        new_tab = simplex_tab - simplex_tab[ind_row]*simplex_tab[:, ind_col, None]
        new_tab[ind_row] = simplex_tab[ind_row]
        simplex_tab = new_tab

    x_ind = np.where(simplex_tab[:-1, :c.shape[0]] == 1)
    res[x_ind[1]] = simplex_tab[:-1, -1][x_ind[0]]

    return res
