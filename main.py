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
        station_x = truncated_normal_randomization(0, SCREEN_WIDTH)
        station_y = truncated_normal_randomization(0, SCREEN_HEIGHT)
        station = Station(get_unique_station_name(), station_x, station_y, True)
        world.add_interchange_station(station)

def generate_line_with_minor_stations(world):
    total_num_interchanges = len(world.interchange_stations)

    weights = []
    while len(weights) < total_num_interchanges - 1:
        weights = [x * 2 for x in weights]
        weights.append(1)

    num_line_interchanges = random.choices(range(2, total_num_interchanges+1), weights=weights, k=1)
    line_interchanges = random.sample(world.interchange_stations, k=num_line_interchanges)




def build_demo_world():
    world = World()

    generate_interchange_stations(world, 3)

    red_line = Line("Red", LINE_COLORS[0])
    for s in world.stations:
        red_line.add_station(s)
    world.add_line(red_line)

    train = Train(red_line)
    world.add_train(train)

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