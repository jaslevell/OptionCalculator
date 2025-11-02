from .monte_carlo import MonteCarloEngine


class AsianOption:

    def __init__(self, S, K, T, r, sigma, q=0, option_type='call', average_type='arithmetic', num_simulations=10000, num_steps=252):
        self.S = S
        self.K = K
        self.T = T
        self.r = r
        self.sigma = sigma
        self.q = q
        self.option_type = option_type.lower()
        self.average_type = average_type.lower()
        self.num_simulations = num_simulations
        self.num_steps = num_steps
        self.mc_engine = MonteCarloEngine(num_simulations, num_steps)

    def price(self):
       return self.mc_engine.price_asian(self.S, self.K, self.T, self.r, self.sigma, self.q, self.option_type, self.average_type)

    def delta(self, bump=0.01):

        S_up = self.S + bump
        S_down = self.S - bump

        mc_up = MonteCarloEngine(self.num_simulations, self.num_steps, seed=42)
        mc_down = MonteCarloEngine(self.num_simulations, self.num_steps, seed=42)

        price_up = mc_up.price_asian(S_up, self.K, self.T, self.r, self.sigma, self.q,
                                      self.option_type, self.average_type)
        price_down = mc_down.price_asian(S_down, self.K, self.T, self.r, self.sigma, self.q,
                                          self.option_type, self.average_type)

        return (price_up - price_down) / (2 * bump)

    def gamma(self, bump=0.01):

        S_up = self.S + bump
        S_down = self.S - bump

        mc_up = MonteCarloEngine(self.num_simulations, self.num_steps, seed=42)
        mc_center = MonteCarloEngine(self.num_simulations, self.num_steps, seed=42)
        mc_down = MonteCarloEngine(self.num_simulations, self.num_steps, seed=42)

        price_up = mc_up.price_asian(S_up, self.K, self.T, self.r, self.sigma, self.q,
                                      self.option_type, self.average_type)
        price_center = mc_center.price_asian(self.S, self.K, self.T, self.r, self.sigma, self.q,
                                              self.option_type, self.average_type)
        price_down = mc_down.price_asian(S_down, self.K, self.T, self.r, self.sigma, self.q,
                                          self.option_type, self.average_type)

        return (price_up - 2 * price_center + price_down) / (bump ** 2)

    def vega(self, bump=0.01):

        sigma_up = self.sigma + bump
        sigma_down = self.sigma - bump

        mc_up = MonteCarloEngine(self.num_simulations, self.num_steps, seed=42)
        mc_down = MonteCarloEngine(self.num_simulations, self.num_steps, seed=42)

        price_up = mc_up.price_asian(self.S, self.K, self.T, self.r, sigma_up, self.q,
                                      self.option_type, self.average_type)
        price_down = mc_down.price_asian(self.S, self.K, self.T, self.r, sigma_down, self.q,
                                          self.option_type, self.average_type)

        return (price_up - price_down) / (2 * bump) / 100

    def theta(self, bump=1/365):

        T_down = max(self.T - bump, 0)

        mc_center = MonteCarloEngine(self.num_simulations, self.num_steps, seed=42)
        mc_down = MonteCarloEngine(self.num_simulations, self.num_steps, seed=42)

        price_center = mc_center.price_asian(self.S, self.K, self.T, self.r, self.sigma, self.q,
                                              self.option_type, self.average_type)
        price_down = mc_down.price_asian(self.S, self.K, T_down, self.r, self.sigma, self.q,
                                          self.option_type, self.average_type)

        return (price_down - price_center) / bump

    def rho(self, bump=0.01):

        r_up = self.r + bump
        r_down = self.r - bump

        mc_up = MonteCarloEngine(self.num_simulations, self.num_steps, seed=42)
        mc_down = MonteCarloEngine(self.num_simulations, self.num_steps, seed=42)

        price_up = mc_up.price_asian(self.S, self.K, self.T, r_up, self.sigma, self.q,
                                      self.option_type, self.average_type)
        price_down = mc_down.price_asian(self.S, self.K, self.T, r_down, self.sigma, self.q,
                                          self.option_type, self.average_type)

        return (price_up - price_down) / (2 * bump) / 100

    def get_all_greeks(self):
        return {
            'delta': self.delta(),
            'gamma': self.gamma(),
            'vega': self.vega(),
            'theta': self.theta(),
            'rho': self.rho()
        }