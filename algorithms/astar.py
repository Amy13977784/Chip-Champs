import copy
from operator import attrgetter

class Astar:
    """ Class implements the A* algorithm to form the connections between a starting point (start_coor)
    and an ending point (end_coor).
    Method __init__ initiates the chip,
    Method make_connection is the A* algorithm,
    Method distance_g calculates the g value for a node,
    Method distance_h calculates the h value for a node,
    Method cost_f calculates the f values for a node,
    Method valid_child checks if a child can be put into the open list,
    Method penalties adds to a child nodes' f value according to certain restrictions. """

    def __init__(self, chip, heuristics=[], intersections_penalty=5):

        self.chip = chip
        self.penalties = heuristics
        self.intersections_penalty = intersections_penalty

        # all the possible directions the connection can take at a node
        self.directions = [(1,0,0), (-1,0,0), (0,1,0), (0,-1,0), (0,0,1), (0,0,-1)]

        # all nodes that surround gates in a list (used in heuristics() method)
        self.adjoining_gates = []
        for gate in self.chip.gates.values():
            for direction in self.directions:
                self.adjoining_gates.append((gate.coor[0] + direction[0], gate.coor[1] + direction[1], gate.coor[2] + direction[2]))


    def all_connections(self):
        """ Loops over every connection to let them form using the make_connection() method. 
        It returns if the connections are valid or not. """

        # connection counter (to keep track of process in terminal)
        self.counter = 0

        # form each connection with there respective properties
        for connection in self.chip.connections:
            self.counter += 1
            self.start_node = Node(connection.start_location, None)
            self.end_node = Node(connection.end_location, None)
            self.connection = connection
            self.make_connection()

        # check if connections are complete and thus valid
        for connection in self.chip.connections:
            if connection.coor_list == []:
                return 'invalid'
        return 'valid'
    
    def make_connection(self):
        """ Makes a connection according to the A* algorithm. It will try to make the shortest route
        possible while complying to certain restrictions (from the valid_child() method). This method 
        adds to the final path that belong to this connection, by updating its coor_list. It returns
        a printstatement that indicates if a path was found or not. Only if a path is found the coor_list
        are updated. """
        
        open_list = []
        self.closed_list = []

        open_list.append(self.start_node)

        # while the end node has not been reached or too many nodes to be investigated
        while open_list and len(open_list) < 10000:

            # get current node --> node with the lowest f value
            self.current_node = min(open_list, key=attrgetter('f'))

            # # if f value too high
            # if self.current_node.f > 100:
                # return print(f'f value too high')
   
            open_list.pop(open_list.index(self.current_node))
            self.closed_list.append(self.current_node)

            # if end node has been reached
            if self.current_node.location == self.end_node.location:
                current = self.current_node

                # until the starting node has been reached (its parent None) --> backtrack to find paths
                while current.parent != None:

                    self.connection.add_coor(current.location)
                    self.chip.occupied_segments.add((current.location, current.parent.location))
                    current = current.parent

                self.connection.add_coor(self.start_node.location)

                # put list in corrrect order
                self.connection.coor_list.reverse()

                return print(f'path {self.counter}/{len(self.chip.connections)} found! :) :) :) {self.connection.coor_list}')

            else: 
                children = []

                #  generate list of child nodes
                for direction in self.directions:
                    child_node_location = (self.current_node.location[0] + direction[0], self.current_node.location[1] + direction[1], self.current_node.location[2] + direction[2])
                    children.append(Node(child_node_location, self.current_node))

                for child in children:
                    
                    # function to check if child is not a valid step:
                    if self.valid_child(child) == False:

                        # if not valid --> on to next child
                        continue
                
                    else:
                        child.g = self.distance_g(child)
                        child.h = self.distance_h(child)
                        child.f = self.cost_f(child.g, child.h)
                    
                        # check if already in open list
                        if any(child.location == open_node.location and child.g > open_node.g for open_node in open_list):
                            continue

                        # give child node necassary penalties
                        self.heuristics(child, self.penalties)

                        open_list.append(child)

        print('No path found :( or open list too big')
        return None

    def distance_g(self, node):
        """ Returns the distance from the current node to the start node. """

        # manhattan distance
        return abs(node.location[0] - self.start_node.location[0]) + abs(node.location[1] - self.start_node.location[1]) + abs(node.location[2] - self.start_node.location[2])

    def distance_h(self, node):
        """ Returns the estimated distance between the current node and the end node. """

        # manhattan distance
        return abs(node.location[0] - self.end_node.location[0]) + abs(node.location[1] - self.end_node.location[1]) + abs(node.location[2] - self.end_node.location[2])
    
    def cost_f(self, g, h):
        """ Returns the cost the node. """

        return g + h
    
    def valid_child(self, child):
        """ Checks if child node can be used in path according to restrictions --> If it can
        be added to the open list. """

        # check if child node is within chip grid
        if child.location[0] > self.chip.x_max or child.location[0] < 0 or child.location[1] > self.chip.y_max or child.location[1] < 0 or child.location[2] > self.chip.z_max or child.location[2] < 0:
            return False
        
        # check if child is on closed list
        elif any(child.location == closed_node.location for closed_node in self.closed_list):
            return False

        # check if gridsegment from current node to child node is not occupied
        elif (child.location, self.current_node.location) in self.chip.occupied_segments or (self.current_node.location, child.location) in self.chip.occupied_segments:
            return False

        # check if child node is not a gate, except if it the end_node
        elif any(child.location == gate.coor for gate in self.chip.gates.values()) and child.location != self.end_node.location:
            return False
    
    def heuristics(self, child, penalties):
        """ Gives childs' f value necassery penalties: if it will create an intersection of wires,
        penalties that come with every layer and penalties for nodes that surround gates (except for
        if the gate is the end_node). In penalties the heuristics are given that are to be used. """

        if 'intersections' in penalties:
            # give child node extra penalty if it will cause a crossing of wires (except it it is an end node)
            if any(child.location == gridsegment[1] for gridsegment in self.chip.occupied_segments) and child.location != self.end_node.location:
                child.f += self.intersections_penalty

        if 'layers' in penalties:
            # make higher layers less expensive
            extra_cost = 7
            for layer in range(7):
                if child.location[2] == layer:
                    child.f += extra_cost
                extra_cost -= 1

        if 'gates' in penalties:
            # gives nodes surrounding end gates extra penalty
            if child.location in self.adjoining_gates:

                # look where the gate is
                for direction in self.directions:
                    possible_gate_location = (child.location[0] + direction[0], child.location[1] + direction[1], child.location[2] + direction[2])
                    
                    # when gate is found and its location is not equal to end_node: extra penalty
                    if any(possible_gate_location == gate.coor for gate in self.chip.gates.values()) and possible_gate_location != self.end_node.location:
                        child.f += 4

class Node:
    """ Class that creates an instance of a node. A node has an location (x,y,z coordinate), a
     g value, h value and f value, and a parent node. """
    
    def __init__(self, location, parent=None):
        """ Creates instances of all the properties of a node. """

        self.location = location
        self.g = 0
        self.h = 0
        self.f = 0
        self.parent = parent


