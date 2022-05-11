import math

import matplotlib.pyplot as plt
import math

i=10
interest = 1.02
territory = 500
income_per_territory = 2

max_value = territory*500


def get_interest(bank, max_value):
    percent = bank/max_value
    interest = 1 + 1/(1+math.exp(32*(percent-0.8)))
    return interest

interest = []
data = [i]
for steps in range(10):
    if steps % 10 == 0:
        i += territory*income_per_territory
    int = get_interest(i, max_value)
    i *= int

    i = min(i, max_value)

    data.append(i)
    interest.append(int)



# plt.plot(data)
# plt.show()

plt.plot(data)
plt.show()
