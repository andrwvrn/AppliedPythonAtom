#!/usr/bin/env python
# coding: utf-8
import numpy as np


class KNNRegressor:
    """
    Построим регрессию с помощью KNN. Классификацию писали на паре
    """

    def __init__(self, n=5):
        '''
        Конструктор
        :param n: число ближайших соседей, которые используются
        '''
        self._n = n

    def fit(self, X, y):
        '''
        :param X: обучающая выборка, матрица размерности (num_obj, num_features)
        :param y: целевая переменная, матрица размерности (num_obj, 1)
        :return: None
        '''
        self._X_train = X
        self._y_train = y

    def predict(self, X):
        '''
        :param X: выборка, на которой хотим строить предсказания (num_test_obj, num_features)
        :return: вектор предсказаний, матрица размерности (num_test_obj, 1)
        '''

        y = []
        assert len(X.shape) == 2
        for t in X:
            # Посчитаем расстояние от всех элементов в тренировочной выборке
            # до текущего примера -> результат - вектор размерности трейна
            d = np.sqrt(np.sum((self._X_train - t)**2, axis=1))
            # Возьмем индексы n элементов, расстояние до которых минимально
            # результат -> вектор из n элементов
            idx = np.argsort(d)[:self._n]
            y_nearest = self._y_train[idx]
            prediction = np.mean(y_nearest)
            y.append(prediction)
        return y
