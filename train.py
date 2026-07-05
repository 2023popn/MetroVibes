import pygame
import math
from settings import TRAIN_SPEED, TRAIN_WIDTH, TRAIN_LENGTH

class Train:
    def __init__(self, line):
        self.line = line
        self.passengers = []
        self.segment_index = 0   # which pair of points we're between
        self.progress = 0.0      # 0.0 to 1.0 along current segment
        self.direction = 1       # 1 forward, -1 backward along the line

    def update(self, dt):
        points = self.line.path_points
        if len(points) < 2:
            return

        a = points[self.segment_index]
        b = points[self.segment_index + self.direction]
        seg_length = ((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2) ** 0.5
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
        return x, y

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
        x, y = self.get_position()
        angle = self.get_angle()

        length = TRAIN_LENGTH  # long axis, e.g. 20
        width = TRAIN_WIDTH  # short axis, e.g. 10

        # draw un-rotated, pointing along +x, on a transparent surface
        train_surface = pygame.Surface((length, width), pygame.SRCALPHA)
        pygame.draw.rect(train_surface, (255, 255, 255), (0, 0, length, width))

        rotated = pygame.transform.rotate(train_surface, angle)
        rect = rotated.get_rect(center=(int(x), int(y)))
        screen.blit(rotated, rect)