# Visualisation of Chip & Circuit problem.
# running the code will give the current solution and the amount of error for that particular
# solution.
#
# Authors: Merel, Amy, Kyra

from classes import class_Visualize_chip, class_Cost, class_Gates

if __name__ == '__main__':
    gates_path = 'data/chip_0/print_0.csv'
    connections_path = 'data/chip_0/netlist_1.csv'

    gates = class_Gates.Gates(gates_path).gates

    my_chip = class_Visualize_chip.Visualize_chip(gates, connections_path)
    my_chip.plot_grid()
    my_chip.plot_connections()
    my_chip.plot_gates()
    my_chip.show_plot()

    costs = class_Cost.Cost(my_chip)
    cost = costs.error_calculation()
    print(f'The costs for this solution: {cost}')
