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

    def plot_chip(self):
        """ Plots the grid, gates and connections (made by the algorithm) in a 3D plot. """
        
        plt.axes(projection='3d')
    
        # grid
        for x in range(1, self.x_max):
            plt.plot(x, [0, self.y_max], 0, color='black', linewidth=0.5)
        for y in range(1, self.y_max):
            plt.plot([0, self.x_max], y, 0, color='black', linewidth=0.5)

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

        if all(end_z == 0 for _, (_, _, end_z) in self.occupied_segments):
            ax.set_zlim(0, self.z_max)

        plt.show()

    def calculate_intersections(self):
        """ Check if segment ends occurs mulitple times in the occupied segments list. In other words,
        check if certain point in the grid are used twice or more. Also keeps track of coordinates where
        an intersections occurs. Function returns the amount of intersections. """
        
        end_points = []
        intersection_coors = [] 
        gates_coordinates = [gate.coor for gate in self.gates.values()]

        for _, end_coordinates in self.occupied_segments:

            # check if the segment end is not a gate/destination
            if end_coordinates not in gates_coordinates:
                if end_coordinates in end_points:
                    intersection_coors.append(end_coordinates)
                end_points.append(end_coordinates)
                
        unique_end_points = set(end_points)

        return len(end_points) - len(unique_end_points)

    def calculate_cost(self):
        """ Using the cost formula C = n + 300 * k, it returns the cost of the current solution. """
        return len(self.occupied_segments) + 300 * self.calculate_intersections()
    
    def create_output_file(self, cost, algorithm, file_number=0, validity='valid'):
        """ 
        Creates the output file, which contains the coordinates of every connection, which chip and 
        netlist, and the cost of the solution. The order of the connections corresponds to the netlist,
        regardless of the order in which the connections are made.
        """
 
        # output df with each connection on a row with format: (start gate, end gate) [coordinates in connection]
        df_output = pd.DataFrame([(connection.gates, connection.coor_list) for connection in self.connections], \
        columns=['net', 'wires']).set_index('net')

        # creates a df of the netlist to align the order of the connections with
        netlist_path = f'data/chip_{self.chip_number}/netlist_{self.netlist}.csv'
        df_netlist = pd.read_csv(netlist_path)
        
        # creates a 'net' column in the same format as the output df: (start gate, end gate)
        df_netlist['net'] = list(zip(df_netlist['chip_a'], df_netlist['chip_b']))

        # reorders the connections of the output df to the order of the netlist
        df_output = df_output.reindex(df_netlist['net'])

        # adds last row  whith informational data 
        df_output.loc[f'chip_{self.chip_number}_net_{self.netlist}'] = [[validity, cost]]
    	
        # creates output folder if it does not exist yet
        if not os.path.isdir("output"):
            os.makedirs("output")
        
        # saves the dataframe into a csv file
        df_output.to_csv(f'output/output_chip_{self.chip_number}_net_{self.netlist}_{algorithm}_{file_number}.csv')

    def plot_solution(self, file_number, algorithm):
        """
        Gets the details of a solutions and tries to find the file. If a file is found, adds the coordinates lists
        to the connections and plots the chip. 
        """
        file_path = f'output/output_chip_{self.chip_number}_net_{self.netlist}_{algorithm}_{file_number}.csv'
        
        try:
            df = pd.read_csv(file_path, index_col='net')

            # excludes the last row, which only contains informational data
            for index, (_, coordinate_list) in enumerate(df.iloc[:-1].iterrows()):
                coordinates = eval(coordinate_list['wires'])
                self.connections[index].coor_list = coordinates

            self.plot_chip()

        except:
            print('File not found')

    def load_solution(self, file_number, algorithm):
        """
        Gets an output file of a solution as input, creates the occupied_segments list and connections. 
        """
        
        file_path = f'output/output_chip_{self.chip_number}_net_{self.netlist}_{algorithm}_{file_number}.csv'
        
        try:
            df = pd.read_csv(file_path, index_col='net')

             # Reset the occupied segments to ensure only the segments form the new solution are reflected 
            self.occupied_segments.clear() 

            for index, (net, row) in enumerate(df.iloc[:-1].iterrows()):
                coordinates = eval(row['wires'])
                self.connections[index].coor_list = coordinates

                # Add segments to occupied_segments
                for i in range(len(coordinates) - 1):
                    segment = (tuple(coordinates[i]), tuple(coordinates[i + 1]))
                    self.occupied_segments.add(segment)

        except:
            print('File not found')

            
            
                