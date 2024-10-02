from math import factorial

import matplotlib.pyplot as plt
import pandas as pd
 

class MultiplierFunc():
      
    def __init__(self, n, r) -> None:
        self.n = n
        self.r = r

    def probability_distribution(self, x:int) -> int:

        numerator = factorial(self.n-self.r) * factorial(self.n-x)
        denominator = factorial(self.n) * factorial(self.n-self.r-x)

        return numerator / denominator # Frequency

    def frequency_table(self) -> pd.DataFrame:
      
        results_table = dict()

        x = 0
        while self.n-self.r-x >= 0: # As long as you can make non-negative moves
            results_table[x] = self.probability_distribution(x,self.n,self.r)
            x += 1

        self.results_table = pd.DataFrame(list(results_table.items()), columns=["x", "frequency"])
        self.results_table["multiplier"] = [1/frequency for frequency in self.results_table.values()]

        return self.results_table
    
    def plot_frequency(self):

        if self.results_table is None:
            self.frequency_table()

        plt.title(f"Plot of the distribution for n:{self.n}, r:{self.r}")
        plt.plot(self.results_table["x"], self.results_table["frequency"], label = "frequency of x")
        plt.plot(self.results_table["x"], self.results_table["multiplier"], label = "multiplier at x")
        plt.legend()
        plt.show()

        return 1
    
    def hello(self):
        print(self.results_table)
                    

temp = MultiplierFunc(25,3)

temp.hello()