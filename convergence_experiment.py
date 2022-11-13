import numpy as np
import Zhang
import networkx as nx
import pandas
import matplotlib.pyplot as plt
import time
from core.constants import *

graph_properties = dict(size=1000,
                        average_degree=6,
                        random_mixing=0.15)
network = nx.generators.watts_strogatz_graph(graph_properties["size"], graph_properties["average_degree"], graph_properties["random_mixing"])

sim_properties = dict(network=network,
                      infect_rate=0.18,
                      recover_rate=0.25,
                      immunity_loss=0.0,
                      select_strength=10,
                      vaccine_cost=0.5,
                      policy=Policy.PARTIAL,
                      delta=0.3)
seasons = 3000
window = 200
windows = 2

# Do simulation and time it.
start = time.time()
sim = Zhang.ZhangSimulation(**sim_properties)
print(sim)
data = sim.run(seasons)
print(f"took {time.time()-start:.2f} seconds")


df = pandas.DataFrame(data)
df["total_vaccinated"] /= 1000
df["total_vaccinated"].plot()


def window_average(window, df):
    s = sum(df["total_vaccinated"].iloc[:window])
    values = [s]

    for offset in range(seasons-window-1):
        s = s + df["total_vaccinated"].iloc[window+offset] - df["total_vaccinated"].iloc[offset]
        values.append(s)

    final = np.array(values)
    return final / window


temp = window_average(window, df)
plt.plot(temp)
plt.show()

# Calculate window differences
window_difference = []
for i in range(seasons-window-window):
    delta = temp[i+window]-temp[i]
    window_difference.append(delta)
plt.plot(window_difference)
plt.show()
