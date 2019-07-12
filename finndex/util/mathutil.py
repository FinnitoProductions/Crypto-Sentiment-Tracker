# Linearly maps a value within one range to a new range.
def map(num, init_min, init_max, new_min, new_max):
    return (num - init_min) * (new_max - new_min) / (init_max - init_min) + new_min
