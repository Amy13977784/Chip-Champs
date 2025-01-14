import random

class Step:
    """ Class that lets a connection/line take step. 
    The method __init__ implements self.location, self.end_location, and the axis (direction of step).
    The method make_step lets the connection take a step and returns the new steps/segments start
    coordinate and end coordinate.""" 

    def __init__(self, location, end_location, axis):
        """Implements self.location (start of last segment/step that was taken), self.end_location (
        end of last segment), and self.axis (x --> horizontal step, y --> vertical step). All
        values given by Connection class, during make_connection function."""
        self.location = location
        self.end_location = end_location
        self.axis = axis

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
