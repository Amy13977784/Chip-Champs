class Gate:
    """Class to manage the properties of the gates.
    The method __init__ creates self.gates, self., self.y, and self.z."""

    def __init__(self, coordinates):
        """creates self.gate: the coordinates of a gate"""
        self.x = coordinates['x']
        self.y = coordinates['y']
        self.z = 0
        self.coor = (self.x, self.y, self.z)