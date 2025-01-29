import random
from algorithms import general_functions as gf

class Random_algorithm:
    """ 
    Class that implements the connections between the gates via a random algorithm.
    method all_connection calls the make_connection function on all the connections.
    method make_connection applies the algorithm to form the connection by letting it take random steps.
    method make_step lets the connection take a step on a random axes in a random direction.
    method check_possible_steps checks if there are any open segments around the current location. 
    """

    def __init__(self, chip):
        self.chip = chip
        self.occupied_segments = chip.occupied_segments


    def all_connections(self):
        """ Loops over every connection to let them form and return if all the connections in 
        the solution are valid """

        for connection in self.chip.connections:
            self.connection = connection
            self.make_connection()
        
        return gf.Functions().validity(self.chip.connections)


    def make_connection(self):
        """ Forms a connection until it has reached the end gate by taking steps along a random axis
        (x, y or z). Randomly picks a step and takes it if the step is valid and the gridsegment is 
        not already occupied. """

        self.current_location = self.connection.start_location
        self.connection.add_coor(self.current_location)

        # the algorithm can make a maximum of 1000 steps
        for i in range(1000):

            # stops the algorithm if there are no possible next steps
            if not self.check_possible_steps():
                return   
                
            # randomly chooses an axis to move on: [0, 1, 2] = [x, y, z]
            axis = random.choice([0, 1, 2])

            new_location = self.choose_step(axis)

            # takes the step if the chosen step and new location are valid and free
            if gf.Functions().valid_step(self.chip, self.connection, self.current_location, new_location):
                self.occupied_segments.add((self.current_location, new_location))
                self.connection.add_coor(new_location)
                self.current_location = new_location

            # stops the algorithm if the end location is reached
            if self.connection.check_end():
                return
                

    def choose_step(self, axis):
            """ Randomly chooses a direction for the next step along the give axis. """

            # changes the location to a list to be adjustable
            new_location = list(self.current_location)

            max_borders = [self.chip.x_max, self.chip.y_max, self.chip.z_max]

            # prevents the connection from going outside of the borders
            if self.current_location[axis] == 0:
                new_location[axis] += 1
            elif self.current_location[axis] == max_borders[axis]:
                new_location[axis] -= 1

            # randomly chooses which direction to move along the axis
            else:
                new_location[axis] += random.choice([-1, 1])

            return tuple(new_location)

   
    def check_possible_steps(self):
        """ Checks if there are any steps available from the current location. """
     
        # format: (x, y, z)
        possible_steps = [
        (self.current_location[0] + 1, self.current_location[1], self.current_location[2]),
        (self.current_location[0] - 1, self.current_location[1], self.current_location[2]),
        (self.current_location[0], self.current_location[1] + 1, self.current_location[2]),
        (self.current_location[0], self.current_location[1] - 1, self.current_location[2]),
        (self.current_location[0], self.current_location[1], self.current_location[2] + 1),
        (self.current_location[0], self.current_location[1], self.current_location[2] - 1), 
        ]

        for step in possible_steps:
            if (
                 # checks if the step is within the grid 
                0 <= step[0] <= self.chip.x_max and 0 <= step[1] <= self.chip.y_max and 0 <= step[2] <= self.chip.z_max and 

                 # checks if the segment is not already occupied
                (self.current_location, step) not in self.occupied_segments and 
                (step, self.current_location) not in self.occupied_segments and 

                # checks if the step is not to another gate
                (not any(Gate.coor == step for Gate in self.chip.gates.values()) or step == self.connection.end_location) 
                ):

                # return True if there is a valid step possible
                return True
    
