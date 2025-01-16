# Visualisation of Chip & Circuit problem.
# running the code will give the current solution and the amount of error for that particular
# solution. It also displays what coordinates belong to which connection/net.
#
# Authors: Merel, Amy, Kyra

from classes import chip
import random_algorithm
        
if __name__ == '__main__':
    chip_number = 0
    netlist = 1

    for i in range(5):        
        my_chip = chip.Chip(chip_number, netlist)

        random_algorithm.Random_algorithm(my_chip).all_connections()

        my_chip.plot_chip()
        cost = my_chip.calculate_cost()
        print(f'The costs for this solution: {cost}')
        my_chip.output_file(i, chip_number, netlist, cost, save=True)


