class Connection:
    """Class creates connections by implementing their starting location (chip a) and
    their einding location (chip b), and lets the connections take form by taking random steps in
    the right directions.
    Method __init__ implements self.location, self.end_location and self.occupied_segments."""

    def __init__(self, start, end):
        """Implements the starting location of the connections (the first gates, chip_a) in self.location,
        and the end destination (chip_b). It also implements all the already occuppied segment in the
        self.occupied_segments list."""

        # tuple coordinates
        self.start_location = start
        self.end_location = end

        # add start coordinate to list
        self.coor_list = [self.start_location]

    def add_coor(self, coor):
        self.coor_list.append(coor)

    def check_end(self):
        return self.coor_list[-1] == self.end_location



   