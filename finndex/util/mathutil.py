'''
Provides utility functions to assist with number manipulation.
'''

__author__ = "Finn Frankis"
__copyright__ = "Copyright 2019, Crypticko"

# Linearly maps a value within one range to a new range.
def map(num, init_min, init_max, new_min, new_max):
    return (num - init_min) * (new_max - new_min) / (init_max - init_min) + new_min
