import random
import pygame

PILLAR_WIDTH = 100
GAP_LENGTH = 200
BORDER_WIDTH = 1

class Pillar():
    _screen: pygame.Surface | None
    _bottom_pill: pygame.Rect | None
    _top_pill: pygame.Rect | None

    def __init__(self, screen):
        self._screen = screen
        self._draw_pillar()

    def _draw_pillar(self):
        bottom_pill_height = random.randint(self._screen.get_height() // 4, self._screen.get_height() // 2)

        self._bottom_pill = pygame.Rect((
            self._screen.get_width() + PILLAR_WIDTH,
            self._screen.get_height() - bottom_pill_height + BORDER_WIDTH,
            PILLAR_WIDTH,
            bottom_pill_height + BORDER_WIDTH
        ))
        self._draw_half_pillar(self._bottom_pill)

        self._top_pill = pygame.Rect((
            self._screen.get_width() + PILLAR_WIDTH,
            -BORDER_WIDTH,
            PILLAR_WIDTH,
            self._screen.get_height() - bottom_pill_height - GAP_LENGTH + BORDER_WIDTH
        ))
        self._draw_half_pillar(self._top_pill)
        
    def _draw_half_pillar(self, pill):
        pygame.draw.rect(self._screen, (0, 255, 0), pill)
        pygame.draw.rect(self._screen, (0, 0, 0), pill, BORDER_WIDTH)

    def move_pillar(self, speed):
        self._draw_half_pillar(self._bottom_pill)
        self._draw_half_pillar(self._top_pill)

        self._bottom_pill.move_ip(-speed, 0)
        self._top_pill.move_ip(-speed, 0)

    def get_x(self):
        return self._bottom_pill.centerx
    
    def is_offscreen(self):
        return self._bottom_pill.right < 0


