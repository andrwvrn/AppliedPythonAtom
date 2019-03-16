#!/usr/bin/env python
# coding: utf-8


class HashMap:
    '''
    Давайте сделаем все объектненько,
     поэтому внутри хешмапы у нас будет Entry
    '''
    class Entry:
        def __init__(self, key, value):
            '''
            Сущность, которая хранит пары ключ-значение
            :param key: ключ
            :param value: значение
            '''
            self._key = key
            self._value = value

        def get_key(self):
            # TODO возвращаем ключ
            return self._key

        def get_value(self):
            # TODO возвращаем значение
            return self._value

        def __eq__(self, other):
            # TODO реализовать функцию сравнения
            return True if self.get_key() == other.get_key() else False

        def __repr__(self):
            return 'Entry:({},{})'.format(self._key, self._value)

    def __init__(self, bucket_num=64):
        '''
        Реализуем метод цепочек
        :param bucket_num: число бакетов при инициализации
        '''
        self._store = [None] * bucket_num
        self._size = 0

    def get(self, key, default_value=None):
        # TODO метод get, возвращающий значение,
        #  если оно присутствует, иначе default_value
        key_hash = self._get_hash(key)
        elem_index = self._get_index(key_hash)

        if (not self._store[elem_index]):
            return default_value
        else:
            list_of_elem = self._store[elem_index]
            for elem in list_of_elem:
                if (key == elem.get_key()):
                    return elem.get_value()
        return default_value

    def put(self, key, value):
        # TODO метод put, кладет значение по ключу,
        #  в случае, если ключ уже присутствует он его заменяет

        key_hash = self._get_hash(key)
        elem_index = self._get_index(key_hash)
        elem = self.Entry(key, value)

        if (not self._store[elem_index]):
            self._store[elem_index] = [elem]
            self._size += 1
        else:
            list_of_elem = self._store[elem_index]
            if (elem not in list_of_elem):
                list_of_elem.append(elem)
                self._size += 1
            else:
                for stored_elem in list_of_elem:
                    if elem == stored_elem:
                        stored_elem._value = elem._value
                        break
        if (self._size / len(self._store) > 0.75):
            self._resize()

    def __len__(self):
        # TODO Возвращает количество Entry в массиве
        return self._size

    def _get_hash(self, key):
        # TODO Вернуть хеш от ключа,
        #  по которому он кладется в бакет
        return hash(key)

    def _get_index(self, hash_value):
        # TODO По значению хеша вернуть индекс элемента в массиве
        return hash_value % len(self._store)

    def values(self):
        # TODO Должен возвращать итератор значений
        return (item[1] for item in self.items())

    def keys(self):
        # TODO Должен возвращать итератор ключей
        return (item[0] for item in self.items())

    def items(self):
        # TODO Должен возвращать итератор пар ключ и значение (tuples)
        list_of_items = []
        for _list in self._store:
            if (_list):
                for element in _list:
                    list_of_items.append((element.get_key(),
                                          element.get_value()))

        return (item for item in list_of_items)

    def _resize(self):
        # TODO Время от времени нужно ресайзить нашу хешмапу
        items = self.items()
        self._size = 0
        self._store = len(self._store) * 2 * [None]
        for item in items:
            self.put(*item)

    def __str__(self):
        # TODO Метод выводит "buckets: {}, items: {}"
        return "buckets: {}, items: {}".format(self._store, list(self.items()))

    def __contains__(self, item):
        # TODO Метод проверяющий есть ли объект (через in)
        if (item in self.keys()):
            return True
        else:
            False
