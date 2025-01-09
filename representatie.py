# representatie van chips en circuits probleem.
#
# authors: de chip champs

import pandas as pd
import matplotlib.pyplot as plt

def plot_grid(connections_path, gates_path):
    gates = pd.read_csv(gates_path, index_col = 'chip')

    x_max = max(gates['x']) + 1
    y_max = max(gates['y']) + 1

    for line in range(1, x_max):
        plt.axvline(line, color = 'black', linewidth = 0.75)

    for line in range(1, y_max):
        plt.axhline(line, color = 'black', linewidth = 0.75)


    plot_connections(connections_path, gates)

    plt.plot(gates['x'], gates['y'], 'rs', markersize = 29 - max([x_max, y_max]))

    for index, row in gates.iterrows():
        plt.text(row['x'], row['y'], index, fontsize = 27 - max([x_max, y_max]), \
            horizontalalignment='center', verticalalignment='center_baseline')

    plt.xticks([])
    plt.yticks([])
    plt.xlim(0, x_max)
    plt.ylim(0, y_max)

    plt.show()


def plot_connections(connections_path, gates):
    connections = pd.read_csv(connections_path)
   
    for _, row in connections.iterrows():
        coor_a = gates.loc[row['chip_a']]
        coor_b = gates.loc[row['chip_b']]

        horizontal_steps = coor_b['x'] - coor_a['x']
        vertical_steps = coor_b['y'] - coor_a['y']
        
        plt.plot((coor_a['x'], coor_a['x'] + horizontal_steps, coor_a['x'] + horizontal_steps), (coor_a['y'], coor_a['y'], coor_a['y'] + vertical_steps), linewidth = 4, color='b')
    

    

gates_path = 'gates&netlists/chip_2/print_2.csv'
connections_path = 'gates&netlists/chip_2/netlist_7.csv'
plot_grid(connections_path, gates_path)


# To Do: kruisingen tussen draden vinden, hoe?