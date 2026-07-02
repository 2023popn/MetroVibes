import pygame

class Line:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.stations = []  # ordered list[Station] - defines the path
        self.trains = []    # list[Train] currently running on this line

    def add_station(self, station):
        self.stations.append(station)
        station.add_line(self)

    def update(self, dt):
        for train in self.trains:
            train.update(dt)

    def draw(self, screen):
        if len(self.stations) < 2:
            return
        points = [(s.x, s.y) for s in self.stations]
        pygame.draw.lines(screen, self.color, False, points, 3)
        for train in self.trains:
            train.draw(screen)