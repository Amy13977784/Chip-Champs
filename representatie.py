# representatie van chips en circuits probleem.
#
# authors: de chip champs

import pandas as pd
import matplotlib.pyplot as plt
import random

def plot_grid(connections_path, gates_path):
    '''
    Function that plots a grid of correct dimension, the gates of the chip and their connections.
    '''
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


def x_step(coor_b, location):
    '''
    Lets a connection take a horizontal step.
    '''

    # check how to change x coordinate of connection to resemble x destination coordinate.
    if location['x'] > coor_b['x']:
        new_location = location['x'] - 1
    elif location['x'] < coor_b['x']:
        new_location = location['x'] + 1
    else:
        new_location = location['x'] + random.choice([-1, 1])

    return (location['x'], location['y']), (new_location, location['y'])


def y_step(coor_b, location):
    '''
    Lets a connection take a vertical step.
    '''

    # check how to change y coordinate of connection to resemble y destination coordinate.
    if location['y'] > coor_b['y']:
        new_location = location['y'] - 1
    elif location['y'] < coor_b['y']:
        new_location = location['y'] + 1
    else:
        new_location = location['y'] + random.choice([-1, 1])

    return (location['x'], location['y']), (location['x'], new_location)


def plot_connections(connections_path, gates):
    '''
    Function that 
    '''

    connections = pd.read_csv(connections_path)

    occupied_segments = []


    for _, row in connections.iterrows():
        coor_a = gates.loc[row['chip_a']]
        coor_b = gates.loc[row['chip_b']]

        location = coor_a.copy()

        while location['x'] != coor_b['x'] or location['y'] != coor_b['y']:
            while location['x'] != coor_b['x']:
                x_change = True
                segment_a, segment_b = x_step(coor_b, location)

                while (segment_a, segment_b) in occupied_segments or (segment_b, segment_a) in occupied_segments:
                    segment_a, segment_b = y_step(coor_b, location)
                    x_change = False

                occupied_segments.append((segment_a, segment_b))

                plt.plot((segment_a[0], segment_b[0]), (segment_a[1], segment_b[1]), linewidth = 4, color='b')

                if x_change:
                    location['x'] = segment_b[0]
                else:
                    location['y'] = segment_b[1]
                print('x')


            while location['y'] != coor_b['y']:
                y_change = True
                segment_a, segment_b = y_step(coor_b, location)

                while (segment_a, segment_b) in occupied_segments or (segment_b, segment_a) in occupied_segments:
                    segment_a, segment_b = x_step(coor_b, location)
                    y_change = False

                occupied_segments.append((segment_a, segment_b))

                plt.plot((segment_a[0], segment_b[0]), (segment_a[1], segment_b[1]), linewidth = 4, color='b')

                if y_change:
                    location['y'] = segment_b[1]
                else:
                    location['x'] = segment_b[0]
                print('y')

        print('connection done')

gates_path = 'gates&netlists/chip_0/print_0.csv'
connections_path = 'gates&netlists/chip_0/netlist_1.csv'
plot_grid(connections_path, gates_path)

# To Do: kruisingen tussen draden vinden, hoe?
# 3d plot om alle lagen te representeren
