import pandas as pd
import matplotlib.pyplot as plt
import os

from classes import connection, gate

class Chip:
    """Class that implements a chip and all its properties (gates, grid, connections).
    Method __init__ creates self.occupied_segments, self.gates, self.connections, self.x_max, 
      self.y_max, and self.z_max.
    Method gates_dict creates a dictionary in the form; gate numberss: Gate class instance.
    Method connections_list creates a list. Every elements contains a Connection class instance.
    Method plot_chip, plots the elements of the chip.
    Method calculate_intersections calculated how many wires cross in the solution provided by the
    algorithm.
    Method calculate cost uses a formula to return the cost of the solution.
    Method output_file creates the an csv_file containing the results from the solution."""
    
    def __init__(self, chip_number, netlist):
        """ This method initiates the occupied segments list of that contain the segments used by
         the connections. It also creates a dictionary with the gates (key = number of gate, value =
         Gate class object) and a list of connections (coordinates of the 2 gates that need to 
         be connected). It also creates the bounds of the grid (self.x_max, self.y_max, self.z_max). """
        
        self.occupied_segments = []

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

            connections.append(connection.Connection(start_location, end_location))

        return connections

    def plot_chip(self):
        """ Plots the grid, gates and connections (made by the algorithm) in a 3D plot. """
        
        plt.axes(projection='3d')
    
        # grid
        for x in range(1, self.x_max):
            plt.plot(x, [0, self.y_max], 0, color='black', linewidth=0.5)
        for y in range(1, self.y_max):
            plt.plot([0, self.x_max], y, 0, color='black', linewidth=0.5)

        # connections
        for segment in self.occupied_segments:
            plt.plot((segment[0][0], segment[1][0]), (segment[0][1], segment[1][1]), (segment[0][2], segment[1][2]), linewidth = 3, color='b')

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
        for segment in self.occupied_segments:

            # check if the segment end is not a gate/destination
            if list(segment[1]) not in self.gates.values():
                end_points.append(segment[1])

        unique_end_points = set(end_points)

        return len(end_points) - len(unique_end_points)

    def calculate_cost(self):
        """ Using the cost formula C = n + 300 * k, it returns the cost of the current solution. """
        return len(self.occupied_segments) + 300 * self.calculate_intersections()
    
    def output_file(self, file_number, chip_number, netlist, cost, validity, save=True):
        """ Creates an output file, in which the coordinates of every connection, what chip, 
        and the error for the solution is shown. """

        # create dataframe 
        df_output = pd.DataFrame(columns = ['net', 'wires'])
    	
        for connection in self.connections:
            
            # recreating the netlist
            for gate_number_key, gate in self.gates.items():

                # retrieves the number of the gate that resembles the start and end coordinate (gate)
                if gate.coor == connection.start_location:
                    start_gate = gate_number_key
                elif gate.coor == connection.end_location:
                    end_gate = gate_number_key

            # row in df in following format: (start gate, end gate) [coordinates in connection]
            df_output.loc[len(df_output)] = [(start_gate, end_gate), connection.coor_list]

        # last row shows which chip, which netlist, and the cost of the solution 
        df_output.loc[len(df_output)] = [f'chip_{chip_number}_net_{netlist}', [validity, cost]]
        
        df_output.set_index('net', inplace=True)

        print(df_output, '\n')
    	
        # if wanting to save output to csv.file
        if save:

            # create output folder if it does not exist yet
            if not os.path.isdir("output"):
                os.makedirs("output")
            
            df_output.to_csv(f'output/output_{file_number}.csv')

