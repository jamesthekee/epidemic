import matplotlib.pyplot as plt


class SIR:
    """ Basic continuous SIR model
    population is real number from 0 to 1"""

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




