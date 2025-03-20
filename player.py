import pygame as pg
from pillar import Pillar
from typing import List

PLAYER_SIZE = 50
GRAVITY = .7
JUMP_POWER = 10

class Player:
    _last_scored_pillar: Pillar | None = None

    def __init__(self, screen: pg.Surface):
        self.player_dead = False
        self.score = 0
        self._screen: pg.Surface = screen

        self._player_img: pg.Surface = pg.image.load("imgs/bird.png")
        self._player_img = pg.transform.scale(self._player_img, (PLAYER_SIZE*1.56, PLAYER_SIZE))

        self.hitbox: pg.Rect = self._player_img.get_rect()
        self.hitbox.w = PLAYER_SIZE * 1.1
        self.hitbox.h = PLAYER_SIZE * .75
        self.hitbox.center = (screen.get_width() // 3, screen.get_height() // 2)

        self.velocity = -10
        self._adjust_attributes()

    def _adjust_attributes(self):
        self.x, self.y = self.hitbox.center
        self.bottom_x, self.bottom_y = self.hitbox.bottomright
        self.top_x, self.top_y = self.hitbox.topright

    def next_frame(self, pillars_q: list[Pillar]):
        self.velocity += GRAVITY
        self.hitbox.move_ip(0, self.velocity)
        self._rotate_player(self.velocity)
        self._adjust_attributes()
        self.player_dead = self.check_collisions_add_score(pillars_q)

    def jump(self):
        self.velocity = -JUMP_POWER

    def _rotate_player(self, velocity):
        x = self.hitbox.left - (self._player_img.get_width() - self.hitbox.w) // 2
        y = self.hitbox.top - (self._player_img.get_height() - self.hitbox.h) // 2

        rotated_image = pg.transform.rotate(self._player_img, -(velocity * 4))
        new_rect = rotated_image.get_rect(center = self._player_img.get_rect(topleft = (x, y)).center)

        self._screen.blit(rotated_image, new_rect)

    def check_collisions_add_score(self, pillars_q: List[Pillar]):
        for pillar in pillars_q:
            if pillar.is_collision(self.hitbox) or self.hitbox.top <= 0 or self.hitbox.bottom >= self._screen.get_height():
                return True
            if pillar.is_score(self.hitbox) and self._last_scored_pillar is not pillar:
                self.score += 1
                self._last_scored_pillar = pillar
        return False

    # def get_closest_pillar(self, pillars_q: List[Pillar]):
