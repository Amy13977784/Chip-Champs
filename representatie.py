# representatie van chips en circuits probleem.
#
# authors: de chip champs

import pandas as pd
import matplotlib.pyplot as plt

def plot_grid(gates_path):
    gates = pd.read_csv(gates_path)

    x_max = max(gates['x']) + 1
    y_max = max(gates['y']) + 1

    for line in range(1, x_max):
        plt.axvline(line, color = 'black', linewidth = 0.75)

    for line in range(1, y_max):
        plt.axhline(line, color = 'black', linewidth = 0.75)

    plt.plot(gates['x'], gates['y'], 'rs', markersize = 29 - max([x_max, y_max]))

    for _, row in gates.iterrows():
        plt.text(row['x'], row['y'], row['chip'], fontsize = 27 - max([x_max, y_max]), \
            horizontalalignment='center', verticalalignment='center_baseline')

    plt.xticks([])
    plt.yticks([])
    plt.xlim(0, x_max)
    plt.ylim(0, y_max)

    plt.show()


plot_grid('gates&netlists/chip_1/print_1.csv')


# connecties plotted (in blauw) met behulp van coordinaten van gates die verbonden
# moeten worden (x-x y-y, zoiets)

# To Do:
# in functie zetten: voor elke input: voor elke chip moet het werken
# connecties eerste poging
