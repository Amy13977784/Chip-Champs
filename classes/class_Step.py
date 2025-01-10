import random

class Step:
    def __init__(self, location, end_location, axis):
        self.location = location
        self.end_location = end_location
        self.axis = axis

    def make_step(self):
        """ Let's the connection take a step according to the end location. """
        if self.location[self.axis] > self.end_location[self.axis]:
            new_location = self.location[self.axis] - 1
        elif self.location[self.axis] < self.end_location[self.axis]:
            new_location = self.location[self.axis] + 1
        else:
            new_location = self.location[self.axis] + random.choice([-1, 1])

        segment_start = (self.location['x'], self.location['y'])

        if self.axis == 'x':
            segment_end = (new_location, self.location['y'])
        else:
            segment_end = (self.location['x'], new_location)

        return segment_start, segment_end
