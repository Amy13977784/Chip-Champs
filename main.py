# Visualisation of Chip & Circuit problem.
# running the code will give the current solution and the amount of error for that particular
# solution.
#
# Authors: Merel, Amy, Kyra

from classes import chip
import algorithm
import time
        
if __name__ == '__main__':
    gates_path = 'data/chip_0/print_0.csv'
    connections_path = 'data/chip_0/netlist_2.csv'

    for i in range(100):        
        my_chip = chip.Chip(gates_path, connections_path)

        algorithm.Random_algorithm(my_chip).all_connections()

        my_chip.plot_chip()
        cost = my_chip.error_calculation()
        print(f'The costs for this solution: {cost}')


