#!/usr/bin/env python
# coding: utf-8

from multiprocessing import Process, Manager, Pool
import functools
import os


res_dict = Manager().dict()


def read_file(filename, pth):
    with open(pth + '/' + filename) as f:
        res_dict[filename] = len(f.read().split())


def word_count_inference(path_to_dir):
    '''
    Метод, считающий количество слов в каждом файле из директории
    и суммарное количество слов.
    Слово - все, что угодно через пробел, пустая строка "" словом не считается,
    пробельный символ " " словом не считается. Все остальное считается.
    Решение должно быть многопроцессным. Общение через очереди.
    :param path_to_dir: путь до директории с файлами
    :return: словарь, где ключ - имя файла, значение - число слов +
        специальный ключ "total" для суммы слов во всех файлах
    '''
    p = Pool()
    list_of_files = os.listdir(path_to_dir)
    p.map(functools.partial(read_file, pth=path_to_dir), list_of_files)

    p.close()
    p.join()
    res_dict['total'] = sum(res_dict.values())
    return res_dict
