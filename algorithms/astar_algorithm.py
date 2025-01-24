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
        '''Makes a connection according to the A* algorithm. It will try to make the shortest route
        possible while complying to certain restrictions. This method returns the a list of coordinates
        that belong to this connection/path. I also updates the coor_list of the connection instance.'''
        open_list = []
        closed_list = []

        adjoining_gates = []
        for gate in self.chip.gates.values():
            for direction in [(1,0,0), (-1,0,0), (0,1,0), (0,-1,0), (0,0,1), (0,0,-1)]:
                adjoining_gates.append((gate.coor[0] + direction[0], gate.coor[1] + direction[1], gate.coor[2] + direction[2]))


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
                    
                    # check if child node is within chip grid
                    if child.location[0] > self.chip.x_max or child.location[0] < 0 or child.location[1] > self.chip.y_max or child.location[1] < 0 or child.location[2] > self.chip.z_max or child.location[2] < 0:
                        continue
                    
                    # check if child is on closed list
                    elif any(child.location == closed_node.location for closed_node in closed_list):
                        continue

                    # check if gridsegment from current node to child node is not occupied
                    elif (child.location, current_node.location) in self.chip.occupied_segments or (current_node.location, child.location) in self.chip.occupied_segments:
                        continue

                    # check if child node is not a gate, except if it the end_node
                    elif any(child.location == gate.coor for gate in self.chip.gates.values()) and child.location != self.end_node.location:
                        continue

                    else:
                        child.g = self.distance_g(child)
                        child.h = self.distance_h(child)
                        child.f = self.cost_f(child.g, child.h)
                    
                        # check if already in open list
                        if any(child.location == open_node.location and child.g > open_node.g for open_node in open_list):
                            continue

                        # give child node extra penalty if it will cause a crossing of wires
                        if any(child.location == gridsegment[1] for gridsegment in self.chip.occupied_segments):
                            child.f += 10 

                        # make higher layers less expensive
                        # extra_cost = 70
                        # for layer in range(7):
                        #     if child.location[2] == layer:
                        #         child.f += extra_cost
                        #     extra_cost -= 10

                        # # make nodes surrounding gates more expensive --> slechter!
                        # for node in adjoining_gates: 
                        #     if child.location == node:
                        #         child.f += child.f * 0.1

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


