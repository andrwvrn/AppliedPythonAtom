#!/usr/bin/env python
# coding: utf-8


import numpy as np


class CSRMatrix:
    """
    CSR (2D) matrix.
    Here you can read how CSR sparse matrix works: https://en.wikipedia.org/wiki/Sparse_matrix
    """
    def __init__(self, init_matrix_representation):
        """
        :param init_matrix_representation: can be usual dense matrix
        or
        (row_ind, col, data) tuple with np.arrays,
            where data, row_ind and col_ind satisfy the relationship:
            a[row_ind[k], col_ind[k]] = data[k]
        """
        if isinstance(init_matrix_representation, tuple) and len(init_matrix_representation) == 3:
            length = len(init_matrix_representation[0])

            if any(len(l) != length for l in init_matrix_representation[1:]):
                raise ValueError('row, column, and data arrays must all be the same length')

            if any(i < 0 for i in init_matrix_representation[0]):
                raise ValueError('row indices must be positive')

            if any(j < 0 for j in init_matrix_representation[1]):
                raise ValueError('column indices must be positive')

            else:
                row_indices = np.array(init_matrix_representation[0])
                col_indices = np.array(init_matrix_representation[1])
                crude_data = np.array(init_matrix_representation[2])
                self._shape = (np.max(row_indices)+1, np.max(col_indices)+1)
                self._row_ind = np.zeros(self._shape[0]+1).astype(int)
                self._col_ind = np.array([])
                self._data = np.array([])

# если в списке значений передали нули, избавляемся от них
                nonzeros = (crude_data != 0)
                row_indices = row_indices[nonzeros].astype(int)
                col_indices = col_indices[nonzeros].astype(int)
                crude_data = crude_data[nonzeros]

                for l in list(zip(row_indices, col_indices, crude_data)):
                    self.set_item(*l)

        elif isinstance(init_matrix_representation, np.ndarray):
            nonzeros = (init_matrix_representation != 0)
            row_indices = np.where(nonzeros)[0]
            self._col_ind = np.where(nonzeros)[1].astype(int)
            self._shape = init_matrix_representation.shape
            self._row_ind = np.zeros(self._shape[0]+1).astype(int)
            for i in range(self._shape[0]):
                self._row_ind[i+1] = self._row_ind[i] + np.count_nonzero(row_indices == i)
            self._data = init_matrix_representation[nonzeros].flatten()

        else:
            raise ValueError

    def get_item(self, i, j):
        """
        Return value in i-th row and j-th column.
        Be careful, i and j may have invalid values (-1 / bigger that matrix size / etc.).
        """
        if (i < 0 or j < 0):
            raise IndexError('only positive indices are allowed')
        elif (i > self._shape[0]):
            raise IndexError(f'row index {i} is out of bounds for matrix with size '
                             '{self._shape[0]}x{self._shape[1]}')
        elif (j > self._shape[1]):
            raise IndexError(f'col index {j} is out of bounds for matrix with size '
                             '{self._shape[0]}x{self._shape[1]}')
        elif (not isinstance(i, (int, np.int64)) or not isinstance(j, (int, np.int64))):
            raise IndexError('indices must be integers')
        else:
            how_much_before = self._row_ind[i]
            how_much_in = self._row_ind[i+1]
            if (how_much_in - how_much_before > 0):
                req_ind = np.where(self._col_ind[how_much_before:how_much_in] == j)
                if (req_ind[0].size > 0):
                    req_ind = req_ind[0][0] + how_much_before
                    return self._data[req_ind]
                else:
                    return 0
            else:
                return 0

    def set_item(self, i, j, value):
        """
        Set the value to i-th row and j-th column.
        Be careful, i and j may have invalid values (-1 / bigger that matrix size / etc.).
        """
        if (i < 0 or j < 0):
            raise IndexError('only positive indices are allowed')
        elif (i > self._shape[0]):
            raise IndexError(f'row index {i} is out of bounds for matrix with size '
                             '{self._shape[0]}x{self._shape[1]}')
        elif (j > self._shape[1]):
            raise IndexError(f'col index {j} is out of bounds for matrix with size '
                             '{self._shape[0]}x{self._shape[1]}')
        elif (not isinstance(i, (int, np.int64)) or not isinstance(j, (int, np.int64))):
            raise IndexError(f'indices must be integers')
        else:
            if (value != 0):
                how_much_before = self._row_ind[i]
                how_much_in = self._row_ind[i+1]

# если в строке i что-то есть, кроме нулей
                if (how_much_in - how_much_before > 0):
                    req_ind = np.where(self._col_ind[how_much_before:how_much_in] == j)

# если в столбце j строки i есть что-то, не равное 0, заменяем существующее значение в нем
                    if (req_ind[0].size > 0):
                        req_ind = req_ind[0][0] + how_much_before
                        self._data[req_ind] = value

# иначе записываем value в столбец j строки i, где пока стоит 0
                    else:
                        count = 0
                        for ind in self._col_ind[how_much_before:how_much_in]:

                            if (j < ind):     # при этом сохраняем порядок столбцов
                                ins_ind = how_much_before + count
                                self._col_ind = np.insert(self._col_ind, ins_ind, j)
                                self._data = np.insert(self._data, ins_ind, value)
                                for k in range(i+1, len(self._row_ind)):
                                    self._row_ind[k] += 1
                                break
                            else:
                                count += 1
                                continue

# если j больше номера любого столбца в строке i, ставим его в конец
                        if (count == (how_much_in - how_much_before)):
                            ins_ind = how_much_before + count
                            self._col_ind = np.insert(self._col_ind, ins_ind, j)
                            self._data = np.insert(self._data, ins_ind, value)
                            for k in range(i+1, len(self._row_ind)):
                                self._row_ind[k] += 1

# если в строке i нет ненулевых значений
                else:
                    ins_ind = how_much_before
                    self._col_ind = np.insert(self._col_ind, ins_ind, j)
                    self._data = np.insert(self._data, ins_ind, value)
                    for k in range(i+1, len(self._row_ind)):
                        self._row_ind[k] += 1

    def to_dense(self):
        """
        Return dense representation of matrix (2D np.array).
        """
        dense = np.zeros((self._shape[0], self._shape[1]))
        for i in range(self._shape[0]):
            for j in range(self._shape[1]):
                dense[i, j] += self.get_item(i, j)
        return dense
