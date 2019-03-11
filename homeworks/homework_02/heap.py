#!/usr/bin/env python
# coding: utf-8


class Heap():

    def __init__(self, array):
        self._heap = array[:]
        self.build_heap()

    def add(self, elem_with_priority):
        self._heap.append(elem_with_priority)
        self.sift_up()

    def build_heap(self):
        for i in range(len(self._heap)//2, -1, -1):
            self.sift_down(i)

    def sift_up(self):
        i = len(self._heap) - 1
        while True:
            if (i > 0 and comparator_d(self._heap[i], self._heap[(i-1)//2])):

                self._heap[i], self._heap[(i-1)//2] = self._heap[(i-1)//2],\
                                                      self._heap[i]
                i = (i-1)//2
            else:
                break

    def sift_down(self, element_index):
        i = element_index
        largest = element_index
        if (2*i+1 <= len(self._heap)-1 and comparator_d(self._heap[2*i+1],
                                                        self._heap[i])):
            largest = 2*i + 1
        if (2*i+2 <= len(self._heap)-1 and comparator_d(self._heap[2*i+2],
                                                        self._heap[largest])):
            largest = 2*i + 2
        if (largest != element_index):
            self._heap[i], self._heap[largest] = self._heap[largest],\
                                                 self._heap[i]
            self.sift_down(largest)


class MaxHeap(Heap):

    def __init__(self, array):
        super().__init__(array)

    def extract_maximum(self):
        max_element = None
        if (len(self._heap) != 0):
            max_element = self._heap.pop(0)
            if (len(self._heap) != 0):
                self._heap.insert(0, self._heap.pop())
                self.sift_down(0)
        return max_element


def comparator_d(x, y):
    if x[0] == y[0]:
        return x[1] >= y[1]
    elif x[0] > y[0]:
        return True
    else:
        return False
