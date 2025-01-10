import pandas as pd

class Gates:
    """Class to manage the properties of the gates."""

    def __init__(self, gates_path):
        self.gates = pd.read_csv(gates_path, index_col='chip')

    def gate_location(self, chip):
        """Get the location of a specific gate."""
        return self.gates.loc[chip]