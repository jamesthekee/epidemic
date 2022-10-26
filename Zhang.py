import math
import numpy as np
import random
from functools import lru_cache
from core.network_sir import NetworkSIR
from core.constants import *


@lru_cache(maxsize=128)
def fermi(x):
    return 1 / (1 + math.exp(-x))


class ZhangSimulation(NetworkSIR):

    def __init__(self, policy, delta, select_strength, vaccine_cost, network, infect_rate, recover_rate,
                 initial_infection=5, immunity_loss=0):
        super().__init__(network, infect_rate, recover_rate, immunity_loss)
        self.policy = policy
        self.select_strength = select_strength
        self.vaccine_cost = vaccine_cost
        self.effective_vaccine_cost = self.vaccine_cost
        self.delta = delta
        self.initial_infection = initial_infection
        self.free_vaccinated = []

        if self.policy == Policy.PARTIAL:
            if self.delta <= 0 or self.delta > 1:
                raise ValueError("Given delta value out of expected interval of (0, 1]")

            self.effective_vaccine_cost = self.vaccine_cost * (1 - self.delta)
        elif self.policy == Policy.FREE_SUBSIDY:
            donees = int(self.total_population * self.delta)
            self.free_vaccinated = np.random.choice(self.total_population, donees, replace=False)

    def __str__(self):
        return f"Zhang: policy={self.policy}, δ={self.delta} β={self.select_strength}, c={self.vaccine_cost}"

    def get_payoff(self, agent_index):
        state = self.population.population[agent_index]

        if agent_index in self.free_vaccinated:
            if state == State.VACCINATED:
                return 0

        if state == State.SUSCEPTIBLE:
            return 0
        elif state == State.INFECTED or state == State.REMOVED:
            return -1
        elif state == State.VACCINATED:
            return -self.effective_vaccine_cost

    def _update_strategies(self):
        is_vaccinated = lambda x: self.population.population[x] == State.VACCINATED
        get_state = lambda x: self.population.population[x]

        # TODO: Deep copy of population to ensure it is done in parallel.
        copy = self.population.population
        for i in range(self.total_population):
            neighbour = np.random.choice(self.network[i])
            if is_vaccinated(i) != is_vaccinated(neighbour):
                payoff_delta = self.get_payoff(neighbour) \
                               - self.get_payoff(i)

                if random.random() < fermi(self.select_strength * payoff_delta):
                    copy[i] = get_state(neighbour)

        # assert self.population.population != copy
        self.population.population = copy

    def run(self, seasons=500, until_stable=False):
        epidemic_sizes = []
        total_vaccinated = []

        self.random_vaccinate(0.5)
        for i in range(seasons):
            self.population.reset(reset_vaccinated=False)
            _ = self.epidemic(initial_infection=self.initial_infection)
            epidemic_size = self.population.count_type(State.INFECTED) \
                            + self.population.count_type(State.REMOVED)

            _ = self._update_strategies()
            vaccinated = self.population.count_type(State.VACCINATED)

            epidemic_sizes.append(epidemic_size)
            total_vaccinated.append(vaccinated)

        return dict(epidemic_sizes=epidemic_sizes,
                    total_vaccinated=total_vaccinated)
