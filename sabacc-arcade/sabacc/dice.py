def roll_dice(num_dice=2):
    """Roll a specified number of dice and return the results as a list."""
    return [random.randint(1, 6) for _ in range(num_dice)]