import random

import pygame

PILLAR_WIDTH = 100
PILLAR_SPEED = 4
GAP_LENGTH = 170
BORDER_WIDTH = 1
PILLAR_COLOR = (0, 255, 0)

class Pillar():
    def __init__(self, screen: pygame.Surface) -> None:
        self._screen: pygame.Surface = screen
        self._draw_pillar()

    def _draw_pillar(self):
        bottom_pill_height = random.randint(self._screen.get_height() // 4, self._screen.get_height() // 2)

        self.bottom_pill = pygame.Rect((
            self._screen.get_width(),
            self._screen.get_height() - bottom_pill_height + BORDER_WIDTH,
            PILLAR_WIDTH,
            bottom_pill_height + BORDER_WIDTH
        ))
        self._draw_half_pillar(self.bottom_pill)

        self.top_pill = pygame.Rect((
            self._screen.get_width(),
            -BORDER_WIDTH,
            PILLAR_WIDTH,
            self._screen.get_height() - bottom_pill_height - GAP_LENGTH + BORDER_WIDTH
        ))
        self._draw_half_pillar(self.top_pill)

        self._score_collider = pygame.Rect((
            self._screen.get_width() + PILLAR_WIDTH,
            0,
            1,
            self._screen.get_height()
        ))
        
    def _draw_half_pillar(self, pill: pygame.Rect) -> None:
        pygame.draw.rect(self._screen, PILLAR_COLOR, pill)
        pygame.draw.rect(self._screen, (0, 0, 0), pill, BORDER_WIDTH)

    def move_pillar(self) -> None:
        self.bottom_pill.move_ip(-PILLAR_SPEED, 0)
        self.top_pill.move_ip(-PILLAR_SPEED, 0)
        self._score_collider.move_ip(-PILLAR_SPEED, 0)
        self.bot_left_x, self.bot_left_y = self.top_pill.bottomleft
        self.bot_right_x, self.bot_right_y = self.top_pill.bottomright

        self._draw_half_pillar(self.bottom_pill)
        self._draw_half_pillar(self.top_pill)

    def is_offscreen(self) -> bool:
        return self.bottom_pill.right < 0
    
    def is_collision(self, other: pygame.Rect) -> bool:
        return self.bottom_pill.colliderect(other) or self.top_pill.colliderect(other)
    
    def is_score(self, other: pygame.Rect) -> bool:
        return self._score_collider.colliderect(other)
