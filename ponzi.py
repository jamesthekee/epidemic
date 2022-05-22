import math
import networkx as nx
import random
import numpy.random
import pandas
import matplotlib.pyplot as plt


def sigmoid(x):
    if x < -50:
        return 0
    elif x > 50:
        return 1
    return 1/(1+math.exp(-x))


class Artist:

    def __init__(self, balance, interest, min_days, init_investors):
        self.balance = balance
        self.interest = interest
        self.min_days = min_days
        self.payments = []
        self.pindex = 0
        self.init_investors = init_investors

    def invest(self, agent, amount, day):
        self.payments.append((agent, amount, day))
        self.balance += amount

    def __str__(self):
        return f"Artist, bal={self.balance}, interest={self.interest}, days+={self.min_days}, seed={self.init_investors}"




class Agent:

    def __init__(self):
        self.balance = 1000
        self.invested = False
        self.confidence = 0

    def pay(self, x):
        self.balance += x
        self.invested = False


class Simulation:

    def __init__(self, network, artist, agent_investment, confidence_increase, confidence_variance,
                 base_confidence, global_increase, global_decline):
        self.network = network
        self.size = len(self.network)
        self.artist = artist
        self.population = [Agent() for _ in range(self.size)]
        self.global_sentiment = 0

        self.global_increase = global_increase
        self.global_decline = global_decline
        self.confidence_increase = confidence_increase

        confidence = numpy.random.normal(base_confidence, confidence_variance, self.size)
        for i in range(self.size):
            self.population[i].confidence = confidence[i]

        self.aware = set()
        self.agent_investment = agent_investment

    def __str__(self):
        return f"Ponzi simulation, N={self.size}, inv={self.agent_investment}, c+={self.confidence_increase} gs+={self.global_increase}, gs-={self.global_decline}"


    def add_active_investors(self, guys):
        self.aware.update(guys)

    def day(self, day):
        income = 0
        payouts = 0

        crowd_think = 2*(2*sigmoid(self.global_sentiment) -1)
        # Possible investors
        for i in self.aware:
            if not self.population[i].invested:

                probability = sigmoid(self.population[i].confidence + crowd_think)
                if random.random() < probability:
                    investment = self.population[i].balance * self.agent_investment
                    self.population[i].balance -= investment
                    self.population[i].invested = True
                    artist.invest(i, investment, day)
                    income += investment

        # Spread awareness
        new = set()
        for i in self.aware:
            if self.population[i].invested:
                selected = random.choice(list(nx.neighbors(self.network, i)))
                new.add(selected)
                # self.population[selected].confidence += 0.05
        self.aware.update(new)

        # Make due pay investments
        cindex = self.artist.pindex
        while cindex < len(self.artist.payments):
            record = self.artist.payments[cindex]
            if day >= record[2]+self.artist.min_days:
                needed_payment = record[1] * self.artist.interest
                if self.artist.balance >= needed_payment:
                    self.artist.balance -= needed_payment

                    self.population[record[0]].pay(needed_payment)
                    self.population[record[0]].confidence += self.confidence_increase
                    payouts += needed_payment
                    cindex += 1
                    self.global_sentiment += self.global_increase
                else:
                    break
            else:
                break

        for i in range(cindex, len(self.artist.payments)):
            record = self.artist.payments[cindex]
            if day >= record[2]+self.artist.min_days:
                self.global_sentiment -= self.global_decline

        self.artist.pindex = cindex

        return len(self.aware), income, payouts, self.artist.balance

    def simulate(self, days):
        initial = numpy.random.choice(self.size, self.artist.init_investors, replace=False)
        self.add_active_investors(initial)

        data = []
        day = 0
        while day < days:
            x = self.day(day)
            data.append(x)
            day += 1
        return data


if __name__ == "__main__":
    art_param = dict(balance=0,
                     interest=1.05,
                     min_days=10,
                     init_investors=5)
    agent_param = dict(agent_investment=0.3,
                       confidence_increase=0.05,
                       base_confidence=-5,
                       confidence_variance=6,
                       global_increase=0,
                       global_decline=0.1)

    graph_parameters = dict(n=2000,
                            k=6,
                            p=0.2)
    network = nx.generators.watts_strogatz_graph(**graph_parameters)
    artist = Artist(**art_param)
    simulation = Simulation(network, artist, **agent_param)

    print(network)
    print(artist)
    print(simulation)

    original_confidences = [x.confidence for x in simulation.population]

    thing = simulation.simulate(500)

    # df = pandas.DataFrame(thing, columns=['active', 'income', 'payouts', 'balance'])
    # fig, ax1 = plt.subplots(nrows=2, ncols=2)
    # df.plot(ax=ax1[0, 0], y="payouts")
    # df.plot(ax=ax1[0, 0], y="income")
    # df.plot(ax=ax1[1, 0], y="balance")
    # df.plot(ax=ax1[0, 1], y='active')

    wealths = [x.balance/1000 for x in simulation.population]
    confidences = [x.confidence for x in simulation.population]
    # wealths.sort()
    # ax1[1, 1].scatter(confidences, wealths, alpha=0.2)

    # sizes = [0.2 + 10*sigmoid(original_confidences[x]) for x in range(len(confidences))]
    # colors = [(sigmoid(original_confidences[x]) ,0,0) for x in range(len(confidences))]
    # plt.scatter(confidences, wealths, s=sizes, c=colors)
    conf_wealth = zip(original_confidences, wealths)
    data = sorted(conf_wealth, key = lambda x: x[0])

    plt.scatter([x[0] for x in data], [y[1] for y in data], s=2, alpha=0.4)

    plt.xlabel("Original confidence")
    plt.ylabel("Wealth increase")
    plt.tight_layout()
    plt.show()

