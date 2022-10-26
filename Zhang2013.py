import pandas
import matplotlib.pyplot as plt
from functools import lru_cache
from core import network_sir
import math


@lru_cache(maxsize=128)
def fermi(x):
    return 1/(1+math.exp(-x))


class Zhang2013Simulation(network_sir.network_SIR):

    def __init__(self, select_strength, vaccine_cost, network, infect_rate, recover_rate,
                 initial_infection=5):
        super().__init__(network, infect_rate, recover_rate, immunity_loss=0)
        self.select_strength = select_strength
        self.vaccine_cost = vaccine_cost
        self.initial_infection = initial_infection

    # @lru_cache()
    # def get_payoff(self, unvaccinated_neighbours, vacc_cost):
    #     other = pow(1-self.infect_rate, unvaccinated_neighbours)-1
    #
    #     delta = -vacc_cost - other
    #     fermi_prob = fermi(self.select_strength*delta)
    #     return fermi_prob

    def get_strategies(self):
        limit = 500
        avg_window = 100

        # Do initial stretch
        arr = []
        for j in range(limit):
            total = 0
            for x in self.population:
                if x.vaccinated:
                    total += 1
            arr.append(total)
            self.strategy_step()

        avg = 0
        for i in range(avg_window):
            avg += arr[-i]
        return avg/avg_window

    def crap_thign(self):
        window_size = 50
        windows = 3
        sums = [0 for _ in range(windows)]
        avgs = []

        # Do initial stretch
        arr = []
        for j in range(windows*window_size):
            total = 0
            for x in self.population:
                if x.vaccinated:
                    total+=1
            arr.append(total)
            self.update_strategies()

        # Calculate two initial windows
        for x in range(windows):
            total = 0
            for i in range(window_size):
                total += arr[i+x*window_size]
            sums[x] = total

        # Continue strech until we meet convergent criteria
        mean_diff = 0
        for i in range(windows-1):
            mean_diff += abs(sums[i]-sums[i+1])
        mean_diff = mean_diff/window_size

        shift = 0
        while mean_diff > 0.25:
            avgs.append(mean_diff)
            total = 0
            for x in self.population:
                if x.vaccinated:
                    total+=1
            arr.append(total)
            self.update_strategies()

            for i in range(windows):
                sums[i] += arr[(i+1)*window_size+shift] - arr[i*window_size+shift]

            mean_diff = 0
            for i in range(windows-1):
                mean_diff += abs(sums[i]-sums[i+1])
            mean_diff = mean_diff/window_size
            shift += 1

        df = pandas.DataFrame(arr)
        df.plot.line()
        plt.show()

        mean_df = pandas.DataFrame(avgs)
        mean_df.plot.line()
        plt.show()




