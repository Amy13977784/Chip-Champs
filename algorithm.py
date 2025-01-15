import random

class Random_algorithm:
    def __init__(self, connections, chip):
        self.connections = connections
        self.occupied_segments = chip.occupied_segments

    def all_connections(self):
        for con in self.connections:
            self.make_connection(con)

    def make_connection(self, connection):
        """Form a connection until it has reached the end gate by taking steps in a random direction 
        (either vertical or horizontal). If gridsegment alreadyin use, step will not be 'saved' and 
        thus a different direction is chosen in the next loop."""

        self.current_location = connection.start_location.copy()

        # while current location is not the end location (for both x and y coordinate)
        while not connection.check_end() == False:
                
            # [0, 1, 2] = [x, y, z]
            axis = random.choice([0, 1, 2])

            # let line/connection take a step in certain axis direction
            coor_start, coor_end = self.make_step(self.current_location, connection.end_location, axis)

            # If segment still free, updates its current location (end segment becomes start of segment, in the next step the new end segment is determined).
            if not self.check_occupied_segment(coor_start, coor_end):
                print(coor_end)
                self.occupied_segments.append((coor_start, coor_end))
                self.current_location = coor_end


    def check_occupied_segment(self, coor_start, coor_end):
        return (coor_start, coor_end) in self.occupied_segments or (coor_end, coor_start) in self.occupied_segments \
                or coor_end in self.gates
    

    def make_step(self, axis, connection):
            """ Let's the connection take a step according to the end location. It returns the coordinates
            of the start of the step (segment_start) and the end of the step (segment_end)."""
            
            # if it x/y is equal: randomly -1 or +1
            if self.current_location[axis] == 0:
                new_location = self.current_location[axis] + 1

            elif self.axis == 0 and self.current_location[axis] == 7:
                new_location = self.current_location[axis] - 1
            
            elif self.axis == 1 and self.current_location[axis] == 6:
                new_location = self.current_location[axis] - 1

            # if the current value x/y value is bigger than the desired x/y value: -1
            elif self.current_location[axis] > connection.end_location[axis]:
                new_location = self.location[axis] - 1

            # if the current x/y value is smaller: +1
            elif self.current_location[axis] < connection.end_location[axis]:
                new_location = self.location[axis] + 1
            
            else:
                new_location = self.current_location[axis] + random.choice([-1, 1])


            # get coordinates of the beginning point from segment
            coor_start = self.current_location

            # get coordinates of end point from segment (tuple made according to direction of step)
            if self.axis == 0:
                coor_end = (new_location, self.current_location[1], self.current_location[2])
            elif self.axis == 1:
                coor_end = (self.current_location[0], new_location, self.current_location[2])
            else:
                coor_end = (self.current_location[0], self.current_location[1], new_location)

            return coor_start, coor_end