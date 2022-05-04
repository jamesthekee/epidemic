import numpy as np
import networkx as nx
# import seaborn
import pandas
import matplotlib.pyplot as plt


class contin_SIR:
    def __init__(self, beta, gamma):
        self.beta = beta
        self.gamma = gamma

        self.sus = 1
        self.inf = 0
        self.rem = 0

    def begin(self, init):
        if init > 1:
            raise ValueError("Initial disease infection is larger than population")
        self.sus -= init
        self.inf += init

    def step(self):
        change = self.sus*self.inf*self.beta
        loss = self.inf * self.gamma
        self.sus -= change
        self.inf += change

        self.inf -= loss
        self.rem += loss


if __name__ == "__main__":

    sim2 = contin_SIR(0.5, 0.1)
    sim2.begin(0.01)

    steps = 100
    data1 = []
    data2 = []
    for i in range(steps):
        sim2.step()
        data2.append(sim2.inf)

    # plt.plot(data1)
    # plt.show()
    plt.plot(data2)
    plt.show()


