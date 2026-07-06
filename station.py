import pygame
import math
from settings import STATION_RADIUS, TEXT_COLOR
from helpers import get_line_angles_at_station, find_open_angle, get_anchor_name

_game_font = None

def _get_font():
    global _game_font
    if _game_font is None:
        _game_font = pygame.font.Font(None, 20)
    return _game_font


class Station:
    def __init__(self, name, x, y, is_interchange = False):
        self.name = name
        self.x = x
        self.y = y
        self.waiting_passengers = []  # list[Passenger]
        self.lines = []               # list[Line] passing through here
        self.is_interchange = is_interchange

    def create_text_objects(self):
        angle = find_open_angle(get_line_angles_at_station(self))
        label_radius = STATION_RADIUS + 14  # distance from center, tune to taste
        label_x = self.x + math.cos(angle) * label_radius
        label_y = self.y + math.sin(angle) * label_radius

        font = _get_font()
        text_surface = font.render(self.name, True, TEXT_COLOR)
        text_rect = text_surface.get_rect()
        anchor = get_anchor_name(angle)
        setattr(text_rect, anchor, (int(label_x), int(label_y)))
        return text_surface, text_rect

    def add_line(self, line):
        if line not in self.lines:
            self.lines.append(line)

    def update(self, dt):
        pass  # station logic later (spawn passengers, etc.)

    def draw_name(self, screen):
        text_surface, text_rect = self.create_text_objects()
        screen.blit(text_surface, text_rect)

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), STATION_RADIUS)

        self.draw_name(screen)