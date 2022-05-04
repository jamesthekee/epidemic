import numpy as np
import networkx as nx
import seaborn
import pandas


class contin_SIR:
    pass


class atomic_SIR:
    # geometric vs poisson
    def __init__(self, size, beta, gamma):
        self.size = size
        self.beta = beta
        self.gamma = gamma


        self.sus = size
        self.inf = 0
        self.rem = 0

    def begin(self, init):
        if init > self.size:
            raise ValueError("Initial disease infection is larger than population")
        self.sus -= init
        self.inf += init

    def step(self):
        change = int(self.sus*self.inf*self.beta)
        loss = int(self.inf * self.gamma)
        self.sus -= change
        self.inf += change

        self.inf -= loss
        self.rem += loss


if __name__ == "__main__":
    sim = atomic_SIR(1000, 0.5, 0.1)
    sim.begin(5)

    steps = 100
    for i in range(steps):
        sim.step()
        print(sim.inf)


