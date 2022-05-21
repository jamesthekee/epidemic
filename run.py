import Zhang
import networkx as nx
import pandas
import matplotlib.pyplot as plt
from constants import *

graph_properties = dict(size=1000,
                        average_degree=6,
                        random_mixing=0.5)

# network = nx.generators.watts_strogatz_graph(graph_properties["size"], graph_properties["average_degree"], graph_properties["random_mixing"])
network = nx.generators.barabasi_albert_graph(graph_properties["size"],
                                              graph_properties["average_degree"]//2)
sim_properties = dict(network=network,
                      policy=FREE_SUBSIDY,
                      delta=0.7,
                      infect_rate=0.18,
                      recover_rate=0.25,
                      select_strength=50,
                      vaccine_cost=0.5)

sim = Zhang.ZhangSimulation(**sim_properties)
print(network)
print(sim)

data = sim.run(seasons=3000)
df = pandas.DataFrame(data)
df.plot()
plt.show()

num = df["total_vaccinated"].loc[-1000:]
print(num)
print(num.mean())
