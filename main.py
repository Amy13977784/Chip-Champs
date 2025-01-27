# Chips & Circuits
# Authors: Merel, Amy, Kyra

# short explanantion

import sys
from classes import chip
from algorithms import random_algorithm, breadth_first, astar_algorithm, sim_annealing_algorithm, heuristics

        
if __name__ == '__main__':

    # loop over every netlist
    for chipnumber, netlistnumber in [(0, 1), (0, 2), (0, 3), (1, 4), (1, 5), (1, 6), (2, 7), (2, 8), (2, 9)]:

        # loop over every combination of heuristiks (penatlies for nodes)
        for penalty1 in ['layers', 'intersections', 'gates']:
            for penalty2 in ['layers', 'intersections', 'gates']:

                ### ----- Adjust the following variables ----- ###

                # select chip = 1, 2 or 3 and netlist = 0, 1, 2, 3, 4, 5, 6, 7, 8 or 9
                chip_number = chipnumber
                netlist = netlistnumber

                # heuristics that change the order in which the connections will be made, select which connections have to be made first
                # choose from 'most connected gates', 'shortest distance', 'longest distance', 'center connections', 'edge connections' or None
                heuristic = 'most connected gates'

                # algorithms that can be used to make the connections
                # choose from 'random', 'breadt first', 'astar' or 'sim annealing'
                algorithm = 'astar'

                # adjust to whether you want to create an output file and plot the solution
                # choose True or False
                output_file = True
                plot_solution = True

                # if you don't want to create a chip and connections, but want to plot a previous solution from a file
                # choose True or False and also adjust the chip_number, netlist and algorithm to which are used in the solution
                plot_solution = False


                ### ----- end of adjustable variables ----- ###


                # plots a solution from an earlier saved file
                # if plot_solution == True:
                #     chip.Chip(chip_number, netlist).plot_solution(0, algorithm)
                #     sys.exit()
                

                # creates the chip
                my_chip = chip.Chip(chip_number, netlist)


                # applies a heuristic to the order in which the connections are made
                if heuristic == 'most connected gates':
                    heuristics.Heuristics(my_chip).order_by_gate()

                elif heuristic == 'shortest distance':
                    heuristics.Heuristics(my_chip).order_by_distance()

                elif heuristic == 'longest distance':
                    heuristics.Heuristics(my_chip).order_by_distance(long_first = True)

                elif heuristic == 'center connections':
                    heuristics.Heuristics(my_chip).order_by_location()

                elif heuristic == 'edge connections':
                    heuristics.Heuristics(my_chip).order_by_location(edged_first = True)
                

                # applies an algorithm to make the connections
                if algorithm == 'random':
                    validity = random_algorithm.Random_algorithm(my_chip).all_connections()

                elif algorithm == 'breadth first':
                    breadth_first.BreadthFirst(my_chip).all_connections()

                elif algorithm == 'astar':
                    astar_algorithm.Astar(my_chip, [penalty1, penalty2]).all_connections()

                elif algorithm == 'sim annealing':
                    
                    # load a presaved solution (from A*)
                    my_chip.load_solution(file_number=0, algorithm="astar")

                    sa = sim_annealing_algorithm.simulated_annealing(
                    chip=my_chip,
                    temperature=1000,
                    cooling_rate=0.99,
                    min_temperature=1)

                    best_solution = sa.run(iterations=1000)

                else:
                    print('No algorithm applied')
                    sys.exit()


                # calculates the cost of the current solution
                cost = my_chip.calculate_cost()
                print(f'The costs for this solution: {cost}')


                if output_file == True:
                    my_chip.create_output_file(cost, algorithm=algorithm)

                if plot_solution == True:
                    my_chip.plot_chip()

                # astar penalties prints
                if penalty1 == penalty2:
                    print(f'penalty used for chip {chip_number} netlist {netlist}: {penalty1}')
                else: print(f'penalties used for chip {chip_number} netlist {netlist}: {penalty1}, {penalty2}')