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

    def step(self, axis):
        """ Let's the connection take a step according to the end location. """
        if self.location[axis] > self.end_location[axis]:
            new_location = self.location[axis] - 1
        elif self.location[axis] < self.end_location[axis]:
            new_location = self.location[axis] + 1
        else:
            new_location = self.location[axis] + random.choice([-1, 1])

        self.segment_start = (self.location['x'], self.location['y'])

        if axis == 'x':
            self.segment_end = (new_location, self.location['y'])
        else:
            self.segment_end = (self.location['x'], new_location)


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
                self.step('x')

                while (self.segment_start, self.segment_end) in self.occupied_segments or (self.segment_end, self.segment_start) in self.occupied_segments:
                    self.step('y')

                self.plot_and_update_values()

            while self.location['y'] != self.end_location['y']:
                self.step('y')

                while (self.segment_start, self.segment_end) in self.occupied_segments or (self.segment_end, self.segment_start) in self.occupied_segments:
                    self.step('x')

                self.plot_and_update_values()
