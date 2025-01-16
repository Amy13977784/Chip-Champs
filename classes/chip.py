import pandas as pd
import matplotlib.pyplot as plt

from classes import connection, gate

class Chip:
    def __init__(self, gates_path, connections_path):

        self.occupied_segments = []

        self.gates = self.gates_dict(gates_path)
        self.connections = self.connections_list(connections_path)

        self.x_max = max(gate.x for gate in self.gates.values()) + 1
        self.y_max = max(gate.y for gate in self.gates.values()) + 1
        self.z_max = 7

    def gates_dict(self, gates_path):
        
        gates = {}
        df_gates = pd.read_csv(gates_path, index_col='chip')

        for index, coordinates in df_gates.iterrows():
            gates[index] = gate.Gate(coordinates)
            
        return gates

    def connections_list(self, connections_path):
        """ Plot the connections in the connections list. """   

        connections = []
        df_connections = pd.read_csv(connections_path)

        for _, con in df_connections.iterrows():
            start_location = self.gates[con['chip_a']].coor
            end_location = self.gates[con['chip_b']].coor
            connections.append(connection.Connection(start_location, end_location))

        return connections

    def plot_chip(self):
        
        plt.axes(projection='3d')
    
        for x in range(1, self.x_max):
            plt.plot(x, [0, self.y_max], 0, color='black', linewidth=0.5)
        for y in range(1, self.y_max):
            plt.plot([0, self.x_max], y, 0, color='black', linewidth=0.5)

        for segment in self.occupied_segments:
            plt.plot((segment[0][0], segment[1][0]), (segment[0][1], segment[1][1]), (segment[0][2], segment[1][2]), linewidth = 3, color='b')

        ax = plt.gca() # get the current axis

        for number, gate in self.gates.items():
            plt.plot(gate.x, gate.y, gate.z, 'rD', markersize=20 - max([self.x_max, self.y_max]))
            ax.text(gate.x, gate.y, gate.z, number, fontsize=20 - max([self.x_max, self.y_max]),
                     horizontalalignment='center', verticalalignment='center_baseline')

        # remove axes values
        plt.xticks([])
        plt.yticks([])

        # set grid bounds
        plt.xlim(0, self.x_max)
        plt.ylim(0, self.y_max)
        ax.set_zlim(0, self.z_max)

        plt.show()

    def calculate_intersections(self):
        """Check if segment ends occur mulitple times in the occupied segments list. In other words,
        check if certain point in the grid are used twice or more."""
        end_points = []
        for segment in self.occupied_segments:

            # check if the segment end is not a gate/destination
            if list(segment[1]) not in self.gates.values():
                end_points.append(segment[1])

        unique_end_points = set(end_points)

        return len(end_points) - len(unique_end_points)

    def calculate_cost(self):
        """ Using the error formula C = n + 300 * k, it returns the calculated error. """
        return len(self.occupied_segments) + 300 * self.calculate_intersections()
    
    def output(self, filenumber):
        df_output = pd.DataFrame(columns = ['net', 'wires'])

        for connection in self.connections:
 
            for gate_number_key, gate in self.gates.items():
                if gate.coor == connection.start_location:
                    start_gate = gate_number_key
                elif gate.coor == connection.end_location:
                    end_gate = gate_number_key

            row = pd.DataFrame({'net': [(start_gate, end_gate)], 'wires': [connection.coor_list]})
            df_output = pd.concat([df_output, row])

        print(df_output)

        df_output.to_csv(f'output/output_{filenumber}.csv', index=False)
