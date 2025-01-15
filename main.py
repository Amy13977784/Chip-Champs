# Visualisation of Chip & Circuit problem.
# running the code will give the current solution and the amount of error for that particular
# solution.
#
# Authors: Merel, Amy, Kyra

from classes import chip
import random_algorithm
        
if __name__ == '__main__':
    gates_path = 'data/chip_0/print_0.csv'
    connections_path = 'data/chip_0/netlist_1.csv'

    for i in range(5):        
        my_chip = chip.Chip(gates_path, connections_path)

        random_algorithm.Random_algorithm(my_chip).all_connections()

        my_chip.plot_chip()
        cost = my_chip.calculate_cost()
        print(f'The costs for this solution: {cost}')


