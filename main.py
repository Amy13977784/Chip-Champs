# Visualisation of Chip & Circuit problem.
# running the code will give the current solution and the amount of error for that particular
# solution. It also displays what coordinates belong to which connection/net. 
# In addition to this a csv.file of this output can be created (set save to True).
#
# Authors: Merel, Amy, Kyra

from classes import chip
import algorithms.random_algorithm as random_algorithm
        
if __name__ == '__main__':
    chip_number = 0
    netlist = 1

    for i in range(5):        
        my_chip = chip.Chip(chip_number, netlist)

        validity = random_algorithm.Random_algorithm(my_chip).all_connections()

        my_chip.plot_chip()
        cost = my_chip.calculate_cost()
        print(f'The costs for this solution: {cost}')

        # save = True: a csv file containing the output is created.
        my_chip.output_file(i, chip_number, netlist, cost, validity, save=True)


