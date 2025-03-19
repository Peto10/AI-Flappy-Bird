import pygame as pg
from pillar import Pillar

PLAYER_SIZE = 50

class Player:
    def __init__(self, screen:pg.Surface):
        self._score = 0
        self._last_scored_pillar: Pillar | None = None
        self._screen = screen
        self.player_img: pg.Surface = pg.image.load("imgs/bird.png")
        self.player_img = pg.transform.scale(self.player_img, (PLAYER_SIZE*1.56, PLAYER_SIZE))

        self._pc: pg.Rect = self.player_img.get_rect()
        self._pc.w = PLAYER_SIZE * 1.1
        self._pc.h = PLAYER_SIZE * .75
        self._pc.center = (screen.get_width() // 3, screen.get_height() // 2)

    def move(self, x, y):
        self._pc.move_ip(x, y)
        self._rotate_player(y)

    def _rotate_player(self, velocity):
        x = self._pc.left - (self.player_img.get_width() - self._pc.w) // 2
        y = self._pc.top - (self.player_img.get_height() - self._pc.h) // 2

        rotated_image = pg.transform.rotate(self.player_img, -(velocity * 4))
        new_rect = rotated_image.get_rect(center = self.player_img.get_rect(topleft = (x, y)).center)

        self._screen.blit(rotated_image, new_rect)

    def check_collisions_add_score(self, pillars_q: list[Pillar]):
        for pillar in pillars_q:
            if pillar.is_collision(self._pc):
                return True
            if pillar.is_score(self._pc) and self._last_scored_pillar is not pillar:
                self._score += 1
                self._last_scored_pillar = pillar
        return False
    
    def get_score(self):
        return self._score