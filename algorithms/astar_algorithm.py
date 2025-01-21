import copy
from operator import attrgetter

class Astar:
    '''Class implements the A* algorithm to form a connection between a starting point (start_coor)
    and an ending point (end_coor).
    Method __init__ initiates the chip'
    Method make_connection is the A* algorithm.
    Method distance_g calculates the g value for a node.
    Method distance_h calculates the h value for a node. 
    Method cost_f calculates the f values for a node. 
    Method valid_child checks is a node can be used in the path or not'''

    def __init__(self, chip):
        '''Imports the chip in self.chip '''
        self.chip = chip

    def all_connections(self):
        """ Loops over every connection to let them form. """
    
        for connection in self.chip.connections:
            self.start_node = Node(connection.start_location, None)
            self.end_node = Node(connection.end_location, None)
            self.connection = connection
            self.make_connection()
    
    def make_connection(self):
        '''Makes a connection according to the A* algorithm. It will try to make the shortest route
        possible while complying to certain restrictions. This method returns the a list of coordinates
        that belong to this connection/path. I also updates the coor_list of the connection instance.'''
        open_list = []
        closed_list = []

        open_list.append(self.start_node)
        current_node = copy.deepcopy(self.start_node)

        # while the end node has not been reached
        while open_list:

            # get current node --> node with the lowest f value
            current_node = min(open_list, key=attrgetter('f'))

            open_list.pop(open_list.index(current_node))
            closed_list.append(current_node)

            if current_node.location == self.end_node.location:
                current = current_node

                # while there is a parent node/until the starting node has been reached
                while current.parent != None:

                    # add coordinade to coordinate list of connection
                    self.connection.add_coor(current.location)

                    # add backtracked step to occupied segments
                    self.chip.occupied_segments.add((current.location, current.parent.location))

                    current = current.parent

                # add starting coordinate to list
                self.connection.add_coor(self.start_node.location)

                self.connection.coor_list.reverse()
                return print(f'path found! :) :) :) {self.connection.coor_list}')

            # generate list of child nodes:
            else: 
                children = []

                # adjoining nodes
                for direction in [(1,0,0), (-1,0,0), (0,1,0), (0,-1,0), (0,0,1), (0,0,-1)]:
                    child_node_location = (current_node.location[0] + direction[0], current_node.location[1] + direction[1], current_node.location[2] + direction[2])
                    children.append(Node(child_node_location, current_node))

                for child in children:
                    
                    # check if child node will cause a valid step
                    if self.valid_child(current_node.location, child.location, self.connection) == False:
                        continue
                    
                    else:
                        child.g = self.distance_g(child)
                        child.h = self.distance_h(child)
                        child.f = self.cost_f(child.g, child.h)

                        # give child node extra penalty if it will cause a crossing of wires
                        if any(child.location == gridsegment[1] for gridsegment in self.chip.occupied_segments):
                            child.f += 10
                    
                        # check if already in open list
                        if any(child.location == open_node.location and child.g > open_node.g for open_node in open_list):
                            continue
            
                        else: 
                            open_list.append(child)

        return print('No path found :(')

    def distance_g(self, node):
        '''Returnst the distance from the current node to the start node.'''

        # manhattan distance
        return abs(node.location[0] - self.start_node.location[0]) + abs(node.location[1] - self.start_node.location[1]) + abs(node.location[2] - self.start_node.location[2])

    def distance_h(self, node):
        ''' Returns the estimated distance between the current node and the end node.'''

        # manhattan distance
        return abs(node.location[0] - self.end_node.location[0]) + abs(node.location[1] - self.end_node.location[1]) + abs(node.location[2] - self.end_node.location[2])
    
    def cost_f(self, g, h):
        ''' Returns the cost the node.'''

        return g + h
    
    def valid_child(self, current, child, connection):
        """ Checks if a child node is a valid step to be taken, by checking if that segment is 
        not yet occupied, not out of bounds, not to a different gate and not a step backwards. """
        # checks if the segment is already occupied
        segment_occupied = (current, child) in self.chip.occupied_segments or \
                        (current, child) in self.chip.occupied_segments

        # checks if child node is out of bounds
        out_of_bounds = any(coor < 0 for coor in child) or child[0] > self.chip.x_max or \
                        child[1] > self.chip.y_max or child[2] > self.chip.z_max

        # checks if child node is not any of the other gates that is not the end node
        valid_end = child == connection.end_location or \
                    all(gate.coor != child for gate in self.chip.gates.values())

        # combines conditions
        if not segment_occupied and not out_of_bounds and valid_end:
            return True

        return False

class Node:
    '''Class that creates an instance of a node. A node has an location (x,y,z coordinate), a
     g value, h value and f value, and a parent node. '''
    def __init__(self, location, parent=None):
        '''Creates instances of all the properties of a node.'''

        self.location = location
        self.g = 0
        self.h = 0
        self.f = 0
        self.parent = parent


