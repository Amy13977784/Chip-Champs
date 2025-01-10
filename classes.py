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


class Chip:
    """ This class contains the code for making the grid"""

    def __init__(self, gates_path):
        """
        Initialize with file paths for gates and connections
        """
        self.gates = pd.read_csv(gates_path, index_col='chip')
        self.x_max = max(self.gates['x']) + 1
        self.y_max = max(self.gates['y']) + 1

    def draw_grid(self):
        """
        Draw the grid with vertical and horizontal lines
        """
        for line in range(1, self.x_max):
            plt.axvline(line, color='black', linewidth=0.75)

        for line in range(1, self.y_max):
            plt.axhline(line, color='black', linewidth=0.75)

    def plot_connections(self):
        Connection.__init__()


    def plot_gates(self):
        """
        Plot the gates on the grid
        """
        plt.plot(self.gates['x'], self.gates['y'], 'rs', markersize=29 - max([self.x_max, self.y_max]))

        for index, row in self.gates.iterrows():
            plt.text(row['x'], row['y'], index, fontsize=27 - max([self.x_max, self.y_max]),
                     horizontalalignment='center', verticalalignment='center_baseline')

    def show_plot(self):
        """
        Show the grid (without the conncections yet)
        """
        plt.xticks([])
        plt.yticks([])
        plt.xlim(0, self.x_max)
        plt.ylim(0, self.y_max)
        plt.show()

if __name__ == '__main__':
    my_chip = Chip('gates&netlists/chip_0/print_0.csv')
    my_chip.draw_grid()
    my_chip.plot_connections()
    my_chip.plot_gates()
    my_chip.show_plot()
