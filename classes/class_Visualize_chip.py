import matplotlib.pyplot as plt
import pandas as pd

from classes import class_Connection

class Visualize_chip:
    """ This class contains the code for making the grid.
    Method __init__ creates self.gates, self.connections, self.x_max, self.y_max, 
    and self.occupied_segments.
    Method plot_grid creates the horizontal and vertical lines of the grid.
    Method plot_connections plots the solution for the connections from the Connection class.
    Method plot_gates plots the gates according to their coordinates.
    Method show_plot makes final adjustments to the plot and shows it."""

    def __init__(self, gates, connections_path):
        """ creates self.gates (dataframe with coordinates of gates), self.connections (gates
        to be connected), self.x_max (how wide the grid has to be according to the gates' coordinates), 
        self.y_max (how long grid has to be), and self.occupied_segments (list of segments)."""
        self.gates = gates
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

            # connection --> pandas series (one column chip a, second column chip b)
            class_Connection.Connection(connection, self.gates, self.occupied_segments).make_connection()

    def plot_gates(self):
        """ Plot the gates on the grid."""
        plt.plot(self.gates['x'], self.gates['y'], 'rs', markersize=29 - max([self.x_max, self.y_max]))

        # plot number (index) of gates on top
        for index, row in self.gates.iterrows():
            plt.text(row['x'], row['y'], index, fontsize=27 - max([self.x_max, self.y_max]),
                     horizontalalignment='center', verticalalignment='center_baseline')

    def show_plot(self):
        """ Adjust the layout and show the grid. """

        # remove axes values
        plt.xticks([])
        plt.yticks([])

        # set grid bounds
        plt.xlim(0, self.x_max)
        plt.ylim(0, self.y_max)

        plt.show()


        

