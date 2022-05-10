import Zhang
import networkx as nx
import pandas
import matplotlib.pyplot as plt

graph_properties = dict(size=1000,
                        average_degree=6,
                        random_mixing=0.15)
network = nx.generators.watts_strogatz_graph(graph_properties["size"], graph_properties["average_degree"], graph_properties["random_mixing"])

sim_properties = dict(network=network,
                      infect_rate=0.18,
                      recover_rate=0.25,
                      immunity_loss=0.0,
                      select_strength=1,
                      vaccine_cost=0.8)

sim = Zhang.ZhangSimulation(**sim_properties)
print(sim)

data = sim.run(seasons=100)
df = pandas.DataFrame(data)
df.plot()
plt.show()