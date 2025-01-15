import random

class Random_algorithm:
    def __init__(self, chip):
        self.chip = chip
        self.occupied_segments = chip.occupied_segments

    def all_connections(self):
        for connection in self.chip.connections:
            self.make_connection(connection)

    def make_connection(self, connection):
        """Form a connection until it has reached the end gate by taking steps in a random direction 
        (either vertical or horizontal). If gridsegment alreadyin use, step will not be 'saved' and 
        thus a different direction is chosen in the next loop."""

        self.current_location = connection.start_location
        counter = 0

        # while current location is not the end location (for both x and y coordinate)
        while connection.check_end() == False and counter < 200:
            counter += 1
                
            # [0, 1, 2] = [x, y, z]
            axis = random.choice([0, 1, 2])

            # let line/connection take a step in certain axis direction
            new_location = self.make_step(axis, connection)

            # If segment still free, updates its current location (end segment becomes start of segment, in the next step the new end segment is determined).
            if self.check_occupied_segment(self.current_location, new_location) == False:
                self.occupied_segments.append((self.current_location, new_location))
                connection.add_coor(new_location)
                self.current_location = new_location

        if connection.check_end():
            print('connection succesful')
        else:
            print('connection unsuccesful')


    def check_occupied_segment(self, coor_start, coor_end):
        return (coor_start, coor_end) in self.occupied_segments or (coor_end, coor_start) in self.occupied_segments \
                or any(Gate.coor == coor_end for Gate in self.chip.gates.values())
        

    def make_step(self, axis, connection):
            """ Let's the connection take a step according to the end location. It returns the coordinates
            of the start of the step (segment_start) and the end of the step (segment_end)."""
            
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