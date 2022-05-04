import numpy as np
import networkx as nx
import numpy.random
import random
import pandas
import matplotlib.pyplot as plt



SUSCEPTIBLE_STATE = 0
INFECTED_STATE = 1
REMOVED_STATE = 2

class network_SIR:

    def __init__(self, network, trans, recover, immunity_loss=0):
        self.network = network
        self.total_population = len(network.nodes)
        self.population = [SUSCEPTIBLE_STATE for _ in range(self.total_population)]
        self.trans = trans
        self.recover = recover
        self.imm_loss = immunity_loss

    def reset(self):
        for i in range(self.total_population):
            self.population = SUSCEPTIBLE_STATE

    def begin_infection(self, init):
        initial_infected = numpy.random.randint(0, self.total_population, init)
        cur = set()
        for i in initial_infected:
            self.population[i] = INFECTED_STATE
            cur.add(i)
        return cur

    def SIR_step(self, cur_infected):
        new_infected = set()
        for i in cur_infected:
            for neighbor in nx.neighbors(self.network, i):
                if self.population[neighbor] == SUSCEPTIBLE_STATE \
                    and random.random() < self.trans:
                    new_infected.add(neighbor)
                    self.population[neighbor] = INFECTED_STATE

        # Loose immunisiation
        for i in range(self.total_population):
            if self.population[i] == REMOVED_STATE and random.random() < self.imm_loss:
                self.population[i] = SUSCEPTIBLE_STATE

        new_removed = set()
        for i in cur_infected:
            if random.random() < self.recover:
                new_removed.add(i)
                self.population[i] = REMOVED_STATE

        cur_infected = cur_infected.difference(new_removed)
        cur_infected = cur_infected.union(new_infected)

        return cur_infected

    def epidemic_to_completion(self):
        if self.imm_loss > 0:
            raise ValueError("oops")

        infected_data = []
        cur = self.begin_infection(5)
        infected_data.append(len(cur))
        while cur:
            cur = self.SIR_step(cur)
            infected_data.append(len(cur))
        return infected_data

    def epidemic_steps(self, n):
        infected_data = []
        cur = self.begin_infection(5)
        infected_data.append(len(cur))

        i = 0
        while cur and i < n:
            cur = self.SIR_step(cur)
            infected_data.append(len(cur))
            i += 1
        return infected_data

    def get_total_infected(self):
        total = 0
        for x in self.population:
            if x ==1 or x == 2:
                total += 1
        return total


if __name__ == "__main__":
    network = nx.generators.watts_strogatz_graph(5000, 6, 0.15)
    # network = nx.generators.barabasi_albert_graph(10000, 3)

    sim = network_SIR(network, 0.18, 0.25, immunity_loss=0.022)
    data = numpy.array(sim.epidemic_steps(2500))

    data = data / 5000
    # print(sim.get_total_infected())
    plt.plot(data)
    plt.show()


