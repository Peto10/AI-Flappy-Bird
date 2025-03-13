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

def move_pillars(pillars_q: deque[Pillar]):
    pill_offscreen = False
    for pillar in pillars_q:
        if (pillar.is_offscreen()):
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

def rotate_player(surf, player_img, player_collider, velocity):
    x = player_collider.left - (player_img.get_width() - player_collider.w) // 2
    y = player_collider.top - (player_img.get_height() - player_collider.h) // 2

    rotated_image = pg.transform.rotate(player_img, -(velocity * 4))
    new_rect = rotated_image.get_rect(center = player_img.get_rect(topleft = (x, y)).center)

    surf.blit(rotated_image, new_rect)

def check_score(player: pg.Rect, pillars_q: deque[Pillar]):
    for pillar in pillars_q:
        if pillar.is_score(player):
            return True
    return False

def player_setup():
    player_img: pg.Surface = pg.image.load("imgs/bird.png")
    player_img = pg.transform.scale(player_img, (PLAYER_SIZE*1.56, PLAYER_SIZE))
    
    player_collider: pg.Rect = player_img.get_rect()
    player_collider.w = PLAYER_SIZE * 1.1
    player_collider.h = PLAYER_SIZE * .75
    player_collider.center = (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2)
    return player_img, player_collider

def render_score(font, score, screen):
    font_img = font.render(str(score), True, (0, 0, 0))
    screen.blit(font_img, (SCREEN_WIDTH // 2 - font_img.get_width() // 2, SCREEN_HEIGHT // 10))

def render_all(screen, player_img, player_collider, font, pillars_q, velocity, score):
    player_collider.move_ip(0, velocity)
    screen.fill(BG_COLOUR)
    move_pillars(pillars_q)
    render_score(font, score, screen)
    rotate_player(screen, player_img, player_collider, velocity)

def main():
    pg.font.init()

    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pg.display.set_caption("AI Flappy Bird")
    pg.display.set_icon(pg.image.load("imgs/bird.png"))
    
    clock = pg.time.Clock()

    PILL_SPAWN_EVENT = pg.USEREVENT + 1
    pg.time.set_timer(PILL_SPAWN_EVENT, PILLAR_SPAWN_RATE)
    
    player_img, player_collider = player_setup()

    font = pg.font.SysFont('slabsherif', 60)
    
    pillars_q: deque[Pillar] = deque()
    velocity = -10
    score = 0
    game_over = False
    score_flag = False
    run = True
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == PILL_SPAWN_EVENT:
                pillars_q.append(Pillar(screen))
        
        if (pg.key.get_pressed()[pg.K_SPACE]):
            velocity = -JUMP_POWER
        velocity += GRAVITY 

        render_all(screen, player_img, player_collider, font, pillars_q, velocity, score)

        if (check_for_collisions(player_collider, pillars_q)):
            game_over = True
            run = False

        if (check_score(player_collider, pillars_q)):
            if (not score_flag):
                score_flag = True
                score += 1
        else:
            score_flag = False

        pg.display.update()
        clock.tick(60)

    pg.quit()

if __name__ == '__main__':
    main()
