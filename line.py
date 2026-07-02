import pygame

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

        if abs(x_diff) == abs(y_diff):
            return

        if abs(x_diff) > abs(y_diff):
            new_x = self.path_points[-1][0] - abs(y_diff) * x_diff/abs(x_diff)
            new_y = self.path_points[-1][1] - y_diff
            self.path_points.append((new_x, new_y))
        elif abs(x_diff) < abs(y_diff):
            new_x = self.path_points[-1][0] - x_diff
            new_y = self.path_points[-1][1] - abs(x_diff) * y_diff/abs(y_diff)
            self.path_points.append((new_x, new_y))

        self.path_points.append((station.x, station.y))


    def update(self, dt):
        for train in self.trains:
            train.update(dt)

    def draw(self, screen):
        if len(self.stations) < 2:
            return
        points = [(p[0], p[1]) for p in self.path_points]
        pygame.draw.lines(screen, self.color, False, points, 3)
        for train in self.trains:
            train.draw(screen)