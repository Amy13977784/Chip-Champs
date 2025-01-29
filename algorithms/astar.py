from algorithms import general_functions as gf
from operator import attrgetter

class Astar:
    """ 
    Class implements the A* algorithm to form the connections between a start and end location.
    Method all_connection applies the algorityhm to all connections.
    Method make_connection applies the A* algorithm to the connection.
    Method distance calculates the manhattan distance between the node and target node (start or end node).
    Method heuristics adds penalties to a child nodes' f value, according to certain restrictions. 
    """

    def __init__(self, chip, penalties=[], intersections_penalty=5):
        self.chip = chip
        self.penalties = penalties
        self.intersections_penalty = intersections_penalty

        # all the possible steps the connection can take at a node
        self.directions = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]

        # all the nodes that are immediately next to a gate
        self.adjoining_gates = []
        for gate in self.chip.gates.values():
            for direction in self.directions:
                self.adjoining_gates.append((gate.coor[0] + direction[0], gate.coor[1] + direction[1], gate.coor[2] + direction[2]))


    def all_connections(self):
        """ Finds the best route for every connection and returns if all the connections are valid. """

        # connection counter
        self.counter = 0

        for connection in self.chip.connections:
            self.counter += 1
            self.start_node = Node(connection.start_location, None)
            self.end_node = Node(connection.end_location, None)
            self.connection = connection

            self.make_connection()

        return gf.Functions().validity(self.chip.connections)

    
    def make_connection(self):
        """ Makes a connection by finding the route with the lowest cost (f value). Saves all 
        possible child nodes in an open list. Only updates the coor_list if a path is found. """
        
        open_list = [self.start_node]
        closed_list = []

        # while the end node has not been reached or too many nodes are to be investigated
        while open_list and len(open_list) < 10000:

            # finds the node with the lowest f value
            self.current_node = min(open_list, key=attrgetter('f'))
   
            open_list.pop(open_list.index(self.current_node))
            closed_list.append(self.current_node)

            # if the end node has been reached
            if self.current_node.location == self.end_node.location:
                current = self.current_node

                # backtracks to find the path by moving to the parent node until the starting node has been reached
                while current.parent != None:

                    self.connection.add_coor(current.location)
                    self.chip.occupied_segments.add((current.location, current.parent.location))
                    current = current.parent

                self.connection.add_coor(self.start_node.location)

                # reverses the list to the corrrect order
                self.connection.coor_list.reverse()

                return print(f'path {self.counter}/{len(self.chip.connections)} found! :) :) :) {self.connection.coor_list}')

            # if the end node has not been reached yet
            else: 

                # generates all child nodes
                for direction in self.directions:
                    child_location = (self.current_node.location[0] + direction[0], self.current_node.location[1] + direction[1], self.current_node.location[2] + direction[2])
                    child = Node(child_location, self.current_node)

                    # checks if child is a valid step
                    if gf.Functions().valid_step(self.chip, self.connection, self.current_node.location, child.location, closed_list=closed_list):

                        child.g = self.distance(child, self.start_node)
                        child.h = self.distance(child, self.end_node)
                        child.f = child.g + child.h
                    
                        # checks if the child is already in the open list
                        if any(child.location == open_node.location and child.g > open_node.g for open_node in open_list):
                            continue

                        # adds possible penalties to the child's f value
                        self.heuristics(child, self.penalties)

                        open_list.append(child)

        print('No path found :( or open list too big')
        return None


    def distance(self, node, target_node):
        """ Returns the Manhattan distance between the given node and the target node. """
        return sum(abs(node.location[i] - target_node.location[i]) for i in range(3))

        
    def heuristics(self, child, penalties):
        """ Gives childs' f value possible penalties. It can give the f value a higher value if the route 
        will create an intersection of wires, doesn't use layers or if it uses a node that surrounds a 
        different gate then the end gate. The input penalties determines which penalties to use. """

        # adds penalty to child node if it will cause a crossing of wires
        if 'intersections' in penalties:
            if any(child.location == gridsegment[1] for gridsegment in self.chip.occupied_segments) and child.location != self.end_node.location:
                child.f += self.intersections_penalty

        # makes higher layers less expensive
        if 'layers' in penalties:
            extra_cost = 7

            for layer in range(7):
                if child.location[2] == layer:
                    child.f += extra_cost

                extra_cost -= 1

        # gives nodes surrounding gates (except its end gate) a penalty
        if 'gates' in penalties:
            if child.location in self.adjoining_gates:

                # determines the location of the gate
                for direction in self.directions:
                    possible_gate_location = (child.location[0] + direction[0], child.location[1] + direction[1], child.location[2] + direction[2])
                    
                    # adds penalty when the gate is not the end gate
                    if any(possible_gate_location == gate.coor for gate in self.chip.gates.values()) and possible_gate_location != self.end_node.location:
                        child.f += 4
                        break


class Node:
    """ Class that creates an instance of a node. A node has an location (x,y,z coordinate), a
     g value, h value and f value and a parent node. """
    
    def __init__(self, location, parent=None):
        self.location = location
        self.g = 0
        self.h = 0
        self.f = 0
        self.parent = parent


