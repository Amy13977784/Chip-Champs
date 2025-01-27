# Visualisation of Chip & Circuit problem.
# running the code will give the current solution and the amount of error for that particular
# solution. It also displays what coordinates belong to which connection/net. 
# In addition to this a csv.file of this output can be created (set save to True).
#
# Authors: Merel, Amy, Kyra

import sys
from classes import chip
from algorithms import random_algorithm, breadth_first, astar_algorithm, sim_annealing_algorithm, heuristics

        
if __name__ == '__main__':
    chip_number = 0
    netlist = 2

    # choose from 'order by gate', 'order by distance', 'order by location' or None
    heuristic = 'order by gate'

    # choose from 'random', 'breadt first', 'astar' or 'sim annealing'
    algorithm = 'astar'

    # choose True or False
    output_file = True
    plot_chip = True

    plot_solution = False


    # ----- if we want to plot a solution from an earlier saved file -----
    
    if plot_solution == True:
        chip.Chip(chip_number, netlist).plot_solution(0, algorithm)
        sys.exit()
    

    my_chip = chip.Chip(chip_number, netlist)


    # ----- If the connections have to be ordered by gate or Manhattan distance -----
    if heuristic == 'order by gate':
        heuristics.Heuristics(my_chip).order_by_gate()

    elif heuristic == 'order by distance':
        heuristics.Heuristics(my_chip).order_by_distance()

    elif heuristic == 'order by location':
        heuristics.Heuristics(my_chip).order_by_location()

    
    if algorithm == 'random':
        validity = random_algorithm.Random_algorithm(my_chip).all_connections()

    elif algorithm == 'breadth first':
        breadth_first.BreadthFirst(my_chip).all_connections()

    elif algorithm == 'astar':
        astar_algorithm.Astar(my_chip).all_connections()

    elif algorithm == 'sim annealing':
        
        # load a presaved solution (from A*)
        my_chip.load_solution(file_number=0, algorithm="astar")

        sa = sim_annealing_algorithm.simulated_annealing(
        chip=my_chip,
        temperature=1000,
        cooling_rate=0.99,
        min_temperature=1)

        best_solution = sa.run(iterations=1000, perturbation_method="reroute_connection")

    else:
        print('No algorithm applied')
        sys.exit()


    cost = my_chip.calculate_cost()
    print(f'The costs for this solution: {cost}')


    if output_file == True:
        my_chip.create_output_file(cost, algorithm=algorithm)

    if plot_chip == True:
        my_chip.plot_chip()