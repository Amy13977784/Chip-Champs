class Visualize_chip:
    """ This class contains the code for making the grid. """

    def __init__(self, gates, connections_path):
        self.gates = gates
        self.connections = pd.read_csv(connections_path)

        self.x_max = max(self.gates['x']) + 1
        self.y_max = max(self.gates['y']) + 1

        self.occupied_segments = []

    def plot_grid(self):
        """ Plot the grid with vertical and horizontal lines. """
        for line in range(1, self.x_max):
            plt.axvline(line, color='black', linewidth=0.75)

        for line in range(1, self.y_max):
            plt.axhline(line, color='black', linewidth=0.75)

    def plot_connections(self):
        """ Plot the connections in the connections list. """
        for _, connection in self.connections.iterrows():
            Connection(connection, self.gates, self.occupied_segments).make_connection()

    def plot_gates(self):
        """ Plot the gates on the grid. """
        plt.plot(self.gates.gates['x'], self.gates.gates['y'], 'rs', markersize=29 - max([self.x_max, self.y_max]))

        for index, row in self.gates.iterrows():
            plt.text(row['x'], row['y'], index, fontsize=27 - max([self.x_max, self.y_max]),
                     horizontalalignment='center', verticalalignment='center_baseline')

    def show_plot(self):
        """ Adjust the layout and show the grid. """
        plt.xticks([])
        plt.yticks([])
        plt.xlim(0, self.x_max)
        plt.ylim(0, self.y_max)
        plt.show()


        

