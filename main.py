import pandas as pd
import matplotlib.pyplot as plt
import random

from classes import class_Visualize_chip
from classes import class_Step
from classes import class_Cost
from classes import class_Gates
from classes import class_Connection

if __name__ == '__main__':
    gates_path = 'gates&netlists/chip_0/print_0.csv'
    connections_path = 'gates&netlists/chip_0/netlist_1.csv'

    gates = class_Gates.Gates(gates_path)

    my_chip = class_Vizualise_chip.Visualize_chip(gates, connections_path)
    my_chip.plot_grid()
    my_chip.plot_connections()
    my_chip.plot_gates()
    my_chip.show_plot()

    costs = class_Cost.Cost(my_chip)
    cost = costs.error_calculation()
    print(f'The costs for this solution: {cost}')
