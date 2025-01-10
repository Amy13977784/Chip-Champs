class Gates:
    """Class to manage the properties of the gates."""

    def __init__(self, gates_path):
        self.gates = pd.read_csv(gates_path, index_col='chip')

    def get_gate_location(self, chip):
        """Get the location of a specific gate."""
        return self.gates.loc[chip]

    def get_max_coordinates(self):
        """Get the maximum x and y values for grid dimensions."""
        return max(self.gates['x']) + 1, max(self.gates['y']) + 1