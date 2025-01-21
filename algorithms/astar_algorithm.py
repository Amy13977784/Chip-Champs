import copy
from operator import attrgetter

class Astar:
    '''Class implements the A* algorithm to form a connection between a starting point (start_coor)
    and an ending point (end_coor).
    Method __init__ initiates the chip'
    Method make_connection is the A* algorithm.
    Method distance_g calculates the g value for a node.
    Method distance_h calculates the h value for a node. 
    Method cost_f calculates the f values for a node. '''
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
                while current.parent != None:

                    # add coordinade to coordinate list of connection
                    self.connection.add_coor(current.location)

                    # add backtracked step to occupied segments lsit
                    self.chip.occupied_segments.add((current.location, current.parent.location))

                    current = current.parent

                # add starting coordinate to list
                self.connection.add_coor(self.start_node.location)
                return print(f'path found! :) :) :) {self.connection.coor_list}')

            # generate list of child nodes:
            else: 
                children = []

                # adjoining nodes
                for direction in [(1,0,0), (-1,0,0), (0,1,0), (0,-1,0), (0,0,1), (0,0,-1)]:
                    child_node_location = (current_node.location[0] + direction[0], current_node.location[1] + direction[1], current_node.location[2] + direction[2])
                    children.append(Node(child_node_location, current_node))

                counter = 0
                for child in children:
                    counter += 1
                    
                    # check if child node is within chip grid
                    if child.location[0] > self.chip.x_max or child.location[0] < 0 or child.location[1] > self.chip.y_max or child.location[1] < 0 or child.location[2] > self.chip.z_max or child.location[2] < 0:
                        continue
                    
                    # check if child is on closed list
                    elif any(child.location == closed_node.location for closed_node in closed_list):
                        continue

                    # check if gridsegment from current node to child node is not occupied
                    elif (child.location, current_node.location) in self.chip.occupied_segments or (current_node.location, child.location) in self.chip.occupied_segments:
                        continue
                    
                    # # no crossing of wires
                    # elif any(child.location == gridsegment[1] for gridsegment in self.chip.occupied_segments):
                    #     continue

                    # no wires ontop of gates
                    elif any(child.location == gate.coor for gate in self.chip.gates.values()) and child.location != self.end_node.location:
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

class Node:
    ''' '''
    def __init__(self, location, parent=None):
        '''location is a coordinate (x,y,z)'''

        self.location = location
        self.g = 0
        self.h = 0
        self.f = 0
        self.parent = parent


