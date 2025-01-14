import pandas as pd

class Gates:
    """Class to manage the properties of the gates.
    The method __init__ creates self.gates (the coordinates for all the gates). 
    The method gate_location returns the location (coordinates) of a certain gate."""

    def __init__(self, gates_path):
        """Reads in  the coordinates of the gates and stores it in self.gates."""
        self.gates = pd.read_csv(gates_path, index_col='chip')

    def gate_location(self, chip):
        """Get the location of a specific gate and returns that location."""
        return self.gates.loc[chip]