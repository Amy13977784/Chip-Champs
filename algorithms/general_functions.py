class Functions:
    """
    Class contains function that are used for all the algorithms applied to this case.
    Method valid_step checks if a found next step is valid to take.
    Method validity determines if the solution is valid or not.
    """

    def valid_step(self, chip, connection, coor_start, coor_end, check_previous_step=False, closed_list=[]):
        """ Checks if a next step on a certain gridsegment from coor_start to coor_end can be taken. """

        # checks if the segment is already occupied
        if (coor_start, coor_end) in chip.occupied_segments or(coor_end, coor_start) in chip.occupied_segments:
            return False

        # checks if coordinates are out of the grid bounds
        if any(coor < 0 for coor in coor_end) or coor_end[0] > chip.x_max or coor_end[1] > chip.y_max or coor_end[2] > chip.z_max:
            return False

        # checks if the segment ends at another gate, which is not the end gate
        if any(gate.coor == coor_end for gate in chip.gates.values()) and coor_end != connection.end_location:
                return False

        # checks if coor_end is a step backwards
        if check_previous_step and len(connection.coor_list) > 1 and coor_end == connection.coor_list[-2]:
            return False

        # checks if end coordinate is in closed list
        if closed_list and any(closed_node.location == coor_end for closed_node in closed_list):
            return False
        
        return True
    

    def validity(self, connections):
        """ Determines and return if all the connections in a solution are valid. """
        
        for connection in connections:
            
            # checks if there is a route
            if not connection.coor_list:
                return 'invalid'
            
            # checks if the connection start at the start gate and ends at the end gate
            elif connection.coor_list[0] != connection.start_location or connection.coor_list[-1] != connection.end_location:
                return 'invalid'
            
            # checks if there are no double used segments
            elif len(connection.coor_list) != len(set(connection.coor_list)):
                return 'invalid'
        
        return 'valid'

  
