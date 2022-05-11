import numpy as np

class RandomBatchManager:

    def __init__(self, n):
        self.n = n
        self.i = 0
        self.numbers = np.random.random(n)

    def get(self):
        k = self.numbers[self.i]
        self.i += 1

        if self.i == self.n:
            self.numbers = np.random.random(self.n)
            self.i = 0
        return k
