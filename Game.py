from collections import deque
from typing import Deque, List

import pygame as pg

from pillar import Pillar
from player import Player

SCREEN_WIDTH = 800 // 1.5
SCREEN_HEIGHT = 1280 // 1.5
BG_COLOUR = (104, 203, 253)

PILLAR_SPAWN_RATE = 1_350
MAX_SPAWNED_SCREEN_PILLARS = 5
FONT_SIZE = 60

class Game:
    def __init__(self) -> None:
        pg.font.init()

        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption("AI Flappy Bird")
        pg.display.set_icon(pg.image.load("imgs/bird.png"))

        self.PILL_SPAWN_EVENT = pg.USEREVENT + 1
        pg.time.set_timer(self.PILL_SPAWN_EVENT, PILLAR_SPAWN_RATE)

        self._font = pg.font.SysFont('slabsherif', FONT_SIZE)
        
        self.pillars_q: Deque[Pillar] = deque()
        self.pillars_q.append(Pillar(self.screen))
        self.players: List[Player] = []

        self.game_stop = False

    def game_step(self) -> bool:
        if (self.game_stop):
            return False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return False
            if event.type == self.PILL_SPAWN_EVENT:
                self.pillars_q.append(Pillar(self.screen))

        self._render_all()

        pg.display.update()
        return True

    def _move_pillars(self) -> None:
        pill_offscreen = False
        for pillar in self.pillars_q:
            if (pillar.is_offscreen()):
                pill_offscreen = True
            else:
                pillar.move_pillar()

        if (pill_offscreen):
            self.pillars_q.popleft()

    def _render_score(self) -> None:
        highest_score = max([player.score for player in self.players], default=0)

        font_img = self._font.render(str(highest_score), True, (0, 0, 0))
        self.screen.blit(font_img, (SCREEN_WIDTH // 2 - font_img.get_width() // 2, SCREEN_HEIGHT // 10))

    def _render_all(self) -> None:
        self.screen.fill(BG_COLOUR)
        self._move_pillars()
        self._render_score()
        for player in self.players:
            player.next_frame(self.pillars_q)

