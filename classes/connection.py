import random

class Connection:
    """Class creates connections by implementing their starting location (chip a) and
    their einding location (chip b), and lets the connections take form by taking random steps in
    the right directions.
    Method __init__ implements self.location, self.end_location and self.occupied_segments.
    Method plot_and_update_values plots and tracks the connections steps.
    Method make_connection lets the connections take steps until end location."""

    def __init__(self, connection, gates, occupied_segments):
        """Implements the starting location of the connections (the first gates, chip_a) in self.location,
        and the end destination (chip_b). It also implements all the already occuppied segment in the
        self.occupied_segments list."""
        self.location = gates.loc[connection['chip_a']].copy()
        self.end_location = gates.loc[connection['chip_b']]
        self.gates = gates

        self.occupied_segments = occupied_segments


    def make_connection(self):
        """Form a connection until it has reached the end gate by taking steps in a random direction 
        (either vertical or horizontal). If gridsegment alreadyin use, step will not be 'saved' and 
        thus a different direction is chosen in the next loop."""

        # while current location is not the end location (for both x and y coordinate)
        while self.location['x'] != self.end_location['x'] or self.location['y'] != self.end_location['y'] or self.location['z'] != self.end_location['z']:

            while self.location['x'] != self.end_location['x'] or self.location['y'] != self.end_location['y']:
                
                # if both x and y values are not correct --> choose random direction
                if self.location['x'] == self.end_location['x']:
                    axis = 'y'

                elif self.location['y'] == self.end_location['y']:
                    axis = 'x'
                
                else:
                    axis = random.choice(['x','y'])

                # let line/connection take a step in certain axis direction
                self.segment_start, self.segment_end = self.make_step(self.location, self.end_location, axis)

                # If segment still free, updates its current location (end segment becomes start of segment, in the next step the new end segment is determined).
                if (self.segment_start, self.segment_end) in self.occupied_segments or (self.segment_end, self.segment_start) in self.occupied_segments \
                    or self.segment_end in self.gates:
                    if axis == 'x':
                        axis = 'y'
                    else:
                        axis = 'x'
        
                    self.segment_start, self.segment_end = self.make_step(self.location, self.end_location, axis)

                if (self.segment_start, self.segment_end) in self.occupied_segments or (self.segment_end, self.segment_start) in self.occupied_segments \
                    or self.segment_end in self.gates:
                    self.segment_start, self.segment_end = self.make_step(self.location, self.end_location, 'z')
                    
                if (self.segment_start, self.segment_end) not in self.occupied_segments and (self.segment_end, self.segment_start) not in self.occupied_segments \
                    and self.segment_end not in self.gates:

                    print(self.segment_end)
                    self.occupied_segments.append((self.segment_start, self.segment_end))
                    self.location.update({'x': self.segment_end[0], 'y': self.segment_end[1], 'z': self.segment_end[2]})

            while self.location['z'] != self.end_location['z']:
                self.segment_start, self.segment_end = self.step_down(self.location, self.end_location, 'z')
            
                if (self.segment_start, self.segment_end) not in self.occupied_segments and (self.segment_end, self.segment_start) not in self.occupied_segments \
                    and self.segment_end not in self.gates:

                    print(self.segment_end)
                    self.occupied_segments.append((self.segment_start, self.segment_end))
                    self.location.update({'x': self.segment_end[0], 'y': self.segment_end[1], 'z': self.segment_end[2]})

                else:
                    
                    axis = random.choice(['x', 'y'])
                    self.segment_start, self.segment_end = self.make_step(self.location, self.end_location, axis)
                    self.segment_start, self.segment_end = self.step_down(self.location, self.end_location, 'z')
                    
                    while (self.segment_start, self.segment_end) in self.occupied_segments or (self.segment_end, self.segment_start) in self.occupied_segments \
                    or self.segment_end in self.gates:
                        
                        axis = random.choice(['x', 'y'])
                        self.segment_start, self.segment_end = self.make_step(self.location, self.end_location, axis)
                        self.segment_start, self.segment_end = self.step_down(self.location, self.end_location, 'z')

                    print(self.segment_end)
                    self.occupied_segments.append((self.segment_start, self.segment_end))
                    self.location.update({'x': self.segment_end[0], 'y': self.segment_end[1], 'z': self.segment_end[2]})

    def step_down(self):
        new_location = self.location['z'] - 1

        segment_start = (self.location['x'], self.location['y'], self.location['z'])
        segment_end = (self.location['x'], self.location['y'], new_location)

        return segment_start, segment_end

    def make_step(self):
        """ Let's the connection take a step according to the end location. It returns the coordinates
        of the start of the step (segment_start) and the end of the step (segment_end)."""
        
        # if it x/y is equal: randomly -1 or +1
        if self.location[self.axis] == 0 or self.axis == 'z':
            new_location = self.location[self.axis] + 1

        elif self.axis == 'x' and self.location['x'] == 7:
            new_location = self.location[self.axis] - 1
        
        elif self.axis == 'y' and self.location['y'] == 6:
            new_location = self.location[self.axis] - 1

        # if the current value x/y value is bigger than the desired x/y value: -1
        elif self.location[self.axis] > self.end_location[self.axis]:
            new_location = self.location[self.axis] - 1

        # if the current x/y value is smaller: +1
        elif self.location[self.axis] < self.end_location[self.axis]:
            new_location = self.location[self.axis] + 1
        
        else:
            new_location = self.location[self.axis] + random.choice([-1, 1])

        # get coordinates of the beginning point from segment
        segment_start = (self.location['x'], self.location['y'], self.location['z'])

        # get coordinates of end point from segment (tuple made according to direction of step)
        if self.axis == 'x':
            segment_end = (new_location, self.location['y'], self.location['z'])
        elif self.axis == 'y':
            segment_end = (self.location['x'], new_location, self.location['z'])
        else:
            segment_end = (self.location['x'], self.location['y'], new_location)

        return segment_start, segment_end




