import pygame
from settings import STATION_RADIUS

class Station:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.waiting_passengers = []  # list[Passenger]
        self.lines = []               # list[Line] passing through here

    def add_line(self, line):
        if line not in self.lines:
            self.lines.append(line)

    def update(self, dt):
        pass  # station logic later (spawn passengers, etc.)

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), STATION_RADIUS)