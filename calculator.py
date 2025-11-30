from logic.european import EuropeanOption
from logic.american import AmericanOption
from logic.asian import AsianOption
from logic.barrier import BarrierOption
from utils.validators import (validate_option_params, validate_barrier_params, validate_asian_params)


class OptionCalculator:
    """Main calculator class that creates and prices options based on config"""

    def __init__(self, config):
        self.config = config
        self.option = None  # Will be set when we create the option
        self.results = {}

    def create_option(self):
        """
        Create the appropriate option object based on config.
        This is where we parse all the parameters and instantiate the right class.
        """
        S = float(self.config['underlying_price'])
        K = float(self.config['strike_price'])
        T = float(self.config['time_to_maturity'])
        r = float(self.config['risk_free_rate'])
        sigma = float(self.config['volatility'])
        q = float(self.config.get('dividend_yield', 0))
        option_type = self.config['option_type'].lower()
        option_style = self.config['option_style'].lower()


        is_valid, error_msg = validate_option_params(S, K, T, r, sigma, q)
        if not is_valid:
            raise ValueError(f"Invalid parameters: {error_msg}")

        # Get Monte Carlo settings (used for American, Asian, Barrier)
        num_simulations = int(self.config.get('num_simulations', 10000))
        num_steps = int(self.config.get('num_steps', 252))

        # Create the right type of option based on style
        if option_style == 'european':
            # European options use analytical Black-Scholes
            self.option = EuropeanOption(S, K, T, r, sigma, q, option_type)

        elif option_style == 'american':
            # American options need Monte Carlo with LSM
            self.option = AmericanOption(S, K, T, r, sigma, q, option_type,
                                        num_simulations, num_steps)

        elif option_style == 'asian':
            # Asian options need to know arithmetic vs geometric averaging
            average_type = self.config.get('average_type', 'arithmetic')
            is_valid, error_msg = validate_asian_params(average_type)
            if not is_valid:
                raise ValueError(f"Invalid Asian option parameters: {error_msg}")

            self.option = AsianOption(S, K, T, r, sigma, q, option_type,
                                     average_type, num_simulations, num_steps)

        elif option_style == 'barrier':
            # Barrier options need barrier type and level
            barrier_type = self.config['barrier_type'].lower()
            barrier_level = float(self.config['barrier_level'])

            # Make sure barrier makes sense (up barrier > S, down barrier < S)
            is_valid, error_msg = validate_barrier_params(barrier_type, barrier_level, S)
            if not is_valid:
                raise ValueError(f"Invalid barrier option parameters: {error_msg}")

            self.option = BarrierOption(S, K, T, r, sigma, q, option_type,
                                        num_simulations, num_steps,
                                        barrier_type, barrier_level)

        else:
            raise ValueError(f"Invalid option style: {option_style}. "
                           f"Must be one of: european, american, asian, barrier")

        return self.option

    def calculate(self, compute_greeks=True):
        """
        Run the full calculation - price and Greeks.
        Set compute_greeks=False if you just want the price (faster).
        """
        # Create the option if we haven't already
        if self.option is None:
            self.create_option()

        # Calculate Greeks if requested (can skip for speed)
        greeks = None
        if compute_greeks:
            greeks = self.option.get_all_greeks()

        # Package everything up into results dict
        self.results = {
            'price': self.option.price(),
            'greeks': greeks,
            'parameters': self.config
        }

        return self.results

    def get_results(self):
        """Get the results dict from last calculation"""
        return self.results


# Convenience function for quick calculations
def calculate_from_config(config, compute_greeks=True):
    """Quick one-liner to calculate from a config dict"""
    calculator = OptionCalculator(config)
    return calculator.calculate(compute_greeks)