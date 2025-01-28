class Gate:
    """ 
    Class that holds the properties of a gate. Contains variables for the seperate coordinates 
    (self.x, self.y, self.z) and a tuple of coordinates (self.coor_list). 
    """

    def __init__(self, coordinates):
        self.x = coordinates['x']
        self.y = coordinates['y']
        self.z = 0

        self.coor = (self.x, self.y, self.z)