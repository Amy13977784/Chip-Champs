from classes import connection as con
import copy
import random

class BreadthFirst:
    """
    Class implements the breadth first algorithm to find the shortest route between the start 
    and end gate/location of every connection.
    Method valid_step checks if a next step can be taken.
    Method next_steps takes the possible next steps of a route.
    Method run checks for the routes if they have reached the end gate or have to be extended. 
    Method all_connections finds the shortest route for all connections. '''
    """

    def __init__(self, chip):
        self.chip = chip

    def valid_step(self, coor_start, coor_end, connection):
        """ 
        Checks if a next step on a certain gridsegment can be taken, by checking if that segment is 
        not yet occupied, not out of bounds, not to a different gate and not a step backwards. 
        """
        # checks if the segment is already occupied
        segment_occupied = (coor_start, coor_end) in self.chip.occupied_segments or \
                        (coor_end, coor_start) in self.chip.occupied_segments

        # checks if coordinates are out of bounds
        out_of_bounds = any(coor < 0 for coor in coor_end) or coor_end[0] > self.chip.x_max or \
                        coor_end[1] > self.chip.y_max or coor_end[2] > self.chip.z_max

        # checks if coor_end is not any of the other gates
        valid_end = coor_end == connection.end_location or \
                    all(gate.coor != coor_end for gate in self.chip.gates.values())

        # checks if coor_end is not a step backwards
        not_previous_step = len(connection.coor_list) < 2 or coor_end != connection.coor_list[-2]

        # combines conditions
        if not segment_occupied and not out_of_bounds and valid_end and not_previous_step:
            return True

        return False


    def next_steps(self, connection):
        """ Creates all valid possible next steps and adds them to the list of routes. """

        # all possible next steps in format (axis, step) with axis: 0=x, 1=y & 2=z
        possible_steps = [(0, 1), (0, -1), (1, 1), (1, -1), (2, 1), (2, -1)]

        # shuffles the list so the next steps are added in different order, this can give different solutions
        random.shuffle(possible_steps)

        # the start location of the next step is the end location of the current route
        start_location = connection.coor_list[-1]

        # creates the new end location for every possible step
        for axis, step in possible_steps:
            end_location = list(start_location)
            end_location[axis] += step

            # if the next step is valid, adds this step to the current route and adds it to the list of routes
            if self.valid_step(start_location, tuple(end_location), connection):
                new_route = copy.deepcopy(connection)
                new_route.add_coor(tuple(end_location))
                self.routes.append(new_route)


    def run(self, start_location, end_location, gates):
        """ Runs the algorithm until one of the routes has reached the end gate. """

        self.routes = []

        # instigate routes with first possible steps from the start gate
        self.next_steps(con.Connection(start_location, end_location, gates))

        while self.routes:

            # gets the route from the list in the queu format
            route = self.routes.pop(0)

            # if the route has not reached the end gate yet, extend the route with all possible next steps
            if not route.check_end():
                self.next_steps(route)
            
            # the first route that reaches the end gate is the shortest route and is returned
            else:
                return route
        
        print('No route possible')


    def all_connections(self):
        """ Finds the shortest route for every connection. """

        for index, connection in enumerate(self.chip.connections):
            shortest_route = self.run(connection.start_location, connection.end_location, connection.gates)
            self.chip.connections[index] = shortest_route

            print('connection done')

            # adds all the used segments in the found route to the chip's occupied segments list
            for index in range(len(shortest_route.coor_list)):
                if index != len(shortest_route.coor_list) - 1:
                    self.chip.occupied_segments.append((shortest_route.coor_list[index], shortest_route.coor_list[index + 1]))
            
