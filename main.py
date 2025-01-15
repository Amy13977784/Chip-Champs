# Visualisation of Chip & Circuit problem.
# running the code will give the current solution and the amount of error for that particular
# solution.
#
# Authors: Merel, Amy, Kyra

from classes import chip
        
if __name__ == '__main__':
    gates_path = 'data/chip_0/print_0.csv'
    connections_path = 'data/chip_0/netlist_3.csv'

    my_chip = chip.Chip(gates_path, connections_path)
    my_chip.plot_chip()
    cost = my_chip.error_calculation()
    print(f'The costs for this solution: {cost}')


