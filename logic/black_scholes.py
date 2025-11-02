import numpy as np
from scipy.stats import norm


class BlackScholesModel:

    @staticmethod
    def d1(S, K, T, r, sigma, q=0):
        if T <= 0: return 0
        return (np.log(S / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))

    @staticmethod
    def d2(S, K, T, r, sigma, q=0):
        if T <= 0: return 0
        return BlackScholesModel.d1(S, K, T, r, sigma, q) - sigma * np.sqrt(T)

    @staticmethod
    def call_price(S, K, T, r, sigma, q=0):
        if T <= 0: return max(S - K, 0)
        return S * np.exp(-q * T) * norm.cdf(BlackScholesModel.d1(S, K, T, r, sigma, q)) - K * np.exp(-r * T) * norm.cdf(BlackScholesModel.d2(S, K, T, r, sigma, q))

    @staticmethod
    def put_price(S, K, T, r, sigma, q=0):
        if T <= 0: return max(K - S, 0)
        return K * np.exp(-r * T) * norm.cdf(-BlackScholesModel.d2(S, K, T, r, sigma, q)) - S * np.exp(-q * T) * norm.cdf(-BlackScholesModel.d1(S, K, T, r, sigma, q))

    @staticmethod
    def simulate_paths(S0, T, r, sigma, q, num_simulations, num_steps):

        dt = T / num_steps
        paths = np.zeros((num_simulations, num_steps + 1))
        paths[:, 0] = S0

        for t in range(1, num_steps + 1):
            Z = np.random.standard_normal(num_simulations)
            paths[:, t] = paths[:, t-1] * np.exp((r - q - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * Z)

        return paths