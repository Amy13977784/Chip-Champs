# Visualisation of Chip & Circuit problem.
# running the code will give the current solution and the amount of error for that particular
# solution. It also displays what coordinates belong to which connection/net. 
# In addition to this a csv.file of this output can be created (set save to True).
#
# Authors: Merel, Amy, Kyra

from classes import chip
from algorithms import random_algorithm, breadth_first, astar_algorithm, sim_annealing_algorithm

        
if __name__ == '__main__':
    chip_number = 0
    netlist = 3

    for i in range(1):
        my_chip = chip.Chip(chip_number, netlist)

        # ----- If the connections have to be ordered by gate or Manhattan distance -----
        my_chip.connection_order_by_gate()
        # my_chip.connection_order_by_distance()

        # ----- Choose the algorithm -----
        # ----- Random algorithm -----
        # validity = random_algorithm.Random_algorithm(my_chip).all_connections()

        # ----- Breadth first algorithm -----
        # breadth_first.BreadthFirst(my_chip).all_connections()

        # ----- A* algorithm -----
        #astar_algorithm.Astar(my_chip).all_connections()

        # ---- Simulated annealing algorithm ---- 
        # load a presaved solution (from A*?)
        my_chip.load_solution(file_number=1, algorithm="astar")

        sa = sim_annealing_algorithm.simulated_annealing(
        chip=my_chip,
        temperature=1000,
        cooling_rate=0.99,
        min_temperature=1)
    
        best_solution, cost = sa.run(iterations=1000, perturbation_method="reroute_connection")

        #my_chip.plot_chip()
        #cost = my_chip.calculate_cost()
        print(f'The costs for this solution: {cost}')

        # output file: (cost, algorithm, iteration, validity), only add validity for the random algorithm
        
        # output file for simulated annealing
        my_chip.output_file(cost, algorithm='simulated_annealing', file_number=i)

        # output file for A*
        # my_chip.output_file(cost, 'astar', i)

    # ----- if we want to plot a solution from an earlier saved file -----
    # chip.Chip(chip_number, netlist).plot_solution(0, 'breadthfirst')


