import numpy as np
from scipy.optimize import fsolve


class CRV:
    def __init__(self, cdf):
        self.cdf = cdf

    def re(self, m=1):
        return [fsolve(self.cdf, np.random.rand(), args=(np.random.rand(),)) for _ in range(m)]