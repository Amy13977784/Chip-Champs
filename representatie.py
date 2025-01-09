# representatie van chips en circuits probleem.
#
# authors: de chip champs

import pandas as pd
import matplotlib.pyplot as plt

def grid(chip_path):

    # gates coordinaten importeren
    gates = pd.read_csv(chip_path)

    max_x = max(gates['x']) + 1
    max_y = max(gates['y']) + 1

    # gates plotten in correcte formaat grid
    for line in range(max_x):
        plt.axvline(line, color = 'black')

    for line in range(max_y):
        plt.axhline(line, color = 'black')

    plt.plot(gates['x'], gates['y'], 'rs', markersize = 18)

    for index, row in gates.iterrows():
        plt.text(row[1]-0.3, row[2]-0.1, row[0], weight='bold', fontsize = 12)
    
    plt.xticks([])
    plt.yticks([])
    plt.ylim(0, max_y)
    plt.xlim(0, max_x)

    plt.show()

grid('gates&netlists/chip_1/print_1.csv')

# connecties plotted (in blauw) met behulp van coordinaten van gates die verbonden
# moeten worden (x-x y-y, zoiets)

# To Do:
# in functie zetten: voor elke input: voor elke chip moet het werken
# connecties eerste poging



# connecties plotted (in blauw) met behulp van coordinaten van gates die verbonden
# moeten worden (x-x y-y, zoiets)

# To Do:
# in functie zetten: voor elke input: voor elke chip moet het werken
# connecties eerste poging

