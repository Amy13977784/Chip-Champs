class Connection:
    """Class creates a connection by implementing their starting location (chip a) and
    their einding location (chip b), and a list of coordinates that the wire occupies.
    Method __init__ implements self.location, self.end_location and self.coor_llsit.
    Method add_coor adds a coordinate to self.coor_list --> adds a step decided by the 
    algorithm to the connection. 
    Method check_end checks if the connection has reached its end_location."""

    def __init__(self, start_location, end_location, gates):
        """Implements the starting location of the connections (the first gates, chip_a) in self.location,
        and the end destination (chip_b). It also implements all the already occuppied segment in the
        self.occupied_segments list."""

        # tuple coordinates
        self.start_location = start_location
        self.end_location = end_location
        self.gates = gates

        # add start coordinate to list
        self.coor_list = [self.start_location]

    def add_coor(self, coor):
        """Adds a coordinate (a taken step) to the coordinate list (route of the wire)."""
        self.coor_list.append(coor)

    def check_end(self):
        """Checks if the last coordinate in the list corresponds to the end location, if yes:
        the wire has reached its goal/end location --> returns True, if not: wire still has
        to take steps --> returns False."""
        return self.coor_list[-1] == self.end_location



   