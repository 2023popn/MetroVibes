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
from world_generation import generate_interchange_stations, generate_line_with_minor_stations

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