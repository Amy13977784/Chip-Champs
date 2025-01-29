class Functions:

    def valid_step(self, chip, connection, coor_start, coor_end, check_previous_step=False, closed_list=[]):
        """ Checks if a next step on a certain gridsegment can be taken, by checking if that segment is
        not already occupied, not out of bounds, not to a different gate and not a step backwards. """

        # checks if the segment is not already occupied
        if (coor_start, coor_end) in chip.occupied_segments or(coor_end, coor_start) in chip.occupied_segments:
            return False

        # checks if coordinates are not out of the grid bounds
        if any(coor < 0 for coor in coor_end) or coor_end[0] > chip.x_max or coor_end[1] > chip.y_max or coor_end[2] > chip.z_max:
            return False

        # checks if the segment does not end at another gate, by checking if coor_end is not any of the other gates
        if any(gate.coor == coor_end for gate in chip.gates.values()) and coor_end != connection.end_location:
                return False

        # checks if coor_end is not a step backwards
        if check_previous_step and len(connection.coor_list) > 1 and coor_end == connection.coor_list[-2]:
            return False

        # checks if end coordinate is in closed list
        if closed_list and any(closed_node.location == coor_end for closed_node in closed_list):
            return False
        
        return True
    

    def validity(self, connections):
        
        for connection in connections:
            if not connection.coor_list:
                return 'invalid'
            elif connection.coor_list[0] != connection.start_location or connection.coor_list[-1] != connection.end_location:
                return 'invalid'
            elif len(connection.coor_list) != len(set(connection.coor_list)):
                return 'invalid'
        
        return 'valid'

  
