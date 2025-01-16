import random

class Random_algorithm:
    """Class that implements the connections between the gates via a random algorithm.
     method __init__ creates the chip and all the occupied segments from the wires on the chip.
     method all_connection calls the make_connection function on all the connections from the 
     netlist (chip.connections).
    method make_connection forms connections by letting them take steps (using make_step function) 
    along a random axis.
    method check_occupied_segment checks if a certain step can be made (if segment is free).
    method make_step lets a connection take a step on a given axes in the correct direction"""

    def __init__(self, chip):
        """Initiates the chip on which te algorithm needs to be implemented in self.chip, and all 
         the already occupied segment in self.occupied_segments. """
        self.chip = chip
        self.occupied_segments = chip.occupied_segments

    def all_connections(self):
        """Loops over every connection to let them form. """
        for connection in self.chip.connections:
            self.make_connection(connection)

    def make_connection(self, connection):
        """Form a connection until it has reached the end gate by taking steps along a random axis
        (either vertical(x), horizontal(y) or up/down(z)). If gridsegment already in use, step will not 
        be 'saved' and thus a different axis is chosen in the next loop."""

        self.current_location = connection.start_location
        counter = 0

        # while current location is not the end location, and there have been less than 200 steps taken
        while connection.check_end() == False and counter < 200:
            counter += 1

            # if there are no possible steps, then stop the algorithm 
            if not self.check_possible_steps(self.current_location, self.occupied_segments, self.chip.gates, self.chip.x_max, self.chip.y_max, self.chip.z_max):
                print(f"No valid steps available from {self.current_location}. No solution found in this experiment.")
                return  # exit the algorithm 
                
            # [0, 1, 2] = [x, y, z]
            axis = random.choice([0, 1, 2])

            # let line/connection take a step in certain axis direction
            new_location = self.make_step(axis, connection)

            # If segment still free, updates its current location
            if self.check_occupied_segment(self.current_location, new_location) == False:
                self.occupied_segments.append((self.current_location, new_location))
                connection.add_coor(new_location)
                self.current_location = new_location

        # check if connection has reached the end location (gate)
        if connection.check_end():
            print('connection succesful')
        else:
            print('connection unsuccesful')


    def check_occupied_segment(self, coor_start, coor_end):
        """Method that checks if a step on a certain gridsegment can be taken, by checking if that
         certain segment is already in self.occupied or not. Returns either True or False. """
        return (coor_start, coor_end) in self.occupied_segments or (coor_end, coor_start) in self.occupied_segments \
                or any(Gate.coor == coor_end for Gate in self.chip.gates.values())
        

    def make_step(self, axis, connection):
            """ Let's the connection take a step according to the end location. It returns the coordinates
            of the new step."""
            
            new_location = list(self.current_location)

            max_borders = [self.chip.x_max, self.chip.y_max, self.chip.z_max]

            # checks if the location is on the border of the chip
            if self.current_location[axis] == 0:
                new_location[axis] += 1

            elif self.current_location[axis] == max_borders[axis]:
                new_location[axis] -= 1

            # if the current value x/y value is bigger than the desired x/y value: -1
            elif self.current_location[axis] > connection.end_location[axis]:
                new_location[axis] -= 1

            # if the current x/y value is smaller: +1
            elif self.current_location[axis] < connection.end_location[axis]:
                new_location[axis] += 1
            
            else:
                new_location[axis] += random.choice([-1, 1])

            return tuple(new_location)
    
    def check_possible_steps(self, current_location, occupied_segments, gates, x_max, y_max, z_max):
        """ Check if there are any steps available from the current location."""
     
        possible_steps = [
        (current_location[0] + 1, current_location[1], current_location[2]),  # x + 1
        (current_location[0] - 1, current_location[1], current_location[2]),  # x - 1
        (current_location[0], current_location[1] + 1, current_location[2]),  # y + 1
        (current_location[0], current_location[1] - 1, current_location[2]),  # y - 1
        (current_location[0], current_location[1], current_location[2] + 1),  # z + 1
        (current_location[0], current_location[1], current_location[2] - 1),  # z - 1 
        ]

        # edge cases: get rid of the steps that are out of bound, already occupied, or is a gate
        valid_steps = []
        for step in possible_steps:
            if (
                0 <= step[0] < x_max and    # check if the step is still within the grid 
                0 <= step[1] < y_max and 
                0 <= step[2] < z_max and 
                (current_location, step) not in occupied_segments and  # Check if the segment (current_location -> step) is already occupied
                (step, current_location) not in occupied_segments and  # Check if the segment (step -> current_location) is already occupied 
                step not in gates.values()  # check if the step is not a gate 
                ):

                valid_steps.append(step)

        return len(valid_steps) > 0  # Return True if there is at least one valid step possible
    
