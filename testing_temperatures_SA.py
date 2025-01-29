import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from algorithms import sim_annealing

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
        self.min_temp = min_temp  # termination temperature 
        self.iterations = iterations
        self.runs_per_combination = 10
        self.results = []  
        self.heatmap = None  

        self.start_temps = [10, 100, 500, 1000, 5000, 10000]
        self.cooling_rates = [0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 0.99]

    def plot_heatmap(self, output_file="heatmap.png"):
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

    def tune(self):
        """ This method performs a grid search of the cooling rate and starting temperatures. It runs the Simulated
        Annealing algorithm a set number of times for every combination and gives the  """

        self.heatmap = np.zeros((len(self.start_temps), len(self.cooling_rates)))

        # Perform a grid search 
        for i, start_temp in enumerate(self.start_temps):
            for j, cooling_rate in enumerate(self.cooling_rates):

                # Store the best costs for multiple runs
                run_costs = [] 

                for run in range(self.runs_per_combination):

                    # Run simulated annealing
                    sa = sim_annealing.simulated_annealing(
                        chip=self.chip,
                        temperature=start_temp,
                        cooling_rate=cooling_rate,
                        min_temperature=self.min_temp,
                    )

                    sa.run(iterations=self.iterations)

                    # Collect the best cost for this run
                    run_costs.append(sa.best_cost)

                # Calculate the average cost for this combination
                avg_best_cost = np.mean(run_costs)

                self.results.append((start_temp, cooling_rate, avg_best_cost))
                self.heatmap[i, j] = avg_best_cost

        self.plot_heatmap(self.start_temps, self.cooling_rates, output_file = "tuning_heatmap.png")




