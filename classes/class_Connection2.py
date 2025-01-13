import matplotlib.pyplot as plt
import random

from classes import class_Step

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

        self.occupied_segments = occupied_segments

    def plot_and_update_values(self):
        """Plots each step of the connection and updates its current location (end segment becomes
        start of segment, in the next step the new end segment is determined)."""
        plt.plot((self.segment_start[0], self.segment_end[0]), (self.segment_start[1], self.segment_end[1]), linewidth = 4, color='b')

        self.occupied_segments.append((self.segment_start, self.segment_end))
        self.location.update({'x': self.segment_end[0], 'y': self.segment_end[1]})

    def make_connection(self):
        """Form the connections by keep initializing a step until it has reached the end gate by 
        taking steps in a random direction (either vertical or horizontal). If gridsegment already
        in use, step will not be 'saved' and thusa different direction is chosen in the next loop."""

        # while current location is not the end location (for both x and y coordinate)
        while self.location['x'] != self.end_location['x'] or self.location['y'] != self.end_location['y']:

            # if both x and y values are not correct --> choose random direction
            if self.location['x'] != self.end_location['x'] and self.location['y'] != self.end_location['y']:
                axis = random.choice(['x', 'y'])

            # if x value correct --> only move in vertical direction
            elif self.location['x'] == self.end_location['x']:
                axis = 'y'

            # if y value correct --> only move in horizontal direction
            else:
                axis = 'x'

            # let line/connection take a step in certain axis direction
            self.segment_start, self.segment_end = class_Step.Step(self.location, self.end_location, axis).make_step()

            # If segment still free
            if (self.segment_start, self.segment_end) not in self.occupied_segments and (self.segment_end, self.segment_start) not in self.occupied_segments:
                self.plot_and_update_values()
