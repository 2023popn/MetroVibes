import pygame
from fillet import make_fillet
from settings import LINE_WIDTH, LINE_FILLET_RADIUS

class Line:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.stations = []  # ordered list[Station]
        self.station_points = []
        self.trains = []    # list[Train] currently running on this line
        self.path_points = [] # station and interpolation points to make the actual path
        self.station_directions = []

    def add_station(self, station):
        self.stations.append(station)
        station.add_line(self)

        self.station_points.append((station.x, station.y))

        self._rebuild_path()

    def _rebuild_path(self):
        stations = self.stations
        self.path_points = []
        if not stations:
            return

        self._assign_station_direction()

        self.path_points.append((stations[0].x, stations[0].y))

        from_direction = ""
        current_direction = ""
        to_direction = ""

        for i in range(1, len(stations)):
            from_pt = self.path_points[-1]
            current = stations[i]
            current_pt = (current.x, current.y)
            next_station = stations[i + 1] if i + 1 < len(stations) else None
            next_point = (next_station.x, next_station.y) if next_station is not None else None

            # Determine current station direction requirement
            diff_to_prev = (current_pt[0] - from_pt[0], current_pt[1] - from_pt[1])
            diff_to_next = (next_point[0] - current_pt[0], next_point[1] - current_pt[1]) if next_point is not None else None

            x_diff_prev = diff_to_prev[0]
            y_diff_prev = diff_to_prev[1]
            x_diff_next = diff_to_next[0] if diff_to_next is not None else None
            y_diff_next = diff_to_next[1] if diff_to_next is not None else None

            corner_x = None
            corner_y = None

            if x_diff_prev != 0 and y_diff_prev != 0 and abs(x_diff_prev) != abs(y_diff_prev):
                if abs(x_diff_prev) > abs(y_diff_prev):
                    lesser_difference = abs(y_diff_prev)
                else:
                    lesser_difference = abs(x_diff_prev)

                # Previous station has priority
                if from_direction == "horizontal":
                    if current_direction == "vertical":
                        corner_x = from_pt[0]
                        corner_y = current_pt[1]
                    else:
                        corner_x = from_pt[0]
                        corner_y = current_pt[1] - lesser_difference * y_diff_prev / abs(y_diff_prev)

                        current_direction += "diagonal" if current_direction != "diagonal" else current_direction

                elif from_direction == "vertical":
                    if current_direction == "horizontal":
                        corner_x = current_pt[0]
                        corner_y = from_pt[1]
                    else:
                        corner_x = current_pt[0] - lesser_difference * x_diff_prev / abs(x_diff_prev)
                        corner_y = from_pt[1]

                        current_direction += "diagonal" if current_direction != "diagonal" else current_direction

                elif from_direction == "diagonal":
                    corner_x = from_pt[0] + lesser_difference * x_diff_prev / abs(x_diff_prev)
                    corner_y = from_pt[1] + lesser_difference * y_diff_prev / abs(y_diff_prev)

                    if x_diff_prev > lesser_difference:
                        current_direction += "horizontal"
                    elif y_diff_prev > lesser_difference:
                        current_direction += "vertical"

                else:
                    if current_direction == "horizontal":
                        corner_x = current_pt[0]
                        corner_y = from_pt[1] + lesser_difference * y_diff_prev / abs(y_diff_prev)
                    elif current_direction == "vertical":
                        corner_x = from_pt[0] + lesser_difference * x_diff_prev / abs(x_diff_prev)
                        corner_y = current_pt[1]
                    elif current_direction == "diagonal":
                        corner_x = current_pt[0] - lesser_difference * x_diff_prev / abs(x_diff_prev)
                        corner_y = current_pt[1] - lesser_difference * y_diff_prev / abs(y_diff_prev)
                    else:
                        corner_x = from_pt[0] + lesser_difference * x_diff_prev / abs(x_diff_prev)
                        corner_y = from_pt[1] + lesser_difference * y_diff_prev / abs(y_diff_prev)

                        if x_diff_prev > lesser_difference:
                            current_direction += "horizontal"
                        elif y_diff_prev > lesser_difference:
                            current_direction += "vertical"

            if corner_x is not None and corner_y is not None:
                arc_points = make_fillet((from_pt[0], from_pt[1]),
                                     (corner_x, corner_y),
                                     (current_pt[0], current_pt[1]),
                                     LINE_FILLET_RADIUS)
                self.path_points += arc_points

            self.path_points.append(current_pt)

            from_direction = current_direction
            current_direction = to_direction
            to_direction = ""

    def _assign_station_direction(self):
        stations = self.stations
        self.station_directions = [""] * len(stations)
        if not stations:
            return

        for i in range(1, len(stations)):
            from_station = stations[i-1]
            from_pt = (from_station.x, from_station.y)
            current = stations[i]
            current_pt = (current.x, current.y)
            next_station = stations[i + 1] if i + 1 < len(stations) else None
            next_point = (next_station.x, next_station.y) if next_station is not None else None

            current_direction = ""

            # Determine current station direction requirement
            diff_to_prev = (current_pt[0] - from_pt[0], current_pt[1] - from_pt[1])
            diff_to_next = (next_point[0] - current_pt[0],
                            next_point[1] - current_pt[1]) if next_point is not None else None

            x_diff_prev = diff_to_prev[0]
            y_diff_prev = diff_to_prev[1]
            x_diff_next = diff_to_next[0] if diff_to_next is not None else None
            y_diff_next = diff_to_next[1] if diff_to_next is not None else None


            x_diff_prev_direction = x_diff_prev / abs(x_diff_prev) if x_diff_prev != 0 else 0
            y_diff_prev_direction = y_diff_prev / abs(y_diff_prev) if y_diff_prev != 0 else 0

            if diff_to_next is not None:
                x_diff_next_direction = x_diff_next / abs(x_diff_next) if x_diff_next != 0 else 0
                y_diff_next_direction = y_diff_next / abs(y_diff_next) if y_diff_next != 0 else 0
            else:
                x_diff_next_direction = None
                y_diff_next_direction = None

                # Directly horizontal
            if x_diff_prev == 0 or x_diff_next == 0:
                current_direction += "horizontal"

            # Directly vertical
            if y_diff_prev == 0 or y_diff_next == 0:
                current_direction += "vertical"

            # Directly Diagonal
            if abs(x_diff_prev) == abs(y_diff_prev):
                current_direction += "diagonal"

            if diff_to_next is not None:
                if abs(x_diff_next) == abs(y_diff_next):
                    current_direction += "diagonal"

                if x_diff_prev_direction == x_diff_next_direction:
                    current_direction += "vertical"

                if y_diff_prev_direction == y_diff_next_direction:
                    current_direction += "horizontal"

            self.station_directions[i] = current_direction

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