import random
import math
import copy
import pandas as pd 
import matplotlib as plt

from algorithms import astar_algorithm 

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
          self.current_solution = copy.deepcopy(chip.occupied_segments)
       
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


    def reroute_connection(self, max_attempts = 5):
        """ Removes a random connection from the current solution and chooses a different path 
        for this conncection using the A* algorithm."""
        
        # Copy the current solution (such that you can adapt it)
        new_solution = self.current_solution.copy()
        
        # choose a random connection from the current solution
        connection =  random.choice(self.chip.connections)

        # these are the coordinates that form the connection 
        old_path = connection.coor_list

        # remove the coordinates for this connection 
        for coor in old_path:
            if coor in new_solution:
                new_solution.remove(coor)

        for attempt in range(max_attempts):

            # use A* algorithm to find a new connection
            astar_alg = astar_algorithm.Astar(self.chip)
            astar_alg.connection = connection
            astar_alg.start_node = astar_algorithm.Node(connection.start_location, None)
            astar_alg.end_node = astar_algorithm.Node(connection.end_location, None)

            astar_alg.make_connection()
            new_path = connection.coor_list # of astar_algorithm.connection.coor_list ?

            path_valid = True

            for i in range(len(new_path) - 1):
                segment = (new_path[i], new_path[i + 1])
                if not self.is_segment_free(segment, connection.end_location):
                    path_valid = False

                    # if the path is not valid, then try to make a new (valid) connection with A*
                    break

            if path_valid:

                # Add this path to the solution
                for coor in new_path:
                    new_solution.append(coor)

                return new_solution  
            
        # If all attempts for a new path don't succeed, return the current solution
        return self.current_solution


    def is_segment_free(self, segment, connection_end_location):
        """Checks if a segment is free (not occupied by other segments or gates (unless end gate))."""

        start, end = segment

        # If the segment is already occupied, then this segment is not available 
        if (start, end) in self.chip.occupied_segments or (end, start) in self.chip.occupied_segments:
            return False

        # It is allowed for the end coordinate of this segment to end in its end-gate of the connection 
        if end == connection_end_location:
            return True

        # Check if the segment's end-coordinate ends in a gate that is not the end gate of this connection 
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


    def run(self, iterations=1000):
        
        logging_data = []
        
        for iteration in range(iterations):
            if self.current_temperature < self.min_temperature:
                break

            # Introduce the pertubation and calculate its associated cost
            new_solution = self.reroute_connection() 
            new_cost = self.calculate_cost(new_solution)

            # Decide whether to accept the new solution
            if self.accept_solution(new_cost):
                self.current_solution = new_solution
                self.current_cost = new_cost

                # Update best solution if the new solution is better
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

