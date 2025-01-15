import pandas as pd
import matplotlib.pyplot as plt

from classes_new import connection
from classes_new import gate

class Chip:
    def __init__(self):
        self.gates = {}
        self.connections = []

        self.occupied_segments = []

    def gates_dict(self, gates_path):

        gates = pd.read_csv(gates_path, index_col='chip')
        gates['z'] = 0
        for index,i in gates.iterrows():
            coordinaten = []
            for j in i:
                coordinaten.append(j)
            coordinaten_gate = tuple(coordinaten)
            self.gates[index:gate.Gate(coordinaten_gate)]


    def connections_list(self, connections_path):
        """ Plot the connections in the connections list. """
        connections = pd.read_csv(connections_path)
        for _, con in connections.iterrows():

            # connection --> pandas series (one column chip a, second column chip b)
            connection.Connection(con, self.gates, self.occupied_segments).make_connection()

    def plot_chip(self):

        self.x_max = max(self.gates['x']) + 1
        self.y_max = max(self.gates['y']) + 1
        self.z_max = 7
        
        plt.axes(projection='3d')
    
        for x in range(1, self.x_max):
            plt.plot(x, [0, self.y_max], 0, color='black', linewidth=0.5)
        for y in range(1, self.y_max):
            plt.plot([0, self.x_max], y, 0, color='black', linewidth=0.5)

        for segment in self.occupied_segments:
            plt.plot((segment[0][0], segment[1][0]), (segment[0][1], segment[1][1]), (segment[0][2], segment[1][2]), linewidth = 3, color='b')

        plt.plot(self.gates['x'], self.gates['y'], self.gates['z'], 'rD', markersize=18 - max([self.x_max, self.y_max]))

        ax = plt.gca()
        # plot number (index) of gates on top
        for index, row in self.gates.iterrows():
            ax.text(row['x'], row['y'], row['z'], index, fontsize=18 - max([self.x_max, self.y_max]),
                     horizontalalignment='center', verticalalignment='center_baseline')

        # remove axes values
        plt.xticks([])
        plt.yticks([])

        # set grid bounds
        plt.xlim(0, self.x_max)
        plt.ylim(0, self.y_max)

        ax = plt.gca()  # get the current axis
        ax.set_zlim(0, self.z_max)

        plt.show()

    def calculate_intersections(self):
        """Check if segment ends occur mulitple times in the occupied segments list. In other words,
        check if certain point in the grid are used twice or more."""
        end_points = []
        for segment in self.occupied_segments:

            # check if the segment end is not a gate/destination
            if list(segment[1]) not in self.gates:
                end_points.append(segment[1])

        unique_end_points = set(end_points)

        return len(end_points) - len(unique_end_points)

    def error_calculation(self):
        """ Using the error formula C = n + 300 * k, it returns the calculated error. """
        return len(self.occupied_segments) + 300 * self.calculate_intersections()
