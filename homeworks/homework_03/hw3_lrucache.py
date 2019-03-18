#!/usr/bin/env python
# coding: utf-8

import collections
import time


def LRUCacheDecorator(maxsize=None, ttl=None):

    class LRUCacheDecClass:

        def __init__(self, func):
            '''
            :param maxsize: максимальный размер кеша
            :param ttl: время в млсек, через которое кеш
                        должен исчезнуть
            '''
            # TODO инициализация декоратора
            #  https://www.geeksforgeeks.org/class-as-decorator-in-python/
            self._size = 0
            self._ttl = ttl
            self._cache = collections.OrderedDict()
            self._func = func
            self._t_end = None

        def __call__(self, *args, **kwargs):
            # TODO вызов функции
            if (self._ttl and self._t_end and
                    time.time() - self._t_end >= self._ttl):
                self._cache.clear()
                self._size = 0

            if (maxsize <= 0):
                return self._func(*args, **kwargs)

            key = args
            kw = None
            if (kwargs):
                kw = sorted(kwargs.items())
                key = args, *kw

            if (not self._cache.get(key)):
                if (self._size != maxsize):
                    self._cache[key] = self._func(*args, **kwargs)
                    self._size += 1
                else:
                    self._cache.popitem(last=False)
                    self._cache[key] = self._func(*args, **kwargs)

                self._t_end = time.time()
                return self._cache[key]

            else:
                self._cache[key] = self._cache.pop(key)
                self._t_end = time.time()
                return self._cache[key]

    return LRUCacheDecClass
