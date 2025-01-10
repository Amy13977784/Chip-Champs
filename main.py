import pandas as pd
import matplotlib.pyplot as plt
import random
import class_Visualize_chip


if __name__ == '__main__':
    gates_path = 'gates&netlists/chip_0/print_0.csv'
    connections_path = 'gates&netlists/chip_0/netlist_1.csv'

    my_chip = Visualize_chip(gates_path, connections_path)
    my_chip.plot_grid()
    my_chip.plot_connections()
    my_chip.plot_gates()
    my_chip.show_plot()

    costs = Error(my_chip)
    cost = costs.error_calculation()
    print(f'The costs for this solution: {cost}')
