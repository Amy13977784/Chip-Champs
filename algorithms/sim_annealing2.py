import random
import math
import copy
import pandas as pd 
import matplotlib.pyplot as plt

from algorithms import astar_algorithm 

class simulated_annealing:
    """ This class implements the simulated annealing algorithm. 
    Method __init__ initiates the chip. 
    Method update_temperature calculates the new temperature after an iteration. 
    Method accept_solution determines whether to accept or reject a new solution. 
    Method reroute_connection chooses a random connection from current solution and reroutes it using A*.  
    Method is_segment_free checks if a segment is free such that you can make a valid new connection. 
    Method calculate_cost calculates the costs for a solution. 
    Method plot_temp plots the iterations against the temperature. 
    Method plot_costs plots the iterations against the costs. 
    Method run runs the simulated annealing algorithm. """
    
    def __init__(self, chip, temperature, cooling_rate, min_temperature):
        self.chip = chip  # chip on which the algorithm is applied
        self.initial_temp = temperature  # starting temperature 
        self.current_temperature = temperature # current temperature
        self.cooling_rate = cooling_rate  # alpha: factor at which the temperature is lowered every iteration
        self.min_temperature = min_temperature  # termination temperature

        if not chip.occupied_segments:
            print("Occupied segments is empty...")
        else:
          self.current_solution = copy.deepcopy(chip.occupied_segments)
       
        self.best_solution = self.current_solution  
        self.current_cost = chip.calculate_cost()
        self.best_cost = self.current_cost

    def update_temperature(self):
        """ This function implements an exponential cooling scheme: T_new = alpha * T_current """
        self.current_temperature = self.current_temperature * self.cooling_rate

    def accept_solution(self, new_cost):
        """ Checks whether a new solution after the perturbation has lower costs than the current solution. If so, 
        this new solution is accepted as the new current solution. If not, then use the acceptation 
        probability to decide whether to accept or reject this worse solution. A higher temperature increases the 
        chance of accepting a worse solutions. This method returns true if the new solution is accepted. """

        # Calculate the cost difference (= diff in energy)
        delta_cost = new_cost - self.current_cost

        # If the new solution is better, always accept 
        if delta_cost < 0:
            return True

        # If delta_cost is >0 (so worse cost), use acceptance probability
        acceptance_probability = math.exp(-delta_cost / self.current_temperature)
        return random.random() < acceptance_probability

    def random_layers(self, point, connection, new_solution, max_retries = 5):
        """ This method helps to reroute the start of a path where an intersection occurs. It generate 
        a random number of vertical steps to avoid intersections. The method needs a starting point: a 
        coordinate for where to start the vertical movement. Furthermore, it needs the current connection that is 
        being rerouted and the new_solution such that the coordinates can be modified."""

        for attempt in range(max_retries):
            print(f"Attempt {attempt+1}/{max_retries} for vertical reroute.") 

            # Randomly pick a number of layers to go upwards 
            layers_to_add = random.randint(1, self.chip.z_max - point[2])

            steps_up = []

            # Add the coordinates of only this new vertical path to the list 
            for layer in range(1, layers_to_add + 1):
                new_coor = (point[0], point[1], point[2] + layer)
                steps_up.append(new_coor)

            print(f"Generated vertical path: {steps_up}")    

            valid_path = True 

            # Validate the vertical steps (check if they are in occupied segments). If not valid, go to next iteration
            for step in zip(steps_up, steps_up[1:]):
                if step in new_solution:
                    valid_path = False 
                    print(f"Step {step} is occupied.")
                    break 
            
            if valid_path:
                # Set a new start location for the A* to run from 
                connection.start_location = steps_up[-1]
                print(f"Vertical path valid: {steps_up}") 
                return steps_up
       
        print("All vertical path attempts failed.")
        return None
    
    def reroute_from_start(self, connection, old_path, new_solution):
        """ Reroute the connection from the start coordinate of the current connection. The input requires an 
        old_path that holds the original path coordinates of the connection."""
       
        # Remove the old path from the connection 
        for segment in zip(old_path, old_path[1:]):
            if segment in new_solution:
                new_solution.remove(segment)

        return self.random_layers(connection.start_location, connection, new_solution)

    def reroute_from_intersection(self, connection, old_path, new_solution, intersection):
        index_intersect = connection.coor_list.index(intersection)
        
        kept_path = None

        for step_back in [1, 2, 3]:
            new_start = connection.coor_list[index_intersect - step_back]
            steps_up = self.random_layers(new_start, connection, new_solution)
            if steps_up:
                kept_path = old_path[:index_intersect - step_back + 1]
                kept_path.extend(steps_up)
                definite_step_back = step_back
                break

        if not kept_path:
            return None
        
        for segment in zip(old_path[index_intersect - definite_step_back:], old_path[index_intersect - definite_step_back + 1:]):
            if segment in new_solution:
                new_solution.remove(segment)

        return kept_path

    def reroute_connection(self):
        """ Removes a random connection from the current solution and chooses a different path 
        for this conncection using the A* algorithm."""
        
        # Copy the current solution (such that you can adapt it)
        new_solution = copy.deepcopy(self.current_solution)
        
        self.chip.calculate_intersections()

        # choose a random connection from the current solution
        intersection =  random.choice(self.chip.intersection_coors)

        for con in self.chip.connections:
            if intersection in con.coor_list:
                connection = con
                break

        # these are the coordinates that form the connection 
        old_path = copy.deepcopy(connection.coor_list)

        pertubation = random.choice(['from start', 'from intersection'])
        print(pertubation)

        if pertubation == 'from start':
            steps_up = self.reroute_from_start(connection, old_path, new_solution)
        else:
            steps_up = self.reroute_from_intersection(connection, old_path, new_solution, intersection)

        if steps_up == None:
            print("Failed to reroute vertically.")
            return None
        
        print(f"Steps up successfully added: {steps_up}") 

        # use A* algorithm to find a new connection
        astar_alg = astar_algorithm.Astar(self.chip, ['intersections'])
        astar_alg.counter = 1
        astar_alg.connection = connection
        astar_alg.start_node = astar_algorithm.Node(connection.start_location, None)
        astar_alg.end_node = astar_algorithm.Node(connection.end_location, None)

        connection.coor_list = []
        astar_alg.make_connection()

        connection.start_location = old_path[0]

        if not connection.coor_list:
            print("A* failed to find a path.")
            return None
        
        connection.coor_list[:0] = steps_up[-1]
        new_path = copy.deepcopy(connection.coor_list)

        # Add this path to the solution
        for segment in zip(new_path, new_path[1:]):
            new_solution.add(segment)  # is new_solution een set of een lijst? anders append gebruiken

        return new_solution  
            
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

    def run(self, iterations):
        
        logging_data = []
        
        for iteration in range(iterations):
            if self.current_temperature < self.min_temperature:
                break

            # Introduce the pertubation and calculate its associated cost
            new_solution = self.reroute_connection()

            if new_solution == None:
                print("Reroute failed, skipping iteration")
                continue
            
            print(f"Current costs: {self.current_cost}")
            new_cost = self.calculate_cost(new_solution)
            print(f"New costs: {new_cost}")

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

        return self.best_solution

