import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap
import os

from classes import connection, gate

class Chip:
    """ Class that implements a chip and all its properties (gates, grid, connections).
    Method __init__ creates self.occupied_segments, self.gates, self.connections, self.x_max, 
      self.y_max, and self.z_max.
    Method gates_dict creates a dictionary in the form; gate numbers: Gate class instance.
    Method connections_list creates a list. Every elements contains a Connection class instance.
    Method plot_chip, plots the elements of the chip.
    Method calculate_intersections calculated how many wires cross in the solution provided by the
    algorithm.
    Method calculate cost uses a formula to return the cost of the solution.
    Method output_file creates the an csv_file containing the results from the solution. """
    
    def __init__(self, chip_number, netlist):
        """ This method initiates the occupied segments list that will contain the segments used by
         the connections. It also creates a dictionary with the gates (key = number of gate, value =
         Gate class object) and a list of connections (coordinates of the 2 gates that need to 
         be connected). It also creates the bounds of the grid (self.x_max, self.y_max, self.z_max). """
        
        self.chip_number = chip_number
        self.netlist = netlist
        
        self.occupied_segments = set()

        self.gates = self.gates_dict(chip_number)
        self.connections = self.connections_list(chip_number, netlist)

        self.x_max = max(gate.x for gate in self.gates.values()) + 1
        self.y_max = max(gate.y for gate in self.gates.values()) + 1
        self.z_max = 7

    def gates_dict(self, chip_number):
        """ Reads in the coordinates of a certain chip. It returns a dictionary in which
         the number of the gate is a key and a Gate class object is the value. """

        gates = {}

        gates_path = f'data/chip_{chip_number}/print_{chip_number}.csv'
        df_gates = pd.read_csv(gates_path, index_col='chip')

        for index, coordinates in df_gates.iterrows():

            # create instance of the Gate class
            gates[index] = gate.Gate(coordinates)
            
        return gates

    def connections_list(self, chip_number, netlist):
        """ Reads in the connections (gates to be connected). By looking for the keys with the 
        number of the start and end gate in the gates dictionary, we can obtain the starting
        and ending coordinates of the connections, use them to create a Connection class instance, 
        and put those instances in a list. This list is returned. """   

        connections = []

        connections_path = f'data/chip_{chip_number}/netlist_{netlist}.csv'
        df_connections = pd.read_csv(connections_path)

        for _, con in df_connections.iterrows():
            
            # use gate dictionary to obtain start and end coordinates
            start_location = self.gates[con['chip_a']].coor
            end_location = self.gates[con['chip_b']].coor
            gates = (con['chip_a'], con['chip_b'])

            connections.append(connection.Connection(start_location, end_location, gates))

        return connections
    
    def connection_order_by_gate(self):
        
        gate_count = {}
        sorted_connections = []

        for connection in self.connections:
            for gate in connection.gates:
                if gate not in gate_count:
                    gate_count[gate] = 0
                gate_count[gate] += 1

        for index, connection in enumerate(self.connections):
            score = gate_count[connection.gates[0]] + gate_count[connection.gates[1]]
            sorted_connections.append((index, score))
        
        sorted_connections.sort(key=lambda x: x[1], reverse=True)
        self.connections = [self.connections[index] for index,_ in sorted_connections]

        print(sorted_connections)

    def connection_order_by_distance(self):
        
        sorted_connections = []

        for index, connection in enumerate(self.connections):
            distance = abs(connection.end_location[0] - connection.start_location[0]) + \
                abs(connection.end_location[1] - connection.start_location[1])
            sorted_connections.append((index, distance))
        
        sorted_connections.sort(key=lambda x: x[1])
        self.connections = [self.connections[con[0]] for con in sorted_connections]

    def plot_chip(self):
        """ Plots the grid, gates and connections (made by the algorithm) in a 3D plot. """
        
        plt.axes(projection='3d')
    
        # grid
        for x in range(1, self.x_max):
            plt.plot(x, [0, self.y_max], 0, color='black', linewidth=0.5)
        for y in range(1, self.y_max):
            plt.plot([0, self.x_max], y, 0, color='black', linewidth=0.5)

        #colors = ['blue', 'green', 'magenta', 'yellow', 'chocolate', 'purple', 'orange', 'lime', 'gray', 'cyan']
        colors = get_cmap('tab20')

        # connections
        for connection_index, connection in enumerate(self.connections):
            for index in range(len(connection.coor_list)):
                if index != len(connection.coor_list) - 1:
                    plt.plot((connection.coor_list[index][0], connection.coor_list[index + 1][0]), \
                            (connection.coor_list[index][1], connection.coor_list[index + 1][1]), \
                            (connection.coor_list[index][2], connection.coor_list[index + 1][2]), \
                                linewidth = 2, color = colors(connection_index / 19))


        # get the current axis
        ax = plt.gca() 

        # gates
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
        """ Check if segment ends occurs mulitple times in the occupied segments list. In other words,
        check if certain point in the grid are used twice or more. Function returns the amount of
        intersections. """
        
        end_points = []
        gates_coordinates = [gate.coor for gate in self.gates.values()]

        for _, end_coordinates in self.occupied_segments:

            # check if the segment end is not a gate/destination
            if end_coordinates not in gates_coordinates:
                end_points.append(end_coordinates)

        unique_end_points = set(end_points)

        return len(end_points) - len(unique_end_points)

    def calculate_cost(self):
        """ Using the cost formula C = n + 300 * k, it returns the cost of the current solution. """
        return len(self.occupied_segments) + 300 * self.calculate_intersections()
    
    def output_file(self, cost, algorithm, file_number, validity='valid'):
        """ Creates an output file, which contains the coordinates of every connection, which chip and 
        netlist, and the cost of the solution. """

        # creates dataframe 
        df_output = pd.DataFrame(columns = ['net', 'wires'])
    	
        for connection in self.connections:
        
            # row in df in following format: (start gate, end gate) [coordinates in connection]
            df_output.loc[len(df_output)] = [connection.gates, connection.coor_list]

        df_output.set_index('net', inplace=True)

        connections_path = f'data/chip_{self.chip_number}/netlist_{self.netlist}.csv'
        df_connections = pd.read_csv(connections_path)
        df_connections['net'] = None

        for index, con in df_connections.iterrows():
            df_connections.at[index, 'net'] = (con['chip_a'], con['chip_b'])

        df_connections.set_index('net', inplace=True)

        df_output = df_output.reindex(df_connections.index)

        # last row shows which chip, which netlist, if the solution is valid and the cost of the solution 
        df_output.loc[f'chip_{self.chip_number}_net_{self.netlist}'] = [[validity, cost]]

        print(df_output, '\n')
    	
        # creates output folder if it does not exist yet
        if not os.path.isdir("output"):
            os.makedirs("output")
        
        # saves the dataframe into a csv file
        df_output.to_csv(f'output/output_chip_{self.chip_number}_net_{self.netlist}_{algorithm}_{file_number}.csv')

    def plot_solution(self, file_number, algorithm):
        """
        Gets an output file of a solution as input, creates the occupied segments list and 
        """
        file_path = f'output/output_chip_{self.chip_number}_net_{self.netlist}_{algorithm}_{file_number}.csv'
        
        try:
            df = pd.read_csv(file_path, index_col='net')
            print(df)

            for index, coordinate_list in enumerate(df.iloc[:-1].iterrows()):
                coordinates = eval(coordinate_list[1]['wires'])
                self.connections[index].coor_list = coordinates

            self.plot_chip()

        except:
            print('File not found')
            