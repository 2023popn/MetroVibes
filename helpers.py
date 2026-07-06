import random
import math
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

def get_line_angles_at_station(station):
    """Return angles (radians, x-right/y-down convention) pointing from this
    station toward every line segment touching it."""
    angles = []
    for line in station.lines:
        points = line.path_points
        for i, p in enumerate(points):
            if p == (station.x, station.y):
                if i > 0:
                    prev = points[i - 1]
                    angles.append(math.atan2(prev[1] - station.y, prev[0] - station.x))
                if i < len(points) - 1:
                    nxt = points[i + 1]
                    angles.append(math.atan2(nxt[1] - station.y, nxt[0] - station.x))
    return angles

def find_open_angle(occupied_angles):
    """Return the angle sitting in the largest gap between occupied angles."""
    if not occupied_angles:
        return -math.pi / 2  # default: straight up, if station has no lines yet

    angles = sorted(a % (2 * math.pi) for a in occupied_angles)
    angles.append(angles[0] + 2 * math.pi)  # wrap around the circle

    best_gap = -1
    best_angle = angles[0]
    for i in range(len(angles) - 1):
        gap = angles[i + 1] - angles[i]
        if gap > best_gap:
            best_gap = gap
            best_angle = angles[i] + gap / 2

    return best_angle

def get_anchor_name(angle):
    dx = math.cos(angle)
    dy = math.sin(angle)

    if abs(dx) < 1e-6:
        return "midbottom" if dy < 0 else "midtop"
    if abs(dy) < 1e-6:
        return "midleft" if dx > 0 else "midright"
    if dy < 0:
        return "bottomleft" if dx > 0 else "bottomright"
    else:
        return "topleft" if dx > 0 else "topright"