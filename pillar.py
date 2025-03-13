import random
import pygame

PILLAR_WIDTH = 50
GAP_LENGTH = 200

class Pillar():
    def __init__(self, screen):
        self.bottom_pill_height = random.randint(200, 500)
        self.x = screen.get_width() - PILLAR_WIDTH - 100 # SCREEN_WIDTH - PILLAR_WIDTH # change if you want to see it
        self.screen = screen
        self.draw_pillar(screen.get_height())

    def draw_pillar(self, screen_height):
        self.draw_bottom_pillar(self.x, self.bottom_pill_height, screen_height)
        self.draw_top_pillar(self.x, screen_height - self.bottom_pill_height - GAP_LENGTH)
        
    def draw_bottom_pillar(self, x, height, screen_height):
        pygame.draw.rect(self.screen, (0, 255, 0), (x, screen_height - height, PILLAR_WIDTH, height))
        pygame.draw.rect(self.screen, (0, 0, 0), (x, screen_height - height, PILLAR_WIDTH, height), 1)

    def draw_top_pillar(self, x, height):
        pygame.draw.rect(self.screen, (0, 255, 0), (x, 0, PILLAR_WIDTH, height))
        pygame.draw.rect(self.screen, (0, 0, 0), (x, 0, PILLAR_WIDTH, height), 1)