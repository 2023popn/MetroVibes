import pygame
import math
from settings import TRAIN_SPEED, TRAIN_WIDTH, TRAIN_LENGTH

class Train:
    def __init__(self, line, clock, initial_station = None):
        self.line = line
        self.passengers = []
        self.segment_index = 0 if initial_station is None else self.set_starting_segment(initial_station)   # which pair of points we're between
        self.progress = 0.0      # 0.0 to 1.0 along current segment
        self.direction = 1       # 1 forward, -1 backward along the line

        if self.segment_index >= len(self.line.path_points) - 1:
            self.direction *= -1

        self.a = 0
        self.b = 0
        self.x = 0
        self.y = 0
        self.get_position()

        self.clock = clock
        self.enter_station_time = 0
        self.is_at_station = False

    def set_starting_segment(self, initial_station):
        points = self.line.path_points
        initial_point = (initial_station.x, initial_station.y)

        initial_segment_index = points.index(initial_point)
        return initial_segment_index

    def update(self, dt):
        points = self.line.path_points
        if len(points) < 2:
            return

        self.get_position()

        if (self.x, self.y) in self.line.station_points:
            if not self.is_at_station:
                self.is_at_station = True
                self.enter_station_time = pygame.time.get_ticks()

        if self.is_at_station:
            if pygame.time.get_ticks() - self.enter_station_time < 2000:
                return

            self.is_at_station = False

        seg_length = ((self.b[0] - self.a[0]) ** 2 + (self.b[1] - self.a[1]) ** 2) ** 0.5
        if seg_length == 0:
            self.segment_index += self.direction
            # bounce back and forth at line ends
            if self.segment_index <= 0 or self.segment_index >= len(points) - 1:
                self.direction *= -1
            return

        self.progress += (TRAIN_SPEED * dt) / seg_length
        if self.progress >= 1.0:
            self.progress = 0.0
            self.segment_index += self.direction
            # bounce back and forth at line ends
            if self.segment_index <= 0 or self.segment_index >= len(points) - 1:
                self.direction *= -1

    def get_position(self):
        points = self.line.path_points
        a = points[self.segment_index]
        b = points[self.segment_index + self.direction]
        x = a[0] + (b[0] - a[0]) * self.progress
        y = a[1] + (b[1] - a[1]) * self.progress

        self.a = a
        self.b = b
        self.x = x
        self.y = y

    def get_angle(self):
        points = self.line.path_points
        a = points[self.segment_index]
        b = points[self.segment_index + self.direction]
        dx = b[0] - a[0]
        dy = b[1] - a[1]
        # pygame's y-axis is flipped vs standard math, and rotate() is counter-clockwise
        angle = -math.degrees(math.atan2(dy, dx))
        return angle

    def draw(self, screen):
        angle = self.get_angle()

        length = TRAIN_LENGTH  # long axis, e.g. 20
        width = TRAIN_WIDTH  # short axis, e.g. 10

        # draw un-rotated, pointing along +x, on a transparent surface
        train_surface = pygame.Surface((length, width), pygame.SRCALPHA)
        pygame.draw.rect(train_surface, (255, 255, 255), (0, 0, length, width))

        rotated = pygame.transform.rotate(train_surface, angle)
        rect = rotated.get_rect(center=(int(self.x), int(self.y)))
        screen.blit(rotated, rect)