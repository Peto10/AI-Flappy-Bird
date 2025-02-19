import pygame
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
RECT_WIDTH = 50
GAP_LENGTH = 200
BG_COLOUR = (104, 203, 253)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("AI Flappy Bird")
pygame.display.set_icon(pygame.image.load("imgs/bird.png"))

clock = pygame.time.Clock()

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    screen.fill(BG_COLOUR)

    pillar_height = random.randint(200, 500)

    pygame.draw.rect(screen, (0, 255, 0),
                     (SCREEN_WIDTH - RECT_WIDTH, SCREEN_HEIGHT - pillar_height, RECT_WIDTH, pillar_height))
    pygame.draw.rect(screen, (0, 0, 0),
                     (SCREEN_WIDTH - RECT_WIDTH, SCREEN_HEIGHT - pillar_height, RECT_WIDTH, pillar_height), 1)
    
    pygame.draw.rect(screen, (0, 255, 0),
                     (SCREEN_WIDTH - RECT_WIDTH, 0, RECT_WIDTH, SCREEN_HEIGHT - pillar_height - GAP_LENGTH))
    pygame.draw.rect(screen, (0, 0, 0),
                     (SCREEN_WIDTH - RECT_WIDTH, 0, RECT_WIDTH, SCREEN_HEIGHT - pillar_height - GAP_LENGTH), 1)


    pygame.display.update()
    
    clock.tick(1)

pygame.quit()
