class Astar:
    '''Class implements the A* algorithm to form a connection between a starting point (start_coor)
    and an ending point (end_coor).
    Method __init__ initiates the chip, occupied segments list, open_list and 
    closed_list.'
    Method make_connection is the A* algorithm.
    Method distance_g calculates the g value for a node.
    Method distance_h calculates the h value for a node. 
    Method cost_f calculates the f values for a node. '''
    def __init__(self, chip):

        self.chip = chip
        self.occupied_segments = chip.occupied_segments

        self.open_list = []
        self.closed_list = []

    def all_connections(self):
        """ Loops over every connection to let them form. """
        for connection in self.chip.connections:
            self.start_node = Node(connection.start_location)
            self.end_node = Node(connection.end_location)
            self.connection = connection
            self.make_connection()
    
    def make_connection(self):

        self.open_list.append(self.start_node)

        # while the end node has not been reached
        while len(self.open_list) > 0:
            
            # get current node --> node with the lowest f value
            current_node = min(self.open_list, key=lambda node: node.f)

            self.open_list.pop(self.open_list.index(current_node))
            self.closed_list.append(current_node)
            self.connection.add_coor(current_node)

            if current_node.location == self.end_node.location:
                print('path found!')
            
            # generate list of child nodes:
            else: 
                children = []

                # adjoining nodes
                for direction in [(1,0,0), (-1,0,0), (0,1,0), (0,-1,0), (0,0,1), (0,0,-1)]:
                    child_node = current_node.location + direction
                    children.append(Node(child_node))

                for child in children:

                    # check if child node is within chip grid
                    if child.location[0] > self.chip.x_max or child.location[0] < 0 or child.location[1] > self.chip.y_max or child.location[1] < 0 or child.location[2] > self.chip.z_max or child.location[2] < 0:
                        continue
                    
                    # check if child is on closed list
                    if any(child.location == closed_node.location for closed_node in self.closed_list):
                        continue

                    # check if gridsegment from current node to child node is not occupied
                    if (child.location, current_node.location) in self.occupied_segments or (current_node.location, child.location) in self.occupied_segments:
                        continue

                    child.g = self.distance_g(child)
                    child.h = self.distance_h(child)
                    child.f = self.cost_f(child.g, child.h)

                    if any(child.location == open_node.location and child.g > open_node.g for open_node in self.open_list):
                        continue
                    else: 
                        self.open_list.append(child)


    def distance_g(self, node):
        '''Returnst the distance from the current node to the start node. '''

        # manhattan distance
        return abs(node.location[0] - self.start_node.location[0]) + abs(node.location[1] - self.start_node.location[1]) + abs(node.location[2] - self.start_node.location[2])

    def distance_h(self, node):
        ''' Returns the estimated distance between the current node and the end node.'''

        x = self.end_node.location[0] - node.location[0]
        y = self.end_node.location[1] - node.location[1]
        z = self.end_node.location[2] - node.location[0]

        # pythagorean theorem
        return x**2 + y**2 + z**2
    
    def cost_f(self, g, h):
        ''' Returns the cost the node.'''

        return g + h

class Node:
    ''' '''
    def __init__(self, location):
        '''location is a coordinate (x,y,z)'''

        self.location = location
        self.g = 0
        self.h = 0
        self.f = 0


