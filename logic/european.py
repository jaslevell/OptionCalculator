import numpy as np
from .black_scholes import BlackScholesModel
from scipy.stats import norm


class EuropeanOption:

    def __init__(self, S, K, T, r, sigma, q=0, option_type='call'):
        self.S = S
        self.K = K
        self.T = T
        self.r = r
        self.sigma = sigma
        self.q = q
        self.option_type = option_type.lower()
        self.bs_model = BlackScholesModel()
        self.d1 = self.bs_model.d1(self.S, self.K, self.T, self.r, self.sigma, self.q)
        self.d2 = self.bs_model.d2(self.S, self.K, self.T, self.r, self.sigma, self.q)

    def price(self):

       if self.option_type == 'call':
           return self.bs_model.call_price(self.S, self.K, self.T, self.r, self.sigma, self.q)
       else:
           return self.bs_model.put_price(self.S, self.K, self.T, self.r, self.sigma, self.q)

    def delta(self):

        if self.option_type == 'call':
            return norm.cdf(self.d1) * np.exp(-self.q * self.T)
        else:
            return (norm.cdf(self.d1) - 1) * np.exp(-self.q * self.T)

    def gamma(self):

        if self.T <= 0:
            return 0

        return (norm.pdf(self.d1) * np.exp(-self.q * self.T)) / (self.S * self.sigma * np.sqrt(self.T))

    def vega(self):

        if self.T <= 0:
            return 0

        return self.S * norm.pdf(self.d1) * np.sqrt(self.T) * np.exp(-self.q * self.T) / 100

    def theta(self):

        if self.T <= 0:
            return 0

        if self.option_type == 'call':
            theta = (-(self.S * norm.pdf(self.d1) * self.sigma * np.exp(-self.q * self.T)) / (2 * np.sqrt(self.T))
                    - self.r * self.K * np.exp(-self.r * self.T) * norm.cdf(self.d2)
                    + self.q * self.S * np.exp(-self.q * self.T) * norm.cdf(self.d1))
        else:
            theta = (-(self.S * norm.pdf(self.d1) * self.sigma * np.exp(-self.q * self.T)) / (2 * np.sqrt(self.T))
                    + self.r * self.K * np.exp(-self.r * self.T) * norm.cdf(-self.d2)
                    - self.q * self.S * np.exp(-self.q * self.T) * norm.cdf(-self.d1))

        return theta / 365

    def rho(self):

        if self.T <= 0:
            return 0

        if self.option_type == 'call':
            return self.K * self.T * np.exp(-self.r * self.T) * norm.cdf(self.d2) / 100
        else:
            return -self.K * self.T * np.exp(-self.r * self.T) * norm.cdf(-self.d2) / 100

    def get_all_greeks(self):

        return {
            'delta': self.delta(),
            'gamma': self.gamma(),
            'vega': self.vega(),
            'theta': self.theta(),
            'rho': self.rho()
        }