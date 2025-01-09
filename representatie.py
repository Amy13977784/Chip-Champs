# representatie van chips en circuits probleem.
#
# authors: de chip champs

import pandas as pd
import matplotlib.pyplot as plt

# gates coordinaten importeren
gates = pd.read_csv('gates&netlists/gates&netlists/chip_0/print_0.csv')

# gates plotten in correcte formaat grid
for line in range(7):
    plt.axvline(line, color = 'black')
    plt.axhline(line, color = 'black')

plt.plot(gates['x'], gates['y'], 'rs', markersize = 18)

for index, row in gates.iterrows():
    plt.text(row[1]-0.08, row[2]-0.08, row[0], weight='bold', fontsize = 12)
plt.xticks([])
plt.yticks([])
plt.ylim(0, 6)
plt.xlim(0, 7)

plt.show()


# connecties plotted (in blauw) met behulp van coordinaten van gates die verbonden
# moeten worden (x-x y-y, zoiets)

# To Do:
# in functie zetten: voor elke input: voor elke chip moet het werken
# connecties eerste poging
