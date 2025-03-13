import pygame

from pillar import Pillar

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
BG_COLOUR = (104, 203, 253)

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("AI Flappy Bird")
    pygame.display.set_icon(pygame.image.load("imgs/bird.png"))
    
    clock = pygame.time.Clock()

    run = True
    while run:
        screen.fill(BG_COLOUR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pill = Pillar(screen)


        pygame.display.update()
        clock.tick(10)

    pygame.quit()

if __name__ == '__main__':
    main()
