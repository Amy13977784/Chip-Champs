import copy
import random
import math
import pandas as pd 
import matplotlib as plt

from classes import connection, gate, chip
from random_algorithm import Random_algorithm
from astar_algorithm import Astar

class simulated_annealing:
    """ This class implements the simulated annealing algorithm. """
    
    def __init__(self, chip, temperature, cooling_rate, min_temperature):
        self.chip = chip  # chip on which the algorithm is applied
        self.initial_temp = temperature  # starting temperature 
        self.current_temperature = temperature # current temperature
        self.cooling_rate = cooling_rate  # alpha : factor at which the temperature is lowered every iteration
        self.min_temperature = min_temperature  # termination temperature

        # characteristics of the initial / current solution 
        if not chip.occupied_segments:
            print("Occupied segments is empty")
        else:
          self.current_solution = chip.occupied_segments.copy()  
       
        self.best_solution = self.current_solution
        self.current_cost = chip.calculate_cost()
        self.best_cost = self.current_cost


    def update_temperature(self):
        """
        This function implements an exponential cooling scheme.
        """
        self.current_temperature = self.current_temperature * self.cooling_rate


    def accept_solution(self, new_cost):
        """
        Checks whether this new solution is a better solution and is then accepted. 
        If it is a worse solution, then use the acceptation probability to make a decision on whether to accept 
        or reject the new solution. This is based on the current temperature. 

        Returns true if the new solution is accepted. 
        """

        # Calculate cost difference (= diff in energy)
        delta_cost = new_cost - self.current_cost

        # If the new solution is better, always accept 
        if delta_cost < 0:
            return True

        # If the energy is >0 (so worse cost), use accepting probability
        # Higher temperature increases the chance of accepting worse solutions
        acceptance_probability = math.exp(-delta_cost / self.current_temperature)
        return random.random() < acceptance_probability


    def pertubation(self, method = 'reroute_connection'):
        """ 
        This method introduces a pertubation to a current solution. There are a couple of possible 
        pertubations. It can be specified which one you want. 
        """

        if method == "reroute_connection":
            return self.reroute_connection()

        elif method == "swap_segments":
            return self.swap_segments()


    def reroute_connection(self, max_attempts = 5):
        """ Removes a random connection from the current solution and chooses a different path 
        for this conncection using the A* algorithm."""

        # if there are no steps taken yet 
        if not self.current_solution:
            return self.current_solution
        
        # Copy the current solution (such that you can adapt it)
        new_solution = self.current_solution.copy()
        
        # choose a random connection from the current solution
        connection =  random.choice(self.chip.connections)

        # remove the current path from this chosen connection from current solution
        old_path = connection.segments
        for segment in old_path:
            if segment in new_solution:
                new_solution.remove(segment)

        for attempt in range(max_attempts):

            # use A* algorithm to find a new connection
            astar_alg = Astar(self.chip)
            astar_alg.connection = connection
            astar_alg.start_node = Node(connection.start_location, None)
            astar_alg.end_node = Node(connection.end_location, None)

            astar_alg.make_connection()
            new_path = connection.segments

            # Check if the new path is valid 
            if all(self.is_segment_free(segment) for segment in new_path):
               
                # add this path to the solution
                for segment in new_path:
                    new_solution.append(segment)

                return new_solution  
            
        # If all attempts for a new path don't succeed, return the current solution
        return self.current_solution


    def swap_segments(self):
        """ Randomly swaps two segments in the current solution and returns a new solution. """
       
        # Choose a random connection 
        connection = random.choice(self.chip.connections)

        # You need at least two segments in this connection to make the swap 
        if len(connection.segments) < 2:
            return self.current_solution

        new_solution = self.current_solution.copy()

        # Choose a segment from a connection 
        segment_index = random.randint(0, len(connection.segments) - 2)

        # Change this segment with the segment next to it 
        connection.segments[segment_index], connection.segments[segment_index + 1] = (
            connection.segments[segment_index + 1],
            connection.segments[segment_index],
        )

        # Remove the old segments and add the new ones 
        for segment in connection.segments:
            if segment not in new_solution:
                new_solution.append(segment)

        return new_solution


    def is_segment_free(self, segment):
        """Checks if a segment is free (not occupied by other segments or gates)."""
        start, end = segment

        # Check if segment is already occupied
        if (start, end) in self.chip.occupied_segments or (end, start) in self.chip.occupied_segments:
            return False

        # Check if the segment ends in a gate that is not part of the connection
        if any(Gate.coor == end for Gate in self.chip.gates.values()):
            return False

        return True


    def calculate_cost(self, solution):
        self.chip.occupied_segments = solution
        return self.chip.calculate_cost()
    

    def plot_temp(self, df_data):
        plt.plot(df_data["iteration"], df_data["temperature"], label="Temperature", color="blue")
        plt.title("Temperature per iteration")
        plt.xlabel("Iteration")
        plt.ylabel("Temperature")
        plt.grid(True)
        plt.legend()
        plt.show()
    

    def plot_costs(self, df_data):
        plt.plot(df_data["iteration"], df_data["current_cost"], label="Current costs", color="orange")
        plt.plot(df_data["iteration"], df_data["best_cost"], label="Best costs", color="red")
        plt.title("Costs per iteration")
        plt.xlabel("Iteration")
        plt.ylabel("Cost")
        plt.grid(True)
        plt.legend()
        plt.show()


    def run(self, iterations=1000, perturbation_method="reroute_connection"):
        
        logging_data = []
        
        for iteration in range(iterations):
            if self.current_temperature < self.min_temperature:
                break

            # introduce the pertubation and calculate its associated cost
            new_solution = self.perturbation(method = perturbation_method)
            new_cost = self.calculate_cost(new_solution)

            # Decide whether to accpet the new solution
            if self.accept_solution(new_cost):
                self.current_solution = new_solution
                self.current_cost = new_cost

                # Update best soltuion if the new solution is better
                if new_cost < self.best_cost:
                    self.best_solution = new_solution
                    self.best_cost = new_cost

            logging_data.append({
            "iteration": iteration,
            "temperature": self.current_temperature,
            "current_cost": self.current_cost,
            "best_cost": self.best_cost,
            })
            
            # Update the temperature 
            self.update_temperature()

        df_data = pd.DataFrame(logging_data)
        # df_data.to_csv("simulated_annealing_log.csv", index=False)

        self.plot_temp(df_data)
        self.plot_costs(df_data)

        return self.best_solution, self.best_cost

