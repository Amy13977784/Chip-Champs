class Gate:
    """Class to manage the properties of the gates.
    The method __init__ creates self.gates (the coordinates for all the gates). 
    The method gate_location returns the location (coordinates) of a certain gate."""

    def __init__(self, gate):
        """creates self.gate: the coordinates of a gate"""
        self.gate = gate
        self.gates['z'] = 0

    def gate_location(self, chip):
        """Get the location of a specific gate and returns that location."""
        return self.gates.loc[chip]