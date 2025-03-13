import pygame as pg
from collections import deque

from pillar import Pillar

SCREEN_WIDTH = 800 / 1.5
SCREEN_HEIGHT = 1280 / 1.5
BG_COLOUR = (104, 203, 253)

PILLAR_SPAWN_RATE = 1_300
PILLAR_SPEED = 4
MAX_SPAWNED_SCREEN_PILLARS = 5

PLAYER_SIZE = 50

GRAVITY = .7
JUMP_POWER = 10

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

def check_for_collisions(player: pg.Rect, pillars_q: deque[Pillar]):
    for pillar in pillars_q:
        if pillar.is_collision(player):
            return True
    return False

def blit_rotate_center(surf, image, topleft, angle):

    rotated_image = pg.transform.rotate(image, -(angle * 4))
    new_rect = rotated_image.get_rect(center = image.get_rect(topleft = topleft).center)

    surf.blit(rotated_image, new_rect)

def main():
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pg.display.set_caption("AI Flappy Bird")
    pg.display.set_icon(pg.image.load("imgs/bird.png"))
    
    clock = pg.time.Clock()
    PILL_SPAWN = pg.USEREVENT + 1
    pg.time.set_timer(PILL_SPAWN, PILLAR_SPAWN_RATE)

    pillars_q: deque[Pillar] = deque()
    
    player_img: pg.Surface = pg.image.load("imgs/bird.png")
    player_img = pg.transform.scale(player_img, (PLAYER_SIZE*1.56, PLAYER_SIZE))
    
    player_collider: pg.Rect = player_img.get_rect()
    player_collider.w = PLAYER_SIZE * 1.1
    player_collider.h = PLAYER_SIZE * .75
    player_collider.center = (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2)

    velocity = -10
    run = True
    while run:
        if (pg.key.get_pressed()[pg.K_SPACE]):
            velocity = -JUMP_POWER
        velocity += GRAVITY

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == PILL_SPAWN:
                pillars_q.append(Pillar(screen))

        pg.draw.rect(screen, (255, 0, 0), player_collider)
        screen.fill(BG_COLOUR)
        player_collider.move_ip(0, velocity)

        x = player_collider.left - (player_img.get_width() - player_collider.w) // 2
        y = player_collider.top - (player_img.get_height() - player_collider.h) // 2
        blit_rotate_center(screen, player_img, (x, y), velocity)

        update_pillars_pos(pillars_q)
        if (check_for_collisions(player_collider, pillars_q)):
            print("COLLISION")

        pg.display.update()
        clock.tick(60)

    pg.quit()

if __name__ == '__main__':
    main()
