import networkx as nx
from collections import deque
import random
import numpy.random
import pandas
import matplotlib.pyplot as plt


class Artist:

    def __init__(self, balance, interest, min_days):
        self.balance = balance
        self.interest = interest
        self.min_days = min_days
        self.payments = []
        self.pindex = 0

    def invest(self, agent, amount, day):
        self.payments.append((agent, amount, day))
        self.balance += amount


class Agent:

    def __init__(self):
        self.balance = 1000
        self.invested = False
        self.confidence = 0

    def pay(self, x):
        self.balance += x
        self.invested = False


class Simulation:

    def __init__(self, network, artist, agent_investment):
        self.network = network
        self.size = len(self.network)
        self.artist = artist
        self.population = [Agent() for _ in range(self.size)]

        # confidence = numpy.random.normal(0, 1, self.size)
        # for i in range(self.size):
        #     self.population[i].confidence = confidence[i]

        self.aware = set()
        self.agent_investment = agent_investment

    def add_active_investors(self, guys):
        self.aware.update(guys)

    def day(self, day):
        income = 0
        payouts = 0

        for i in self.aware:
            if not self.population[i].invested:
                investment = self.population[i].balance * self.agent_investment
                self.population[i].balance -= investment
                self.population[i].invested = True
                artist.invest(i, investment, day)
                income += investment

        new = set()
        for i in self.aware:
            selected = random.choice(list(nx.neighbors(self.network, i)))
            new.add(selected)
        self.aware.update(new)

        cindex = self.artist.pindex
        while cindex < len(self.artist.payments):
            thing = self.artist.payments[cindex]
            if day >= thing[2]+self.artist.min_days:
                needed_payment = thing[1] * self.artist.interest
                if self.artist.balance >= needed_payment:
                    self.artist.balance -= needed_payment

                    self.population[thing[0]].pay(needed_payment)
                    payouts += needed_payment
                    cindex += 1
                else:
                    break
            else:
                break
        self.artist.pindex = cindex

        return len(self.aware), income, payouts, self.artist.balance

    def simulate(self, days, init_invest):
        initial = numpy.random.choice(self.size, init_invest, replace=False)
        self.add_active_investors(initial)

        data = []
        day = 0
        while day < days:
            x = self.day(day)
            data.append(x)
            day += 1
        return data


if __name__ == "__main__":
    parameters = dict(artist_bal=0,
                      artist_int=1.01,
                      artist_delay=,
                      agent_investment=0.75)

    graph_parameters = dict(n=2000,
                            k=6,
                            p=0.2)
    network = nx.generators.watts_strogatz_graph(**graph_parameters)
    artist = Artist(parameters["artist_bal"],
                    parameters["artist_int"],
                    parameters["artist_delay"])
    simulation = Simulation(network, artist, parameters["agent_investment"])
    thing = simulation.simulate(200, 1)

    df = pandas.DataFrame(thing, columns=['active', 'income', 'payouts', 'balance'])
    fig, ax1 = plt.subplots(nrows=2, ncols=2)
    df.plot(ax=ax1[0, 0], y="payouts")
    df.plot(ax=ax1[0, 0], y="income")
    df.plot(ax=ax1[1, 0], y="balance")
    df.plot(ax=ax1[0, 1], y='active')
    plt.show()

