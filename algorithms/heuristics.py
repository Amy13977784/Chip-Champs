import math

class Heuristics:
    """ Class orders the connections in the connections list by different heuristics.
    Method sort_and_return sorts and return the list by their given scores.
    Method order_by_gate scores the connections by how many total connections the gates have.
    Method order_by_distance orders the connections by the Manhattan distance. 
    Method order_by_location scores the connections by how far the gates are from the center. """

    def __init__(self, chip):
        self.chip = chip
        self.connections = chip.connections


    def sort_and_return(self, scored_connections, reversed):
        """ Sorts the list by scores and returns the newly ordered list of connections. """

        scored_connections.sort(key=lambda x: x[1], reverse=reversed)
        self.chip.connections = [self.connections[index] for index, _ in scored_connections]


    def order_by_gate(self):
        """ Orders the connections by gate scores. For each gate is counted how many connections they 
        have and each connection gets a score by adding the amount of connections each of the gates have.
        Connections with higher scores are classified as harder connections and will be placed first
        in the order. """

        gate_count = {}
        scored_connections = []

        # counts for every gate in how many connections they are involved
        for connection in self.connections:
            for gate in connection.gates:
                if gate not in gate_count:
                    gate_count[gate] = 0
                gate_count[gate] += 1

        # scores each connection by how many connections both gates have
        for index, connection in enumerate(self.connections):
            score = gate_count[connection.gates[0]] + gate_count[connection.gates[1]]
            scored_connections.append((index, score))
        
        self.sort_and_return(scored_connections, reversed = True)


    def order_by_distance(self):
        """ Orders the connections by the Manhattan distance. For every connection is the Manhatten distance
        between the start and end location calculated. The connections are ordered by distance and 
        the shorter distance connections are first in the order. """

        scored_connections = []

        for index, connection in enumerate(self.connections):

            # calculates the Manhattan distance between the start and end location
            distance = abs(connection.end_location[0] - connection.start_location[0]) + \
                        abs(connection.end_location[1] - connection.start_location[1])
            scored_connections.append((index, distance))
        
        self.sort_and_return(scored_connections, reversed = False)

    def order_by_location(self):
        """ Orders the connection by location on the grid. The location is based on how far away a gate is 
        from the center of the grid (layer 0). Connections with gates close to the center are first in order. """

        scored_connections = []

        # get the x and y coordinates of the center of the grid layer 0
        center_x = self.chip.x_max / 2
        center_y = self.chip.y_max / 2

        for index, connection in enumerate(self.connections):
            x_start, y_start, _ = connection.start_location
            x_end, y_end, _ = connection.end_location
            
            # determine the distance to the center for both gates with the pythagorean theorem
            score_start = math.sqrt((x_start - center_x) ** 2 + (y_start - center_y) ** 2)
            score_end = math.sqrt((x_end - center_x) ** 2 + (y_end - center_y) ** 2)

            total_score = score_start + score_end

            scored_connections.append((index, total_score))
        
        self.sort_and_return(scored_connections, reversed = False)
