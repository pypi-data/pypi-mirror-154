import numpy as np
from scipy.integrate import quad

def gauss(mu, sigma):
    def gauss_cdf(x, p=0):
        def func(t, mean, std):
            return (1/np.sqrt(2*np.pi)) * np.exp((-1/2) * ((t-mean)/std)**2)
        y = quad(func, -np.inf, x, args=(mu, sigma))[0]
        return y - p
    return gauss_cdf