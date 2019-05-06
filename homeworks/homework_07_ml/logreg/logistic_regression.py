#!/usr/bin/env python
# coding: utf-8


import numpy as np
import pandas as pd


class NotFittedError(Exception):
    def __init__(self):
        message = "Data is not fitted yet. Call 'fit' method before using this method."
        Exception.__init__(self, message)


class LogisticRegression:
    def __init__(self, lambda_coef=0.5, regularization=None, alpha=0.5, n_iters=100000):
        """
        LogReg for Binary case
        :param lambda_coef: constant coef for gradient descent step
        :param regulatization: regularizarion type ("L1" or "L2") or None
        :param alpha: regularizarion coefficent
        """
        if (regularization not in ("L1", "L2", None)):
            raise ValueError("regularization parameter must be 'L1', 'L2' or None.")

        self._lambda_coef = lambda_coef
        self._n_iters = n_iters
        self._reg = regularization
        self._alpha = alpha
        self._coef = None

    def fit(self, X_train, y_train, delta=0.00001, coef_rand_seed=222):
        """
        Fit model using gradient descent method
        :param X_train: training data
        :param y_train: target values for training data
        :return: None
        """
        if (X_train.shape[0] != y_train.shape[0]):
            raise ValueError(f"Found input variables with inconsistent numbers of"
                             f" samples: {X_train.shape[0]} != {len(y_train)}.")

        else:
            y_train = pd.get_dummies(y_train)

            zero_std = np.where(np.std(X_train, axis=0) == 0)[0]
            X_train = np.delete(X_train, zero_std, axis=1)

            X_train = np.hstack((np.ones((X_train.shape[0], 1)), X_train))
            # n - number of features, k - number of target classes
            m, n = X_train.shape
            k = y_train.shape[1]

            r = np.random.RandomState(coef_rand_seed)
            self._coef = r.normal(-1, 1, (n, k))

            y_hat = None
            prev = None
            reg_term = 0

            for _ in range(self._n_iters):
                if (prev is not None and np.all(np.absolute(self._coef - prev) < delta)):
                    break
                else:
                    prev = self._coef
                    denominator = np.sum(np.exp(X_train @ self._coef), axis=1)
                    y_hat = np.exp(X_train @ self._coef) / denominator[:, None]
                    if (self._reg == 'L2'):
                        reg_term = 2*np.sum(self._coef, axis=0)
                    elif (self._reg == 'L1'):
                        reg_term = (np.sum(self._coef > 0, axis=0) - np.sum(self._coef < 0, axis=0))

                    grad = X_train.T @ (y_hat - y_train) / m + self._alpha * reg_term / m
                    self._coef = self._coef - self._lambda_coef * grad
                    continue

            self._intercept = self._coef[0]
            self._coef = np.delete(self._coef, 0, axis=0)

            for i in zero_std:
                self._coef = np.insert(self._coef, i, np.zeros(k), axis=0)

    def predict(self, X_test):
        """
        Predict using model.
        :param X_test: test data for predict in
        :return: y_test: predicted values
        """
        if (self._coef is not None):
            denominator = np.sum(np.exp(X_test @ self._coef + self._intercept.reshape(1, -1)), axis=1)
            probs = np.exp(X_test @ self._coef + self._intercept.reshape(1, -1)) / denominator[:, None]
            pred = np.argmax(probs, axis=1)
            return pred
        else:
            raise NotFittedError

    def predict_proba(self, X_test):
        """
        Predict probability using model.
        :param X_test: test data for predict in
        :return: y_test: predicted probabilities
        """
        if (self._coef is not None):
            denominator = np.sum(np.exp(X_test @ self._coef + self._intercept.reshape(1, -1)), axis=1)
            probs = np.exp(X_test @ self._coef + self._intercept.reshape(1, -1)) / denominator[:, None]
            return probs
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
