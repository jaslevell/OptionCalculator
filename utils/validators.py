def validate_option_params(S, K, T, r, sigma, q=0):

    errors = []

    if S <= 0:
        errors.append("Underlying price must be positive")

    if K <= 0:
        errors.append("Strike price must be positive")

    if T < 0:
        errors.append("TTM must be positive")

    if sigma <= 0:
        errors.append("Volatility must be positive")

    if q < 0:
        errors.append("Dividend yield must be positive")

    if errors:
        return False, "; ".join(errors)

    return True, None


def validate_barrier_params(barrier_type, barrier_level, S):

    valid_types = ['up-and-out', 'up-and-in', 'down-and-out', 'down-and-in']

    if barrier_type.lower() not in valid_types:
        return False, f"Invalid barrier_type. Must be one of: {', '.join(valid_types)}"

    if barrier_level <= 0:
        return False, "Barrier level must be positive"

    if 'up' in barrier_type.lower() and barrier_level <= S:
        return False, "For up-barriers, barrier level must be > stock price"

    if 'down' in barrier_type.lower() and barrier_level >= S:
        return False, "For down-barriers, barrier level must be < stock price"

    return True, None


def validate_asian_params(average_type):

    valid_types = ['arithmetic', 'geometric']

    if average_type.lower() not in valid_types:
        return False, f"Invalid average_type. Must be one of: {', '.join(valid_types)}"

    return True, None