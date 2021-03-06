# -*- coding: utf-8 -*-
"""
Created on Sun Sep 30 18:36:43 2018

@author: Lauro Moraes
"""

from Method import Method


class TabuSearch(Method):
    
    def __init__(self, solution):
        super(TabuSearch, self).__init__(solution)
    
    def run(self):
        self.set_metrics('fos', 'stars')
        self.tabu_search()
        return self.solution.fo

    def move_next_tabu_neighbour(self, solution):
        n = self.n_cities
        R = solution.route
        fo = solution.fo
        new_i = new_j = None
        
#        i, j = 1, 2
#        new_i, new_j = i, j
#        
#        delta1 = self.delta(i, j)
#        R[i], R[j] = R[j], R[i]
#        delta2 = self.delta(i, j)
#        fo_best_neighbour = fo_neighbour = fo - delta1 + delta2
#        R[i], R[j] = R[j], R[i]
        
        fo_best_neighbour = float('inf')
        
        # For each city i
        for i in range(0, n):
            # For each city j
            for j in range(i+1, n):

                # Verify total value with edges formed with selecteds cities and respectives neighbours. Called delta value.
                delta1 = solution.delta(i, j)
                # Apply movement. Switch allocation of cities i and j on the R - route.
                R[i], R[j] = R[j], R[i]
                # Verify new delta value.
                delta2 = solution.delta(i, j)

                # Calculate new Objective Function formed by switch.
                fo_neighbour = fo - delta1 + delta2
#                print(i, j, fo_neighbour, fo_neighbour, fo_best_neighbour, self.tabu_matrix[i-1][j-1])

                # Switch back positions of cities, restoring previus R.
                R[i], R[j] = R[j], R[i]  # Remove movement

                # Verify if this new Objective Function is better than global - aspiration.
                if fo_neighbour < self.best_fo and fo_neighbour < fo_best_neighbour:
                    new_i, new_j = i, j
                    fo_best_neighbour = fo_neighbour
                    break
#                    print('TABU', i, j, self.current_iteration, self.tabu_matrix[i-1][j-1])
#                    print(i, j, self.current_iteration, self.tabu_matrix[i-1][j-1])
                elif fo_neighbour < fo_best_neighbour and self.tabu_matrix[i][j] <= self.current_iteration:
                    new_i, new_j = i, j
                    # Store new best Objective Function.
                    fo_best_neighbour = fo_neighbour

#        print(new_i, new_j, self.tabu_matrix[new_i-1][new_j-1])
        return new_i, new_j, fo_best_neighbour
        
    def tabu_search(self, iterMax=50, duration=7):
        import numpy as np
        import copy
        
        self.duration = duration
        self.tabu_matrix = np.zeros((self.n_cities, self.n_cities), dtype=int)
        self.best_fo = self.solution.fo
        S = copy.deepcopy(self.solution)
        
        self.current_iteration = 0
        iterMelhora = 0

        print(self.solution.route)

        while self.current_iteration - iterMelhora < iterMax:
            self.current_iteration += 1
            print(self.current_iteration)
            print('FO: ', self.best_fo)

            new_i, new_j, fo_neighbour = self.move_next_tabu_neighbour(S)
            print(new_i, new_j)
            self.tabu_matrix[new_i][new_j] = self.current_iteration + self.duration

            S.route[new_i], S.route[new_j] = S.route[new_j], S.route[new_i]
            S.fo = fo_neighbour

            print(S.route)

            if S.fo < self.best_fo:
                iterMelhora = self.current_iteration
                self.solution = copy.deepcopy(S)
                self.best_fo = S.fo

            if self.current_iteration % 100 == 0:
                print(S.fo, self.best_fo)

            self.metrics['fos'].append(S.fo)
            self.metrics['stars'].append(self.best_fo)

        return self.solution
