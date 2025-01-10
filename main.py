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


class Chip:
    """ This class contains the code for making the grid. """

    def __init__(self, gates_path, connections_path):
        self.gates = pd.read_csv(gates_path, index_col='chip')
        self.connections = pd.read_csv(connections_path)

        self.x_max = max(self.gates['x']) + 1
        self.y_max = max(self.gates['y']) + 1

        self.occupied_segments = []

    def plot_grid(self):
        """ Plot the grid with vertical and horizontal lines. """
        for line in range(1, self.x_max):
            plt.axvline(line, color='black', linewidth=0.75)

        for line in range(1, self.y_max):
            plt.axhline(line, color='black', linewidth=0.75)

    def plot_connections(self):
        """ Plot the connections in the connections list. """
        for _, connection in self.connections.iterrows():
            Connection(connection, self.gates, self.occupied_segments).make_connection()

    def plot_gates(self):
        """ Plot the gates on the grid. """
        plt.plot(self.gates['x'], self.gates['y'], 'rs', markersize=29 - max([self.x_max, self.y_max]))

        for index, row in self.gates.iterrows():
            plt.text(row['x'], row['y'], index, fontsize=27 - max([self.x_max, self.y_max]),
                     horizontalalignment='center', verticalalignment='center_baseline')

    def show_plot(self):
        """ Adjust the layout and show the grid. """
        plt.xticks([])
        plt.yticks([])
        plt.xlim(0, self.x_max)
        plt.ylim(0, self.y_max)
        plt.show()


class Error:
    """ This class calculates the cost of the solution. """
    
    def __init__(self, chip):
        self.occupied_segments = chip.occupied_segments
        self.gates = chip.gates.values.tolist()

    def calculate_intersections(self):
        """
        Check if segment ends occur mulitple times in the occupied segments list. In other words,
        check if certain point in the grid are used twice or more.
        """
        end_points = []
        for segment in self.occupied_segments:
            if list(segment[1]) not in self.gates:
                end_points.append(segment[1])

        unique_end_points = set(end_points)

        return len(end_points) - len(unique_end_points)

    def error_calculation(self):
        return len(self.occupied_segments) + 300 * self.calculate_intersections()


if __name__ == '__main__':
    gates_path = 'gates&netlists/chip_0/print_0.csv'
    connections_path = 'gates&netlists/chip_0/netlist_1.csv'

    my_chip = Chip(gates_path, connections_path)
    my_chip.plot_grid()
    my_chip.plot_connections()
    my_chip.plot_gates()
    my_chip.show_plot()

    costs = Error(my_chip)
    cost = costs.error_calculation()
    print(f'The costs for this solution: {cost}')
