#!/usr/bin/env python
# coding: utf-8

import collections


def groupping_anagramms(words):
    """
    Функция, которая группирует анаграммы.
    Возвращаем массив, где элементом является массив с анаграмами.
    Пример:  '''Аз есмь строка живу я мерой остр
                За семь морей ростка я вижу рост
                Я в мире сирота
                Я в Риме Ариост'''.split()
                ->
                [
                 ['Аз'], ['есмь', 'семь'],
                 ['строка', 'ростка'], ['живу', 'вижу'],
                 ['я', 'я'], ['мерой', 'морей'],
                 ['остр)'], ['За'], ['рост'], ['Я', 'Я'],
                 ['в', 'в'], ['мире'], ['сирота'],
                 ['Риме'], ['Ариост']
                ]
    :param words: list of words (words in str format)
    :return: list of lists of words
    """
    # TODO: реализовать функцию

    dict_of_anagramms = collections.OrderedDict()
    list_of_lists = []

    for word in words:
        dict_of_anagramms[''.join(sorted(word.lower()))] = []

    for word in words:
        sample = ''.join(sorted(word.lower()))
        if sample in dict_of_anagramms:
            dict_of_anagramms[sample].append(word)
        else:
            continue

    for value in dict_of_anagramms.values():
        list_of_lists.append(value)

    return list_of_lists
