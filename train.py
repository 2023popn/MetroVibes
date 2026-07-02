import pygame
from settings import TRAIN_SIZE, TRAIN_SPEED

class Train:
    def __init__(self, line):
        self.line = line
        self.passengers = []
        self.segment_index = 0   # which pair of stations we're between
        self.progress = 0.0      # 0.0 to 1.0 along current segment
        self.direction = 1       # 1 forward, -1 backward along the line

    def update(self, dt):
        stations = self.line.stations
        if len(stations) < 2:
            return

        a = stations[self.segment_index]
        b = stations[self.segment_index + self.direction]
        seg_length = ((b.x - a.x) ** 2 + (b.y - a.y) ** 2) ** 0.5
        if seg_length == 0:
            return

        self.progress += (TRAIN_SPEED * dt) / seg_length
        if self.progress >= 1.0:
            self.progress = 0.0
            self.segment_index += self.direction
            # bounce back and forth at line ends
            if self.segment_index <= 0 or self.segment_index >= len(stations) - 1:
                self.direction *= -1

    def get_position(self):
        stations = self.line.stations
        a = stations[self.segment_index]
        b = stations[self.segment_index + self.direction]
        x = a.x + (b.x - a.x) * self.progress
        y = a.y + (b.y - a.y) * self.progress
        return x, y

    def draw(self, screen):
        x, y = self.get_position()
        rect = pygame.Rect(0, 0, TRAIN_SIZE, TRAIN_SIZE)
        rect.center = (int(x), int(y))
        pygame.draw.rect(screen, (255, 255, 255), rect)