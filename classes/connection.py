import random

class Connection:
    """Class creates connections by implementing their starting location (chip a) and
    their einding location (chip b), and lets the connections take form by taking random steps in
    the right directions.
    Method __init__ implements self.location, self.end_location and self.occupied_segments."""

    def __init__(self, connection, gates, occupied_segments):
        """Implements the starting location of the connections (the first gates, chip_a) in self.location,
        and the end destination (chip_b). It also implements all the already occuppied segment in the
        self.occupied_segments list."""

        self.segments_list = []
        self.location = gates.loc[connection['chip_a']].copy()
        self.end_location = gates.loc[connection['chip_b']]
        self.gates = gates
        self.occupied_segments = occupied_segments
   