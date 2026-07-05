import pygame
from fillet import make_fillet
from settings import LINE_WIDTH, LINE_FILLET_RADIUS

class Line:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.stations = []  # ordered list[Station]
        self.trains = []    # list[Train] currently running on this line
        self.path_points = [] # station and interpolation points to make the actual path

    def add_station(self, station):
        self.stations.append(station)
        station.add_line(self)

        if len(self.stations) == 1:
            self.path_points.append((station.x, station.y))
            return

        last_x = self.path_points[-1][0]
        last_y = self.path_points[-1][1]

        x_diff = last_x - station.x
        y_diff = last_y - station.y

        if x_diff != 0 and y_diff != 0:
            if abs(x_diff) > abs(y_diff):
                corner_x = self.path_points[-1][0] - abs(y_diff) * x_diff / abs(x_diff)
                corner_y = self.path_points[-1][1] - y_diff

                arc_points = make_fillet((last_x, last_y),
                            (corner_x, corner_y),
                            (station.x, station.y),
                            LINE_FILLET_RADIUS)

                self.path_points += arc_points
            elif abs(x_diff) < abs(y_diff):
                corner_x = self.path_points[-1][0] - x_diff
                corner_y = self.path_points[-1][1] - abs(x_diff) * y_diff / abs(y_diff)

                arc_points = make_fillet((last_x, last_y),
                                         (corner_x, corner_y),
                                         (station.x, station.y),
                                         LINE_FILLET_RADIUS)

                self.path_points += arc_points

        self.path_points.append((station.x, station.y))


    def update(self, dt):
        for train in self.trains:
            train.update(dt)

    def draw(self, screen):
        if len(self.stations) < 2:
            return
        points = [(p[0], p[1]) for p in self.path_points]
        pygame.draw.lines(screen, self.color, False, points, LINE_WIDTH)
        for train in self.trains:
            train.draw(screen)