# Visualisation of Chip & Circuit problem.
# running the code will give the current solution and the amount of error for that particular
# solution. It also displays what coordinates belong to which connection/net. 
# In addition to this a csv.file of this output can be created (set save to True).
#
# Authors: Merel, Amy, Kyra

from classes import chip
from algorithms import random_algorithm, breadth_first, astar_algorithm

        
if __name__ == '__main__':
    chip_number = 0
    netlist = 3

    for i in range(1):
        my_chip = chip.Chip(chip_number, netlist)

        # ----- If the connections have to be ordered by gate or Manhattan distance -----
        my_chip.connection_order_by_gate()
        # my_chip.connection_order_by_distance()

        # ----- Random algorithm -----
        # validity = random_algorithm.Random_algorithm(my_chip).all_connections()

        # ----- Breadth first algorithm -----
        # breadth_first.BreadthFirst(my_chip).all_connections()

        # ----- A* algorithm -----
        astar_algorithm.Astar(my_chip).all_connections()

        my_chip.plot_chip()
        cost = my_chip.calculate_cost()
        print(f'The costs for this solution: {cost}')

        # output file: (cost, algorithm, iteration, validity), only add validity for the random algorithm
        my_chip.output_file(cost, 'astar', i)

    # ----- if we want to plot a solution from an earlier saved file -----
    # chip.Chip(chip_number, netlist).plot_solution(0, 'breadthfirst')


