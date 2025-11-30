def validate_option_params(S, K, T, r, sigma, q=0):
    """
    Sanity check the basic option parameters.
    Returns (is_valid, error_message) - error_message is None if valid.
    """
    errors = []

    # Prices need to be positive
    if S <= 0:
        errors.append("Underlying price must be positive")

    if K <= 0:
        errors.append("Strike price must be positive")

    # Can't have negative time left
    if T < 0:
        errors.append("TTM must be positive")

    # Volatility has to be positive
    if sigma <= 0:
        errors.append("Volatility must be positive")

    # Dividend yield should be non-negative
    if q < 0:
        errors.append("Dividend yield must be positive")

    # If we found any problems, return them
    if errors:
        return False, "; ".join(errors)

    return True, None


def validate_barrier_params(barrier_type, barrier_level, S):
    """
    Check barrier option parameters make sense.
    The barrier needs to be in the right place relative to current price.
    """
    valid_types = ['up-and-out', 'up-and-in', 'down-and-out', 'down-and-in']

    # Make sure barrier type is one we know about
    if barrier_type.lower() not in valid_types:
        return False, f"Invalid barrier_type. Must be one of: {', '.join(valid_types)}"

    # Barrier level has to be positive
    if barrier_level <= 0:
        return False, "Barrier level must be positive"

    # Up barriers should be above the current price (otherwise they're useless)
    if 'up' in barrier_type.lower() and barrier_level <= S:
        return False, "For up-barriers, barrier level must be > stock price"

    # Down barriers should be below the current price
    if 'down' in barrier_type.lower() and barrier_level >= S:
        return False, "For down-barriers, barrier level must be < stock price"

    return True, None


def validate_asian_params(average_type):
    """
    Check Asian option parameters.
    Just need to verify the average type is valid.
    """
    valid_types = ['arithmetic', 'geometric']

    if average_type.lower() not in valid_types:
        return False, f"Invalid average_type. Must be one of: {', '.join(valid_types)}"

    return True, None