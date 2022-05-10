import math
import numpy as np
import networkx as nx
import random
import pandas
import matplotlib.pyplot as plt
import scipy
from functools import lru_cache


SUSCEPTIBLE_STATE = 0
INFECTED_STATE = 1
REMOVED_STATE = 2
VACCINATED_STATE = 3
EXPOSED_STATE = 4


class Population:
    def __init__(self, size):
        self.total_population = size
        self.population = [SUSCEPTIBLE_STATE for _ in range(self.total_population)]

    def reset(self, reset_vaccinated=False):
        if reset_vaccinated:
            for i in range(self.total_population):
                self.population[i] = SUSCEPTIBLE_STATE
            return

        for i in range(self.total_population):
            if self.population[i] != VACCINATED_STATE:
                self.population[i] = SUSCEPTIBLE_STATE

    def begin_epidemic(self, init):
        initial_infected = np.random.choice(self.total_population, size=init, replace=False)
        cur = set()
        for i in initial_infected:
            self.population[i] = INFECTED_STATE
            cur.add(i)
        return cur

    def count_type(self, type):
        total = 0
        for x in self.population:
            if x == type:
                total += 1
        return total


class network_SIR:


    def __init__(self, network, infect_rate, recover_rate, immunity_loss=0):


        if not nx.is_connected(network):
            raise ValueError("Provided network is not connected")

        for k in [infect_rate, recover_rate]:
            if not 0 < infect_rate <= 1:
                raise ValueError(f"{k.__name__} is not in interval (0, 1]")

        self.network = network
        self.total_population = len(network.nodes)
        self.population = Population(self.total_population)
        self.infect_rate = infect_rate
        self.recover_rate = recover_rate
        self.immunity_loss = immunity_loss

    def reset(self, reset_vaccinated=False):
        self.population.reset(reset_vaccinated=reset_vaccinated)

    def _SIR_step(self, cur_infected):
        # S->I : get infected
        new_infected = set()
        for i in cur_infected:
            for neighbor in nx.neighbors(self.network, i):
                if self.population.population[neighbor] == SUSCEPTIBLE_STATE \
                    and random.random() < self.infect_rate:
                    new_infected.add(neighbor)
                    self.population.population[neighbor] = INFECTED_STATE

        # R->S : loose immunity
        if self.immunity_loss:
            for i in range(self.total_population):
                if self.population.population[i] == REMOVED_STATE and random.random() < self.immunity_loss:
                    self.population.population[i] = SUSCEPTIBLE_STATE

        # I->R : recover from infection
        new_removed = set()
        for i in cur_infected:
            if random.random() < self.recover_rate:
                new_removed.add(i)
                self.population.population[i] = REMOVED_STATE

        cur_infected = cur_infected.difference(new_removed)
        cur_infected = cur_infected.union(new_infected)

        return cur_infected

    def epidemic(self, initial_infection=5, step_limits=None):
        if not step_limits:
            step_limits = float("inf")

        infected_data = []
        cur = self.population.begin_epidemic(initial_infection)
        infected_data.append(len(cur))

        i = 0
        while cur and i < step_limits:
            cur = self._SIR_step(cur)
            infected_data.append(len(cur))
            i += 1
        return infected_data

    def random_vaccinate(self, prop):
        # TODO: Do later lol
        pass
        count = int(self.total_population*prop)
        victims = np.random.choice(self.total_population, count, replace=False)
        for i in victims:
            self.population.population[i] = VACCINATED_STATE

    def get_count(self, x):
        return self.population.count_type(x)


if __name__ == "__main__":
    graph_properties = dict(size=1000,
                            average_degree=6,
                            random_mixing=0.15)
    network = nx.generators.watts_strogatz_graph(graph_properties["size"], graph_properties["average_degree"], graph_properties["random_mixing"])
    sim_properties = dict(network=network,
                          infect_rate=0.18,
                          recover_rate=0.25,
                          immunity_loss=0.024)

    sim = network_SIR(**sim_properties)
    data = np.array(sim.epidemic(step_limits=2500))
    data = data / graph_properties["size"]
    plt.plot(data)
    plt.show()


