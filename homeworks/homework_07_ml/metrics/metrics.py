#!/usr/bin/env python
# coding: utf-8


import numpy as np


def logloss(y_true, y_pred, eps=1e-15):
    """
    logloss
    :param y_true: vector of truth (correct) class values
    :param y_hat: vector of estimated probabilities
    :return: loss
    """
    y_pred = np.clip(y_pred, eps, 1-eps)
    loss = -np.sum(y_true * np.log(y_pred) + (1 - y_true) * np.log(1 - y_pred)) / y_true.shape[0]
    return loss


def accuracy(y_true, y_pred):
    """
    Accuracy
    :param y_true: vector of truth (correct) class values
    :param y_hat: vector of estimated class values
    :return: loss
    """
    return np.sum(y_pred == y_true) / len(y_true)


def presicion(y_true, y_pred):
    """
    presicion
    :param y_true: vector of truth (correct) class values
    :param y_hat: vector of estimated class values
    :return: loss
    """
    true_positive = np.sum(y_pred[y_true == 1])
    return true_positive / np.sum(y_pred)


def recall(y_true, y_pred):
    """
    presicion
    :param y_true: vector of truth (correct) class values
    :param y_hat: vector of estimated class values
    :return: loss
    """
    true_positive = np.sum(y_pred[y_true == 1])
    return true_positive / np.sum(y_true)


def roc_auc(y_true, y_pred):
    """
    roc_auc
    :param y_true: vector of truth (correct) target values
    :param y_hat: vector of estimated probabilities
    :return: loss
    """
    sorted_pred_idx = np.argsort(y_pred)[::-1]
    y_true_sort = np.zeros(len(y_true)).astype(float)
    y_pred_sort = np.zeros(len(y_pred)).astype(float)
    for (i, j) in enumerate(sorted_pred_idx):
        y_true_sort[i] = y_true[j]
        y_pred_sort[i] = y_pred[j]
    tpr = 0
    fpr = 0
    auc = 0
    count_ones = 0
    count = 0

    i = 0
    while i < len(y_true_sort):
        count_ones = 0
        count = 0

        for j in range(i, len(y_true_sort)):
            if y_pred_sort[j] == y_pred_sort[i]:
                count_ones += y_true_sort[j]
                count += 1

        if count != 1:
            auc += tpr * (count - count_ones)
            tpr += count_ones
            fpr += count - count_ones
            auc += (count_ones * (count - count_ones)) / 2
            i = i + count
            continue

        if y_true_sort[i] == 1:
            tpr += 1

        elif y_true_sort[i] == 0:
            fpr += 1
            auc += tpr

        i += 1
    return auc / (fpr * tpr)
