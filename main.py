# Visualisation of Chip & Circuit problem.
# running the code will give the current solution and the amount of error for that particular
# solution.
#
# Authors: Merel, Amy, Kyra

from classes import visualize_chip, cost, gates

if __name__ == '__main__':
    gates_path = 'data/chip_0/print_0.csv'
    connections_path = 'data/chip_0/netlist_3.csv'

    gates = gates.Gates(gates_path).gates

    my_chip = visualize_chip.Visualize_chip(gates, connections_path)
    my_chip.plot_grid()
    my_chip.plot_connections()
    my_chip.plot_gates()
    my_chip.show_plot()

    costs = cost.Cost(my_chip)
    cost = costs.error_calculation()
    print(f'The costs for this solution: {cost}')
