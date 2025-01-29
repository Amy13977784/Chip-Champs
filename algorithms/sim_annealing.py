import random
import math
import copy
import pandas as pd 
import matplotlib.pyplot as plt

from algorithms import astar 

class SimulatedAnnealing:
    """ Class implements the simulated annealing algorithm. 
    Method __init__ initiates the chip. 
    Method update_temperature calculates the new temperature after an iteration. 
    Method accept_solution determines whether to accept or reject a new solution. 
    Method random_layer randomly picks how many layers to move up and change the starting pint to.
    Method reroute_from_start reroutes the entire connection from start.
    Method reroute_from_intersection reroutes starting right in front of the intersection.
    Method reroute_connection chooses a random connection from current solution and reroutes it using A*.  
    Method calculate_cost calculates the costs for a solution. 
    Method plot_temp plots the iterations against the temperature. 
    Method plot_costs plots the iterations against the costs. 
    Method run runs the simulated annealing algorithm. """
    
    def __init__(self, chip, temperature, cooling_rate, min_temperature):
        self.chip = chip
        self.initial_temp = temperature  
        self.current_temperature = temperature
        self.cooling_rate = cooling_rate
        self.min_temperature = min_temperature
        self.counter = 0

        if not chip.occupied_segments:
            print("Occupied segments is empty...")
        else:
          self.current_solution = copy.deepcopy(chip.occupied_segments)
       
        self.best_solution = copy.deepcopy(chip)  
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

        # calculate the cost difference (= diff in energy)
        delta_cost = new_cost - self.current_cost

        # if the new solution is better, always accept 
        if delta_cost < 0:
            return True

        # if delta_cost is > 0 (so worse cost), use acceptance probability
        acceptance_probability = math.exp(-delta_cost / self.current_temperature)
        return random.random() < acceptance_probability


    def random_layers(self, point, connection, new_solution, max_retries = 5):
        """ This method generates a random number of vertical steps to a starting point and if
        these steps up are valid, changes the starting point of the connections to the top of 
        these steps. The new connection will be made starting from a higher layer. """

        for attempt in range(max_retries):

            # randomly pick a number of layers to go upwards 
            layers_to_add = random.randint(1, self.chip.z_max - point[2] + 1)

            steps_up = []

            # add the coordinates of only this new vertical path to the list 
            for layer in range(1, layers_to_add + 1):
                new_coor = (point[0], point[1], point[2] + layer)
                steps_up.append(new_coor)

            valid_path = True 

            # validate the vertical steps (check if they are in occupied segments). If not valid, go to next iteration
            for step_start, step_end in zip(steps_up, steps_up[1:]):
                if (step_start, step_end) in new_solution or (step_end, step_start) in new_solution:
                    valid_path = False 
                    break 
            
            if valid_path:
                # set a new start location for the A* to run from 
                connection.start_location = steps_up[-1]
                print(f"Vertical path valid: {steps_up}") 
                return steps_up
       
        print("All vertical path attempts failed.")
        return None
    

    def reroute_from_start(self, connection, old_path, new_solution):
        """ Reroutes the connection from the start coordinate of the current connection. Removes the
         entire old path and adds steps up to the starting point. """
       
        # remove the old path from the connection 
        for segment in zip(old_path, old_path[1:]):
            if segment in new_solution:
                new_solution.remove(segment)

        start = [connection.start_location]
        steps_up = self.random_layers(connection.start_location, connection, new_solution)

        return start + steps_up


    def reroute_from_intersection(self, connection, old_path, new_solution, intersection):
        """ Reroutes the connection from the intersection of the current connection. Moves back from
        the intersections coordinates, adds steps up there and only reroutes the last part of the
        connection. """
        
        index_intersect = connection.coor_list.index(intersection)
        
        kept_path = None

        # checks how many steps back from the intersect it can move upwards
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
        
        # removes the segments starting from the point that will be rerouted
        for segment in zip(old_path[index_intersect - definite_step_back:], old_path[index_intersect - definite_step_back + 1:]):
            if segment in new_solution:
                new_solution.remove(segment)

        return kept_path


    def reroute_connection(self):
        """ Removes a random connection from the current solution and chooses a different path 
        for this conncection using the A* algorithm."""
        
        # copy the current solution (such that you can adapt it)
        new_solution = copy.deepcopy(self.current_solution)
        
        self.chip.calculate_intersections()

        # choose a random connection from the current solution
        intersection =  random.choice(self.chip.intersection_coors)

        connection = None

        for con in self.chip.connections:
            if intersection in con.coor_list:
                connection = con
                break
            
        if connection is None:
            return
        
        # the coordinates that form the connection 
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
        
        # use A* algorithm to find a new connection
        astar_alg = astar.Astar(self.chip, ['intersections'], 10)
        astar_alg.counter = self.counter
        astar_alg.connection = connection
        astar_alg.start_node = astar.Node(connection.start_location, None)
        astar_alg.end_node = astar.Node(connection.end_location, None)

        connection.coor_list = []
        astar_alg.make_connection()

        connection.start_location = old_path[0]

        if not connection.coor_list:
            print("A* failed to find a path.")
            connection.coor_list = old_path
            return None
        
        connection.coor_list = steps_up[:-1] + connection.coor_list
        new_path = copy.deepcopy(connection.coor_list)

        # add this path to the solution
        for segment in zip(new_path, new_path[1:]):
            new_solution.add(segment) 

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
        plt.plot(df_data["iteration"], df_data["best_cost"], label="Best costs", color="red", linestyle='dashed')
        plt.title("Costs per iteration")
        plt.xlabel("Iteration")
        plt.ylabel("Cost")
        plt.grid(True)
        plt.legend()
        plt.show()


    def run(self, iterations):
        
        logging_data = [{
            "iteration": 0,
            "temperature": self.current_temperature,
            "current_cost": self.current_cost,
            "best_cost": self.best_cost,
            }]
        
        for iteration in range(1, iterations + 1):
            if self.current_temperature < self.min_temperature:
                break

            self.counter += 1

            # introduce the pertubation and calculate its associated cost
            new_solution = self.reroute_connection()

            if new_solution:
                            
                print(f"Current costs: {self.current_cost}")
                new_cost = self.calculate_cost(new_solution)
                print(f"New costs: {new_cost}")

                # decide whether to accept the new solution
                if self.accept_solution(new_cost):
                    self.current_solution = new_solution
                    self.current_cost = new_cost

                    # update best solution if the new solution is better
                    if new_cost < self.best_cost:
                        self.best_solution = copy.deepcopy(self.chip)
                        self.best_solution.occupied_segments = copy.deepcopy(new_solution)
                        self.best_cost = new_cost

            logging_data.append({
                "iteration": iteration,
                "temperature": self.current_temperature,
                "current_cost": self.current_cost,
                "best_cost": self.best_cost,
                })
            
            self.update_temperature()

        df_data = pd.DataFrame(logging_data)

        self.plot_temp(df_data)
        self.plot_costs(df_data)
