import ctypes
import platform
import random

if platform.system() == "Windows":
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)  # PROCESS_PER_MONITOR_DPI_AWARE
    except Exception:
        ctypes.windll.user32.SetProcessDPIAware()  # fallback for older Windows

import pygame
from settings import *
from helpers import *
from world import World
from station import Station
from line import Line
from train import Train

def generate_interchange_stations(world, num_stations):
    for i in range(num_stations):
        station_x = round(truncated_normal_randomization(0, SCREEN_WIDTH), -1)
        station_y = round(truncated_normal_randomization(0, SCREEN_HEIGHT), -1)
        station = Station(get_unique_station_name(), station_x, station_y, True)
        world.add_interchange_station(station)

def generate_line_with_minor_stations(world):
    new_line = Line("Red", LINE_COLORS[0])
    stations_to_add = []

    total_num_interchanges = len(world.interchange_stations)

    weights = []
    while len(weights) < total_num_interchanges - 1:
        weights = [x * 2 for x in weights]
        weights.append(1)

    num_line_interchanges = random.choices(list(range(2, total_num_interchanges+1)), weights=weights)[0]
    line_interchanges = random.sample(world.interchange_stations, k=num_line_interchanges)

    for interchange in line_interchanges:
        stations_to_add.append(interchange)

    # Generate stations between interchanges
    for i in range(len(line_interchanges) - 1):
        current_station = line_interchanges[i]
        next_station = line_interchanges[i+1]

        direction_vector = [next_station.x - current_station.x, next_station.y - current_station.y]
        magnitude_noise = truncated_normal_randomization(0, 1)

        x_noise = truncated_normal_randomization(-50, 50)
        y_noise = truncated_normal_randomization(-50, 50)

        minor_station_start_x = current_station.x + direction_vector[0] * magnitude_noise + x_noise
        minor_station_start_y = current_station.y + direction_vector[1] * magnitude_noise + y_noise

        generation_direction = random.choice(["x", "y", "xy"])
        available_stations = 0
        new_stations = []

        if generation_direction == "x":
            available_x_space = next_station.x - minor_station_start_x
            available_stations = abs(int(available_x_space / STATION_MIN_SPACING))

            num_stations = random.choice(range(available_stations + 1))

            for j in range(num_stations):
                new_station_x = round(minor_station_start_x + STATION_MIN_SPACING * j, -1)
                new_station_y = round(minor_station_start_y, -1)

                new_stations.append(Station(get_unique_station_name(), new_station_x, new_station_y))

        elif generation_direction == "y":
            available_y_space = next_station.y - minor_station_start_y
            available_stations = abs(int(available_y_space / STATION_MIN_SPACING))

            num_stations = random.choice(range(available_stations + 1))

            for j in range(num_stations):
                new_station_x = round(minor_station_start_x, -1)
                new_station_y = round(minor_station_start_y + STATION_MIN_SPACING * j, -1)

                new_stations.append(Station(get_unique_station_name(), new_station_x, new_station_y))

        elif generation_direction == "xy":
            available_x_space = next_station.x - minor_station_start_x
            available_y_space = next_station.y - minor_station_start_y
            available_space = min(available_x_space, available_y_space)
            available_stations = abs(int(available_space / STATION_MIN_SPACING))

            num_stations = random.choice(range(available_stations + 1))

            for j in range(num_stations):
                new_station_x = round(minor_station_start_x + STATION_MIN_SPACING * j, -1)
                new_station_y = round(minor_station_start_y + STATION_MIN_SPACING * j, -1)

                new_stations.append(Station(get_unique_station_name(), new_station_x, new_station_y))

        current_station_index_in_line = stations_to_add.index(current_station)
        stations_to_add[current_station_index_in_line + 1:current_station_index_in_line + 1] = new_stations

    for station in stations_to_add:
        new_line.add_station(station)
    world.add_line(new_line)

    starting_station = random.choice(new_line.stations)
    new_train = Train(new_line)
    world.add_train(new_train)

def build_demo_world():
    world = World()

    generate_interchange_stations(world, 3)

    generate_line_with_minor_stations(world)

    return world

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Metro Sim")
    clock = pygame.time.Clock()

    world = build_demo_world()

    running = True
    while running:
        dt = clock.tick(FPS) / 1000  # seconds since last frame

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        world.update(dt)

        screen.fill(BG_COLOR)
        world.draw(screen)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()