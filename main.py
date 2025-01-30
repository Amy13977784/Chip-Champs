# Chips & Circuits
# Authors: Merel, Amy, Kyra

# This program creates solutions for the chips and circuits case. 
# It gets a chip and netlist as input and finds the best connections.

import sys
import argparse
from classes import chip
from algorithms import astar, general_functions, random, breadth_first, sim_annealing, heuristics


def get_input(prompt, valid_values, input_message):
    while True:
        print(f"\n{input_message}")
        user_input = input(prompt).strip().lower()

        if user_input in valid_values:
            return user_input

def set_argument_parser():
    # create the parser
    parser = argparse.ArgumentParser(description='Arguments')
    
    # define all the arguments
    parser.add_argument('--solution', type=str, help='Creating or loading a solution, or finding the best output file')
    parser.add_argument('--chip_number', type=str, help='Chip number (0, 1 or 2)')
    parser.add_argument('--netlist', type=str, help='Netlist number (integer from 1-9)')
    parser.add_argument('--algorithm', type=str, help='Which algorithm to use to make the connections (random, breadth_first, astar, sim annealing)')
    parser.add_argument('--plot_chip', type=str, help='Whether to plot the solution (True or False)')

    # if arguments are not provided in the command line, ask for them as input
    args = parser.parse_args()

    try: 
        if args.solution not in ['loading', 'creating', 'best_solution']:
            args.solution = get_input('Enter if you are creating or loading a solution, or want to load the file with the best overall solution: ',
                valid_values=['loading', 'creating', 'best_solution'], input_message='Choose loading, creating or best_solution.')

        if args.chip_number not in ['0', '1', '2']:
            args.chip_number = get_input('Enter the chip number: ',
                valid_values=['0', '1', '2'], input_message='Choose 0, 1 or 2 and enter only the number.')

        netlist_options = {'0': ['1', '2', '3'], '1': ['4', '5', '6'], '2': ['7', '8', '9']}
        if args.netlist not in netlist_options[args.chip_number]:
            args.netlist = get_input(f'Enter the netlist: ', valid_values=netlist_options[args.chip_number],
                input_message=f"With chip {args.chip_number} you can only choose netlists {', '.join(netlist_options[args.chip_number])}.")

        if args.algorithm not in ['random', 'breadth_first', 'astar', 'sim_annealing'] and args.solution not in ['best_solution']:
            args.algorithm = get_input('Enter which algorithm to make the connections with: ',
                valid_values=['random', 'breadth_first', 'astar', 'sim_annealing'],
                input_message='Choose from: random, breadth_first, astar or sim_annealing.')

        if args.plot_chip not in ['true', 'false'] and args.solution not in ['best_solution']:
            args.plot_chip = get_input('Enter if you want to plot the solution: ',
                valid_values=['true', 'false'], input_message='Choose true or false. Use lowercase letters.')
        
        if args.solution not in ['best_solution']:
            args.plot_chip = args.plot_chip.lower() == 'true'

    except KeyboardInterrupt:
        print("\nInput interrupted. Exiting...")
        exit()

    print('\nArguments received:')
    for arg, value in vars(args).items():
        print(f'{arg}: {value}')
    print()
    
    return args

        
if __name__ == '__main__':

    astar_heuristics = {'1': {'connection_order': [], 'penalties': []},
                    '2': {'connection_order': ['order by distance'], 'penalties': ['intersections']},
                    '3': {'connection_order': ['order by distance'], 'penalties': ['intersections']},
                    '4': {'connection_order': ['order by location'], 'penalties': ['intersections']},
                    '5': {'connection_order': ['order by location', 'order by distance'], 'penalties': ['gates', 'intersections', 8]},
                    '6': {'connection_order': ['order by location', 'order by distance'], 'penalties': ['gates', 'intersections', 7]},
                    '7': {'connection_order': ['order by gates', 'order by distance'], 'penalties': ['intersections', 7]},
                    '8': {'connection_order': ['order by distance'], 'penalties': ['intersections']},
                    '9': {'connection_order': ['order by distance'], 'penalties': ['gates', 'intersections', 6]}}

    args = set_argument_parser()


    # creates the chip
    my_chip = chip.Chip(args.chip_number, args.netlist)

    # returns the file with the lowest cost for a certain chip and netlist
    if args.solution == 'best_solution':
        best_cost, best_file = my_chip.find_best_output(output_dir='output')

        if best_file:
            print(f"The file with the best costs for chip {args.chip_number} and netlist {args.netlist} is: {best_file} with costs {best_cost}")
        else:
            print("No file found.")

        sys.exit()

    # plots a solution from an earlier saved file
    if args.solution == 'loading':
        validity = my_chip.load_solution(args.algorithm, plot=args.plot_chip)
        cost = my_chip.calculate_cost()
        print(f'The solution is {validity} and has a cost of {cost}.')

        sys.exit()

    if args.algorithm == 'astar':
        for heuristic in astar_heuristics[args.netlist]['connection_order']:
            
            # applies a heuristic to the order in which the connections are made
            if heuristic == 'order by gates':
                heuristics.Heuristics(my_chip).order_by_gate()

            elif heuristic == 'order by distance':
                heuristics.Heuristics(my_chip).order_by_distance()

            elif heuristic == 'order by location':
                heuristics.Heuristics(my_chip).order_by_location()
    

    # applies an algorithm to make the connections
    if args.algorithm == 'random':
        validity = random.Random_algorithm(my_chip).all_connections()

    elif args.algorithm == 'breadth_first':

        validity = breadth_first.BreadthFirst(my_chip, beam=2).all_connections()

    elif args.algorithm == 'astar':
        penalties = astar_heuristics[args.netlist]['penalties']

        if penalties and type(penalties[-1]) == int:
            validity = astar.Astar(my_chip, penalties[:-1], penalties[-1]).all_connections()
        else:
            validity = astar.Astar(my_chip, penalties).all_connections()

    elif args.algorithm == 'sim_annealing':
        
        for i in range (10):
            # load a presaved solution (from A*)
            my_chip.load_solution(algorithm='astar')

            sa = sim_annealing.SimulatedAnnealing(
            chip = my_chip,
            temperature = 1000,
            cooling_rate = 0.9,
            min_temperature = 0.1,
            )

            sa.run(iterations = 10000)
            
            my_chip = sa.best_solution
            validity = general_functions.Functions().validity(my_chip.connections)

            cost = my_chip.calculate_cost()
            print(f'\nThe solution is {validity} and has a cost of {cost}.')
            my_chip.create_output_file(cost, args.algorithm, validity, i)


    # calculates the cost of the current solution
    cost = my_chip.calculate_cost()
    print(f'\nThe solution is {validity} and has a cost of {cost}.')
    my_chip.create_output_file(cost, args.algorithm, validity)

    if args.plot_chip == True:
        my_chip.plot_chip()
