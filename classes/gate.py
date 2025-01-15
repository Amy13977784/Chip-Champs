class Gate:
    """Class to manage the properties of the gates.
    The method __init__ creates self.gates (the coordinates for all the gates). 
    The method gate_location returns the location (coordinates) of a certain gate."""

    def __init__(self, gate):
        """creates self.gate: the coordinates of a gate"""
        self.x = gate['x']
        self.y = gate['y']
        self.z = 0
        self.gate = tuple(self.x, self.y, self.z)