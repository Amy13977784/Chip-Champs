class Connection:
    """ 
    Class that contains all coordinates of the route from the start_location to the end_location 
    found by an algorithm.
    Method __init__ contains self.start_location, self.end_location, self_gates and self.coor_list.
    Method add_coor adds a coordinate to self.coor_list, adding a step to the connection. 
    Method check_end checks if the connection has reached its end_location. 
    """

    def __init__(self, start_location, end_location, gates, add_start=False):

        # tuples of coordinates
        self.start_location = start_location
        self.end_location = end_location

        # gate numbers in format: (start_gate, end_gate)
        self.gates = gates

        # will contain all the coordinates of the connection
        self.coor_list = []

        # will add the coordinates of the start_location to the coordinates list
        if add_start:
            self.add_coor(start_location)

    def add_coor(self, coordinate):
        """ Adds a coordinate (a taken step) to the coordinate list (route of the connection). """
        self.coor_list.append(coordinate)

    def check_end(self):
        """ Checks if the last coordinate in the list corresponds to the end location. Returns 
        True if the connection has reached its end location, returns False otherwise. """
        return self.coor_list[-1] == self.end_location



   