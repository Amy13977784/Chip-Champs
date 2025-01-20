import copy
import random
import math

from classes import connection, gate, chip
from random_algorithm import Random_algorithm

class simulated_annealing:
    """ This class implements the simulated annealing algorithm. """
    
    def __init__(self, chip, temperature, cooling_rate, min_temperature):
        self.chip = chip  # chip on which the algorithm is applied
        self.temperature = temperature  # initial temperature 
        self.cooling_rate = cooling_rate  # factor at which the temperature is lowered every iteration
        self.min_temperature = min_temperature  # termination temperature

        # characteristics of the initial / current solution 
        self.current_solution = chip.occupied_segments.copy()  
        self.best_solution = self.current_solution
        self.current_cost = chip.calculate_cost()
        self.best_cost = self.current_cost

    def pertubation(self, method = 'reroute_connection'):
        """ 
        This method executes a pertubation on a current solution. There are a couple of possible 
        pertubations. It can be specified which one you want. This method returns a new solution. 
        """

        if method == "reroute_connection":
            return self.reroute_connection()
        elif method == "swap":
            return self.swap_connections()
        elif method == "reroute":
            return self.reroute_connection()

    def reroute_connection(self):
        """ Removes a random connection from the current solution and chooses a different path 
        for this conncection."""

        # if there are no steps taken yet 
        if not self.current_solution:
            return self.current_solution
        
        new_solution = self.current_solution.copy()
        
        # choose a random connection from the current solution
        connection =  random.choice(self.chip.connections)

        # remove the current path from this chosen connection from current solution
        old_path = connection.segments
        for segment in old_path:
            if segment in new_solution:
                new_solution.remove(segment)

        # apply the random algorithm to generate a new path for this connection
        random_alg = Random_algorithm(self.chip)
        random_alg.connection = connection
        random_alg.make_connection()

        # add the new path of the connection to the new solution
        new_path = connection.segments
        for segment in new_path:
            if segment not in new_solution:
                new_solution.append(segment)

        return new_solution
    
    def swap_connections(self):
        """ This method swaps two random connections in the current solution and returns this as a new solution. """

        # you need at least 2 connections 
        if len(self.chip.connections) < 2:
            return self.current_solution
        
        new_solution = self.current_solution.copy()
        connection1, connection2 = random.sample(self.chip.connections, 2)  # randomly choose 2 connections

        # swap the start and end locations from the connections 
        connection1.start_location, connection2.start_location = connection2.start_location, connection1.start_location
        connection1.end_location, connection2.end_location = connection2.end_location, connection1.end_location

        return new_solution



        
        