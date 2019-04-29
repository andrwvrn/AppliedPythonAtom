#!/usr/bin/env python
# coding: utf-8

import numpy as np


class NotFittedError(Exception):
    def __init__(self):
        message = "Data is not fitted yet. Call 'fit' method before using this method."
        Exception.__init__(self, message)


class DecisionStumpRegressor:
    '''
    Класс, реализующий решающий пень (дерево глубиной 1)
    для регрессии. Ошибку считаем в смысле MSE
    '''

    def __init__(self):
        '''
        Мы должны создать поля, чтобы сохранять наш порог th и ответы для
        x <= th и x > th
        '''
        self._th = np.array([])
        self._pred = np.array([])
        self._mse = np.array([])

    def fit(self, X, y):
        '''
        метод, на котором мы должны подбирать коэффициенты th, y1, y2
        :param X: массив размера (1, num_objects)
        :param y: целевая переменная (1, num_objects)
        :return: None
        '''
        X_train = X.flatten()
        y_train = y.flatten()

        for x in X_train:
            left_child_ = y_train[X_train <= x]
            right_child_ = y_train[X_train > x]

            mse_left = np.sum((left_child_ - np.mean(left_child_))**2)
            if len(right_child_ > 0):
                mse_right = np.sum((right_child_ - np.mean(right_child_))**2)
            else:
                mse_right = 0

            mse_ = mse_left + mse_right
            self._th = np.append(self._th, x)
            self._mse = np.append(self._mse, mse_)

        self._best_th = self._th[np.argmin(self._mse)]
        self._pred = np.append(self._pred, np.mean(y_train[X_train <= self._best_th]))
        self._pred = np.append(self._pred, np.mean(y_train[X_train > self._best_th]))

    def predict(self, X):
        '''
        метод, который позволяет делать предсказания для новых объектов
        :param X: массив размера (1, num_objects)
        :return: массив, размера (1, num_objects)
        '''
        if len(self._mse > 0):
            y_pred = np.zeros(X.shape)
            y_pred[X <= self._best_th] = self._pred[0]
            y_pred[X > self._best_th] = self._pred[1]

            return y_pred.flatten()

        else:
            raise NotFittedError
