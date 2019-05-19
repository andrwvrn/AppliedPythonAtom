#!/usr/bin/env python
# coding: utf-8

import numpy as np
import numpy.ma as ma


class NotFittedError(Exception):
    def __init__(self):
        message = "Data is not fitted yet. Call 'fit' method before using this method."
        Exception.__init__(self, message)


class LinearRegression:
    def __init__(self, lambda_coef=1.0, regularization=None, alpha=0.5):
        """
        :param lambda_coef: constant coef for gradient descent step
        :param regulatization: regularizarion type ("L1" or "L2") or None
        :param alpha: regularizarion coefficent
        """
        self._lambda_coef = lambda_coef

        if (regularization not in ("L1", "L2", None)):
            raise ValueError("regularization parameter must be 'L1', 'L2' or None.")

        self._reg = regularization
        self._alpha = alpha
        self._coef = None

    def fit(self, X_train, y_train, n_iters=100000, eps=0.00001, seed = 22):
        """
        Fit model using gradient descent method
        :param X_train: training data
        :param y_train: target values for training data
        :return: None
        """
        if (y_train.ndim == 1):
            y_train = y_train[:, None]

        if (X_train.shape[0] != y_train.shape[0]):
            raise ValueError(f"Found input variables with inconsistent numbers of"
                             f" samples: {X_train.shape[0]} != {len(y_train)}.")
        else:
            # избавимся от признаков с нулевым разбросом, так как они неинформативны
            zero_std = np.where(np.std(X_train, axis=0) == 0)[0]
            X_train = np.delete(X_train, zero_std, axis=1)
            X_train = (X_train - np.mean(X_train, axis=0)) / np.std(X_train, axis=0)

            # добавим единичный признак, вес при котором будет отвечать за сдвижку вдоль оси
            X_train = np.hstack((np.ones((X_train.shape[0], 1)), X_train))
            m, n = X_train.shape

            # нагенерим коэффициенты
            r = np.random.RandomState(seed)
            self._coef = r.normal(-1, 1, (n, 1))

            prev = None
            reg_term = 0

            for _ in range(n_iters):
                if (prev is not None and np.all(np.absolute(self._coef - prev) < eps)):
                    break
                else:
                    prev = self._coef
                    loss = (X_train @ self._coef) - y_train
                    if (self._reg == 'L2'):
                        reg_term = 2*np.sum(self._coef, axis=1)
                        reg_term = reg_term[:, None]
                    elif (self._reg == 'L1'):
                        reg_term = np.sum(self._coef > 0, axis=1) - np.sum(self._coef < 0, axis=1)
                        reg_term = reg_term[:, None]
                    grad = (X_train.T @ loss) / m + self._alpha * reg_term
                    self._coef = self._coef - self._lambda_coef * grad
                    continue

            self._intercept = self._coef[0]
            self._coef = np.delete(self._coef, 0)

            self._coef = self._coef.flatten()
            for i in zero_std:
                self._coef = np.insert(self._coef, i, 0)

    def predict(self, X_test):
        """
        Predict using model.
        :param X_test: test data for predict in
        :return: y_test: predicted values
        """
        if (self._coef is not None):
            return (X_test @ self._coef[:None] + self._intercept)
        else:
            raise NotFittedError

    def get_weights(self):
        """
        Get weights from fitted linear model
        :return: weights array
        """
        if (self._coef is not None):
            return self._coef
        else:
            raise NotFittedError
