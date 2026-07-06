import pygame
from settings import STATION_RADIUS, TEXT_COLOR

class Station:
    def __init__(self, name, x, y, is_interchange = False):
        self.name = name
        self.x = x
        self.y = y
        self.waiting_passengers = []  # list[Passenger]
        self.lines = []               # list[Line] passing through here
        self.is_interchange = is_interchange

    def add_line(self, line):
        if line not in self.lines:
            self.lines.append(line)

    def update(self, dt):
        pass  # station logic later (spawn passengers, etc.)

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), STATION_RADIUS)

        game_font = pygame.font.Font(None, 20)
        text_surface = game_font.render(self.name, True, TEXT_COLOR)

        text_rect = text_surface.get_rect(center=(int(self.x), int(self.y)))
        screen.blit(text_surface, text_rect)