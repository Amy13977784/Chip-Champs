class Cost:
    """ This class calculates the cost of the current solution.
    The method __init__ stores the occupied segments in self.occupied_segments and stores the 
    coordinates of the gates in the chip to self.gates.
    The method calculate_intersections returns the amount of connection intersections on the chip. 
    The method error_calculation returns the amount of error of the solution."""
    
    def __init__(self, chip):
        """Stores the occupied segments from the initiated chip from chip class and stores the 
        coordinates of the gates.  """
        self.occupied_segments = chip.occupied_segments
        self.gates = chip.gates.values.tolist()

    def calculate_intersections(self):
        """Check if segment ends occur mulitple times in the occupied segments list. In other words,
        check if certain point in the grid are used twice or more."""
        end_points = []
        for segment in self.occupied_segments:

            # check if the segment end is not a gate/destination
            if list(segment[1]) not in self.gates:
                end_points.append(segment[1])

        unique_end_points = set(end_points)

        return len(end_points) - len(unique_end_points)

    def error_calculation(self):
        """ Using the error formula C = n + 300 * k, it returns the calculated error. """
        return len(self.occupied_segments) + 300 * self.calculate_intersections()