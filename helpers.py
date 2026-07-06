import random
from settings import *

PREFIXES = ["North", "South", "East", "West", "Upper", "Lower", "Old", "New"]
ROOTS = ["Bridge", "Park", "River", "Hill", "Mill", "Cross", "Grove", "Harbor", "Vale", "Market"]
SUFFIXES = ["", " Square", " Station", " Junction", " Terminal", " Gate"]

used_names = set()

def get_unique_station_name():
    while True:
        name = generate_station_name()
        if name not in used_names:
            used_names.add(name)
            return name

def generate_station_name():
    name = random.choice(ROOTS)
    if random.random() < 0.4:
        name = random.choice(PREFIXES) + " " + name
    name += random.choice(SUFFIXES)
    return name

def truncated_normal_randomization(min, max):
    mean = (min + max) / 2
    std_dev = (max - min) / 6

    while True:
        num = random.gauss(mean, std_dev)
        if min <= num <= max:
            return num