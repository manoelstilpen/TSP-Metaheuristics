#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Files(object):
    def __init__(self):
        pass

    def read_info(self, path):
        with open(path) as f:
            info = f.readlines()[0].split()
            n_cities, best_fo = int(info[0]), float(info[1])
            return n_cities, best_fo

    def read_cities(self, path):
        with open(path) as f:
            cities = []
            for line in f.readlines():
                index, x, y = (int(x) for x in line.split())
                cities.append((x, y))
            return cities
