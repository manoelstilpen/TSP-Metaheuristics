#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Files import *
from Solution import *
from Descent import *
from SimulatedAnnealing import *
from MultiStart import *


class Problem(object):

    def __init__(self, name, info_path, cities_path):
        self.name = name
        self.setup(info_path, cities_path)
        self.solution_factory = SolutionFactory(self.distances)
        self.initial_solution = None
        self.solution = None
        self.method = None
        self.n_cities = 0
        self.best_fo = 0
        self.cities = []
        self.distances = []

    def setup(self, info_path, cities_path):
        file_reader = Files()
        self.n_cities, self.best_fo = file_reader.read_info(info_path)
        self.cities = file_reader.read_cities(cities_path)
        self.distances = self.calc_dists()

    def dist(self, i, j):
        return float(((self.cities[i][0]-self.cities[j][0])**2 + (self.cities[i][1]-self.cities[j][1])**2)**.5)

    def calc_dists(self):
        import numpy as np
        distances = np.zeros((self.n_cities, self.n_cities), dtype=float)
        for i in range(self.n_cities):
            for j in range(i+1, self.n_cities):
                distances[i, j] = distances[j, i] = self.dist(i, j)
        return distances

    def create_solution(self, solution_type):
        self.initial_solution = self.solution = self.solution_factory.setup_solution(solution_type)

    def apply_method(self, method_type):
        method_class = getattr(__import__(method_type), method_type)
        self.method = method_class(self.solution)
        self.solution = self.method.solution
        return self.method, self.solution
