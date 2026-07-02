import ctypes
import platform

if platform.system() == "Windows":
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)  # PROCESS_PER_MONITOR_DPI_AWARE
    except Exception:
        ctypes.windll.user32.SetProcessDPIAware()  # fallback for older Windows

import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BG_COLOR, LINE_COLORS
from world import World
from station import Station
from line import Line
from train import Train

def build_demo_world():
    world = World()

    s1 = Station("A", 150, 300)
    s2 = Station("B", 400, 150)
    s3 = Station("C", 650, 300)
    for s in (s1, s2, s3):
        world.add_station(s)

    red_line = Line("Red", LINE_COLORS[0])
    for s in (s1, s2, s3):
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