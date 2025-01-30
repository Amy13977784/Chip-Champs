# Dit is nog een bestandje voor onszelf om parameters te tunen. Dit hoeft niet nagekeken te worden! 

import numpy as np
import matplotlib.pyplot as plt
from algorithms import sim_annealing
from classes import chip

class tuning_params_simulated_annealing:
    """
    This class performs a grid search to find the best start temperature and cooling rate for the
    simulated annealing algorithm.
    Method __init__ initiates the chip and other variables,
    Method plot_heatmap plots a heatmap to see what combination of temp and cooling rate gives the lowest average cost,
    Method tune performs the grid search
    """

    def __init__(self, chip, min_temp, iterations):
        self.chip = chip
        self.min_temp = min_temp
        self.iterations = iterations
        self.runs_per_combination = 10
        self.results = []
        self.heatmap = None

        self.start_temps = [10, 100, 500]
        self.cooling_rates = [0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 0.99]

    def plot_heatmap(self, output_file="output/tuning_heatmap.png"):
        """ This method plots a heatmap for combinations of the cooling rate and start temperature. """

        if self.heatmap is None:
            print("No data yet available for the heatmap.")
            return

        plt.imshow(self.heatmap, cmap="viridis", origin="lower",
                   extent=[self.cooling_rates[0], self.cooling_rates[-1], self.start_temps[0], self.start_temps[-1]])
        plt.colorbar(label = "Best Cost")
        plt.xlabel("Cooling rate")
        plt.ylabel("Starting temperature")
        plt.title("Simulated Annealing parameter tuning")
        plt.savefig(output_file)
        plt.show()

    def tune(self, input_file = None):
        """ This method performs a grid search of the cooling rate and starting temperatures. It runs the Simulated
        Annealing algorithm a set number of times for every combination and gives the  """

        if input_file:
            print(f"Loading initial solution from {input_file}...")
            self.chip.load_solution(algorithm='astar', plot=False)

        if not self.chip.occupied_segments:
            raise ValueError("Initial solution could not be loaded.")

        self.heatmap = np.zeros((len(self.start_temps), len(self.cooling_rates)))

        # perform a grid search
        for i, start_temp in enumerate(self.start_temps):
            for j, cooling_rate in enumerate(self.cooling_rates):

                print(f"Trying combination of start temp {start_temp} with cooling rate {cooling_rate}")

                # store the best costs for multiple runs
                run_costs = []

                for run in range(self.runs_per_combination):

                    print(f"Run {run}/{self.runs_per_combination}")

                    # run simulated annealing
                    sa = sim_annealing.SimulatedAnnealing(
                        chip=self.chip,
                        temperature=start_temp,
                        cooling_rate=cooling_rate,
                        min_temperature=self.min_temp,
                    )

                    try:
                        sa.run(iterations=self.iterations)

                        if sa.best_cost is None:
                            print("Simulated Annealing failed to find a valid solution. Skipping this run.")
                            continue

                        print(f"These best costs are: {sa.best_cost}")
                        run_costs.append(sa.best_cost)

                    except Exception as e:
                        print(f"This SA run failed to find a path: {e}. Skipping this run.")
                        continue

                # if no valid runs were successful, skip this combination
                if not run_costs:
                    print(f"There were no valid runs for start temp {start_temp} and cooling rate {cooling_rate}.")

                    # asssign infinity to invalid combinations
                    self.heatmap[i, j] = np.inf
                    continue

                # calculate the average cost for this combination
                avg_best_cost = np.mean(run_costs)
                print(f"The average best costs are: {avg_best_cost}")

                print(f"The run costs are: {run_costs}")

                self.results.append((start_temp, cooling_rate, avg_best_cost))
                self.heatmap[i, j] = avg_best_cost

        print(self.results)
        self.plot_heatmap(output_file="output/tuning_heatmap.png")


if __name__ == '__main__':

    chip_number = 2
    netlist = 7
    my_chip = chip.Chip(chip_number, netlist)

    min_temp = 0.1
    iterations = 70  # number of iterations for SA

    tuner = tuning_params_simulated_annealing(
        chip=my_chip,
        min_temp=min_temp,
        iterations=iterations
    )

    input_file = 'output/output_chip_2_net_7_astar_-_intersections.csv'

    tuner.tune(input_file=input_file)
