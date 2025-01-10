import pandas as pd
import matplotlib.pyplot as plt
import random

class Connection:
    """
    This class creates connections by implementing their starting location (chip a) and
    their einding location (chip b), and lets the connections take form by taking steps in
    the right directions.
    """

    def __init__(self, connection, gates, occupied_segments):
        self.location = gates.loc[connection['chip_a']].copy()
        self.end_location = gates.loc[connection['chip_b']]

        self.occupied_segments = occupied_segments

    def plot_and_update_values(self):
        """
        Plot each step of the connection and updates its current location (end segment becomes
        start of segment, in the next step the new end segment is determined).
        """
        plt.plot((self.segment_start[0], self.segment_end[0]), (self.segment_start[1], self.segment_end[1]), linewidth = 4, color='b')

        self.occupied_segments.append((self.segment_start, self.segment_end))
        self.location.update({'x': self.segment_end[0], 'y': self.segment_end[1]})

    def make_connection(self):
        """
        Form the connections by taking steps. If a certain segment is already in use by a
        connection/wire, the next step will be in the direction of the other axis.
        """
        while self.location['x'] != self.end_location['x'] or self.location['y'] != self.end_location['y']:

            while self.location['x'] != self.end_location['x']:
                Step.make_step(self.location, self.end_location, 'x')

                while (self.segment_start, self.segment_end) in self.occupied_segments or (self.segment_end, self.segment_start) in self.occupied_segments:
                    Step.make_step(self.location, self.end_location, 'y')

                self.plot_and_update_values()

            while self.location['y'] != self.end_location['y']:
                Step.make_step(self.location, self.end_location, 'y')

                while (self.segment_start, self.segment_end) in self.occupied_segments or (self.segment_end, self.segment_start) in self.occupied_segments:
                    Step.make_step(self.location, self.end_location, 'x')

                self.plot_and_update_values()
