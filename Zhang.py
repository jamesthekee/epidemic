import math
import numpy as np
import networkx as nx
import random
import pandas
import matplotlib.pyplot as plt
import scipy
from functools import lru_cache
import network_sir


SUSCEPTIBLE_STATE = 0
INFECTED_STATE = 1
REMOVED_STATE = 2
VACCINATED_STATE = 3
EXPOSED_STATE = 4


@lru_cache(maxsize=128)
def fermi(x):
    return 1/(1+math.exp(-x))


class ZhangSimulation(network_sir.network_SIR):

    def __init__(self, select_strength, vaccine_cost, network, infect_rate, recover_rate, immunity_loss=0,
                 initial_infection=5):
        super().__init__(network, infect_rate, recover_rate, immunity_loss)
        self.select_strength = select_strength
        self.vaccine_cost = vaccine_cost
        self.initial_infection = initial_infection

    def __str__(self):
        return f"Zhang sim β={self.select_strength}, c={self.vaccine_cost}"

    def get_payoff(self, agent):
        if agent == SUSCEPTIBLE_STATE:
            return 0
        elif agent == INFECTED_STATE or agent == REMOVED_STATE:
            return -1
        elif agent == VACCINATED_STATE:
            return -self.vaccine_cost

    def _update_strategies(self):
        is_vaccinated = lambda x: self.population.population[x] == VACCINATED_STATE
        get_state = lambda x: self.population.population[x]

        for i in range(self.total_population):
            neighbour = np.random.choice(self.network[i])
            if is_vaccinated(i) != is_vaccinated(neighbour):
                payoff_delta = self.get_payoff(get_state(neighbour)) \
                               -self.get_payoff(get_state(i))

                if random.random() < fermi(self.select_strength*payoff_delta):
                    self.population.population[i] = get_state(neighbour)

    def run(self, seasons=500, until_stable=False):
        epidemic_sizes = []
        total_vaccinated = []

        self.random_vaccinate(0.2)
        for i in range(seasons):
            self.population.reset(reset_vaccinated=False)
            _ = self.epidemic(initial_infection=self.initial_infection)
            epidemic_size = self.population.count_type(INFECTED_STATE) \
                            + self.population.count_type(REMOVED_STATE)

            _ = self._update_strategies()
            vaccinated = self.population.count_type(VACCINATED_STATE)

            epidemic_sizes.append(epidemic_size)
            total_vaccinated.append(vaccinated)

        return dict(epidemic_sizes=epidemic_sizes,
                    total_vaccinated=total_vaccinated)

