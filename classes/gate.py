class Gate:
    """Class to manage the properties of the gates.
    The method __init__ creates self.gates, self., self.y, and self.z."""

    def __init__(self, gate):
        """creates self.gate: the coordinates of a gate"""
        self.x = gate['x']
        self.y = gate['y']
        self.z = 0
        self.gate = [self.x, self.y, self.z]