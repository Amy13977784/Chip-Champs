class Error:
    """ This class calculates the cost of the solution. """
    
    def __init__(self, chip):
        self.occupied_segments = chip.occupied_segments
        self.gates = chip.gates.values.tolist()

    def calculate_intersections(self):
        """
        Check if segment ends occur mulitple times in the occupied segments list. In other words,
        check if certain point in the grid are used twice or more.
        """
        end_points = []
        for segment in self.occupied_segments:
            if list(segment[1]) not in self.gates:
                end_points.append(segment[1])

        unique_end_points = set(end_points)

        return len(end_points) - len(unique_end_points)

    def error_calculation(self):
        return len(self.occupied_segments) + 300 * self.calculate_intersections()