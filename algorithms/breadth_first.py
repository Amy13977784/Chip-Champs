from classes import connection as con
import copy
import random

class BreadthFirst:
    """
    Class implements the breadth first algorithm to find the shortest route between the start 
    and end gate/location of every connection, possibly with beam search.
    Method valid_step checks if a next step can be taken.
    Method select_best_steps selects the beam amount of next steps with the shortest distance to the end location.
    Method next_steps extends the route with the valid next steps.
    Method run checks for the routes if they have reached the end gate or have to be extended. 
    Method all_connections applies the algorithm to find the shortest route to all connections.
    """

    def __init__(self, chip, beam=None):
        self.chip = chip
        self.beam = beam


    def valid_step(self, coor_start, coor_end, connection):
        """ 
        Checks if a next step on a certain gridsegment can be taken, by checking if that segment is 
        not already occupied, not out of bounds, not to a different gate and not a step backwards. 
        """
        # checks if the segment is not already occupied
        segment_free = (coor_start, coor_end) not in self.chip.occupied_segments and \
                        (coor_end, coor_start) not in self.chip.occupied_segments

        # checks if coordinates are not out of the grid bounds
        inside_grid = all(coor >= 0 for coor in coor_end) and coor_end[0] <= self.chip.x_max and \
                        coor_end[1] <= self.chip.y_max and coor_end[2] <= self.chip.z_max

        # checks if the segment does not end at another gate, by checking if coor_end is not any of the other gates
        not_different_gate = all(gate.coor != coor_end for gate in self.chip.gates.values()) or \
                        coor_end == connection.end_location

        # checks if coor_end is not a step backwards
        not_previous_step = len(connection.coor_list) < 2 or coor_end != connection.coor_list[-2]

        # combines conditions to check if the step is valid
        return segment_free and inside_grid and not_different_gate and not_previous_step


    def select_best_steps(self, next_steps, route):
        """ Selects the beam amount of steps that bring the route closer to the end location. """

        distance_steps = []

        for step in next_steps:

            # calculates the Manhattan distance
            distance = abs(route.end_location[0] - step[0]) + abs(route.end_location[1] - step[1])
            distance_steps.append((step, distance))
        
        # sorts the steps from shortest to longest distance to the end_location
        steps_sorted = sorted(distance_steps, key=lambda x: x[1])

        # returns the first beam amount of steps
        return [step for step, _ in steps_sorted[:self.beam]]


    def next_steps(self, route):
        """ 
        Creates all valid possible next steps, finds the beam amount of best steps and adds them to the list of 
        routes. The best steps are the steps from which the end points are closest to the end point, 
        calcuated with the Manhattan distance.
        """

        # all possible next steps in format (axis, direction) with axis: 0=x, 1=y & 2=z
        possible_steps = [(0, 1), (0, -1), (1, 1), (1, -1), (2, 1), (2, -1)]

        # shuffles the list so the next steps are added in different order, this can give different solutions
        random.shuffle(possible_steps)

        # for the route with every possible valid next step
        valid_next_steps = []

        # the start location of the next step is the end location of the current route
        start_location = route.coor_list[-1]

        # creates the new end location for every possible step
        for axis, step in possible_steps:
            end_location = list(start_location)
            end_location[axis] += step

            # checks if this next step is valid
            if self.valid_step(start_location, tuple(end_location), route):
                valid_next_steps.append(end_location)
        
        # if beam search present, selects the best beam amount of next step, based on the shortest new distance to the end gate
        if self.beam and len(valid_next_steps) > self.beam:
            valid_next_steps = self.select_best_steps(valid_next_steps, route)

        # adds the extended routes to the possible routes list
        for step in valid_next_steps:
            new_route = copy.deepcopy(route)
            new_route.add_coor(tuple(step))
            self.routes.append(new_route)


    def run(self, start_location, end_location, gates):
        """ Runs the algorithm until one of the routes has reached the end gate. """

        self.routes = []

        # instigates routes with first possible steps from the start gate
        self.next_steps(con.Connection(start_location, end_location, gates, add_start=True))

        while self.routes:

            # gets the route from the list in the queue format
            route = self.routes.pop(0)

            # if the route has not reached the end gate yet, extends the route with possible next steps
            if not route.check_end():
                self.next_steps(route)
            
            # the first route that reaches the end gate is the shortest route and is returned
            else:
                return route
        
        print('No route possible')


    def all_connections(self):
        """ Finds the shortest route for every connection. """

        for index, connection in enumerate(self.chip.connections):

            # applies the algorithm to find the shortest route for this connection
            shortest_route = self.run(connection.start_location, connection.end_location, connection.gates)
            self.chip.connections[index] = shortest_route

            # adds all the used segments in the found route to the chip's occupied segments list
            for segment in zip(shortest_route.coor_list, shortest_route.coor_list[1:]):
                self.chip.occupied_segments.add(segment)

            
