import pygame
from collections import deque

from pillar import Pillar

SCREEN_WIDTH = 800 / 1.5
SCREEN_HEIGHT = 1280 / 1.5
BG_COLOUR = (104, 203, 253)

PILLAR_SPAWN_RATE = 1_300
PILLAR_SPEED = 4
MAX_SPAWNED_SCREEN_PILLARS = 5

def _is_ofscreen(pillar: Pillar):
    return pillar.get_x() < -SCREEN_WIDTH

def update_pillars_pos(pillars_q: deque[Pillar]):
    pill_offscreen = False
    for pillar in pillars_q:
        if (_is_ofscreen(pillar)):
            pill_offscreen = True
        else:
            pillar.move_pillar(PILLAR_SPEED)

    if (pill_offscreen):
        pillars_q.popleft()

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("AI Flappy Bird")
    pygame.display.set_icon(pygame.image.load("imgs/bird.png"))
    
    clock = pygame.time.Clock()
    PILL_SPAWN = pygame.USEREVENT + 1
    pygame.time.set_timer(PILL_SPAWN, PILLAR_SPAWN_RATE)

    pillars_q: deque[Pillar] = deque()
    
    run = True
    while run:
        screen.fill(BG_COLOUR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == PILL_SPAWN:
                pillars_q.append(Pillar(screen))
        
        update_pillars_pos(pillars_q)

        pygame.display.update()
        clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    main()
