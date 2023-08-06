import cdf_generator as cg
import random_variable as rv
from time import time

cdf = cg.gauss(0,1)
X = rv.CRV(cdf)
t1 = time()
Vs = X.re(1000)
print(time()-t1)