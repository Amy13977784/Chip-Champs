import matplotlib.pyplot as plt
import pandas as pd

class Plots:
    """ Creates a plot instance. 
    The method distribution_plot() creates a plot showing the costs and the frequency. """

    def distribution_plot(self, costs, title, file_or_list):
        """ Plots the distribution of a costs list. Only works if costs is a list or a file 
        with the list in the first column. """
        
        if file_or_list == 'file':
            df = pd.read_csv(costs)
            costs = df.iloc[:, 0].tolist()
        
        plt.hist(costs)

        plt.title(title)
        plt.xlabel('Kosten')
        plt.ylabel('Frequentie')
        plt.show()
